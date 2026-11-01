"""Own disposable verification paths separately from durable development records."""

import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4


class Invocation:
    """Track one verification command's owned paths and persistent outcomes."""

    def __init__(
        self,
        *,
        checkout: Path,
        workspace: Path | None = None,
        keep_workspace: bool = False,
    ) -> None:
        """Allocate exclusive workspace and records below the harness checkout."""
        self.keep_workspace = keep_workspace
        self.checkout = checkout.resolve()
        self.workspace = (
            workspace.resolve()
            if workspace is not None
            else Path(tempfile.mkdtemp(prefix="agentic-ml-verification-")).resolve()
        )
        if self.workspace.is_relative_to(self.checkout) or self.checkout.is_relative_to(
            self.workspace
        ):
            raise ValueError("workspace ownership cannot overlap checkout or records")
        if workspace is not None:
            self.workspace.mkdir(parents=True, exist_ok=False)

        def identify(command: list[str]) -> str:
            try:
                result = subprocess.run(
                    command,
                    cwd=self.checkout if self.checkout.exists() else self.workspace,
                    text=True,
                    capture_output=True,
                )
                return (
                    result.stdout.strip() if result.returncode == 0 else "unavailable"
                )
            except OSError as error:
                return f"unavailable: {error}"

        self.identity: dict[str, object] = {
            "source_revision": identify(["git", "rev-parse", "HEAD"]),
            "working_tree": identify(["git", "status", "--short"]),
            "platform": platform.platform(),
            "python": sys.version,
            "uv": identify(["uv", "--version"]),
            "invocation_command": [sys.executable, *sys.argv],
            "invocation_cwd": str(Path.cwd()),
        }
        self.records = (
            self.checkout
            / ".dev-records/verification"
            / f"{datetime.now(UTC):%Y%m%dT%H%M%SZ}-{str(self.identity['source_revision'])[:12]}-{uuid4().hex}"
        )
        self.records.mkdir(parents=True)
        print(f"WORKSPACE {self.workspace}", flush=True)
        print(f"RECORDS {self.records}", flush=True)
        (self.records / "logs").mkdir()
        (self.records / "identities").mkdir()
        self.commands: list[dict[str, object]] = []
        (self.records / "commands.json").write_text("[]\n")
        (self.records / "summary.json").write_text(
            json.dumps(
                {
                    **self.identity,
                    "workspace": str(self.workspace),
                    "verification_exit_code": None,
                    "cleanup": "not attempted",
                },
                indent=2,
            )
        )
        self.disposable: dict[Path, tuple[int, int] | None] = {}
        self.workspace_identity = (
            self.workspace.stat().st_dev,
            self.workspace.stat().st_ino,
        )

    def create_disposable(self, relative: str, *, create: bool = True) -> Path:
        """Exclusively create a disposable directory inside this workspace."""
        if Path(relative).is_absolute() or ".." in Path(relative).parts:
            raise ValueError("disposable ownership requires a relative child path")
        path = self.workspace / relative
        if (
            path == self.workspace
            or path.resolve() != path
            or not path.resolve().is_relative_to(self.workspace)
        ):
            raise ValueError("disposable ownership rejects redirected paths")
        if path.exists() or path.is_symlink():
            raise FileExistsError(path)
        if create:
            path.mkdir(parents=True, exist_ok=False)
        self.disposable[path] = (
            (path.stat().st_dev, path.stat().st_ino) if create else None
        )
        return path

    def remove_disposable(self, path: Path) -> None:
        """Remove only a registered, unchanged directory and reserve its next creation."""
        if path not in self.disposable or path.resolve() != path:
            raise ValueError(f"ownership changed: {path}")
        if (
            self.workspace.stat().st_dev,
            self.workspace.stat().st_ino,
        ) != self.workspace_identity:
            raise ValueError(f"workspace ownership changed: {path}")
        if path.exists():
            if (path.stat().st_dev, path.stat().st_ino) != self.disposable[path]:
                raise ValueError(f"ownership changed: {path}")
            shutil.rmtree(path)
        self.disposable[path] = None

    def preserve(self, source: Path, name: str) -> None:
        """Retain explicitly selected evidence with its checksum."""
        if Path(name).name != name:
            raise ValueError("evidence name must be a basename")
        data = source.read_bytes()
        (self.records / "identities" / name).write_bytes(data)
        (self.records / "identities" / (name + ".sha256")).write_text(
            hashlib.sha256(data).hexdigest() + "\n"
        )

    def run(
        self, stage: str, command: list[str], cwd: Path, env: dict[str, str]
    ) -> str:
        """Record each command and both output streams before propagating failure."""
        print(f"STAGE {stage}: {command!r} cwd={cwd}", flush=True)
        result: subprocess.CompletedProcess[str] | None = None
        spawn_error: OSError | None = None
        try:
            result = subprocess.run(
                command, cwd=cwd, env=env, text=True, capture_output=True
            )
        except OSError as error:
            spawn_error = error
        for path, expected in self.disposable.items():
            if expected is None and path.is_dir() and path.resolve() == path:
                self.disposable[path] = (path.stat().st_dev, path.stat().st_ino)
        log = f"logs/{len(self.commands):03d}.log"
        stdout = result.stdout if result is not None else ""
        stderr = result.stderr if result is not None else str(spawn_error)
        (self.records / log).write_text(
            f"{command!r} cwd={cwd}\nstdout:\n{stdout}\nstderr:\n{stderr}",
            encoding="utf-8",
        )
        self.commands.append(
            {
                "stage": stage,
                "command": command,
                "cwd": str(cwd),
                "returncode": result.returncode if result is not None else None,
                "log": log,
            }
        )
        (self.records / "commands.json").write_text(json.dumps(self.commands, indent=2))
        if spawn_error is not None:
            raise spawn_error
        assert result is not None
        if result.returncode:
            raise RuntimeError(
                f"{stage}: exit {result.returncode}; records={self.records}\n{result.stdout}{result.stderr}"
            )
        return result.stdout

    def finish(self, verification_code: int) -> int:
        """Persist the outcome and release disposable paths after successful checks."""
        retained = verification_code != 0 or self.keep_workspace
        summary: dict[str, object] = {
            **self.identity,
            "verification_exit_code": verification_code,
            "cleanup": "retained" if retained else "pending",
            "workspace": str(self.workspace),
        }
        summary_path = self.records / "summary.json"
        try:
            summary_path.write_text(json.dumps(summary))
        except OSError as error:
            print(
                f"RECORD FAIL: {error}; workspace={self.workspace}; records={self.records}",
                file=sys.stderr,
            )
            return verification_code or 1
        errors: list[str] = []
        if not retained:
            for path, expected in self.disposable.items():
                try:
                    if (
                        self.workspace.stat().st_dev,
                        self.workspace.stat().st_ino,
                    ) != self.workspace_identity or path.resolve() != path:
                        raise ValueError(f"ownership changed: {path}")
                    if not path.exists():
                        continue
                    if (path.stat().st_dev, path.stat().st_ino) != expected:
                        raise ValueError(f"ownership changed: {path}")
                    shutil.rmtree(path)
                except (OSError, ValueError) as error:
                    errors.append(str(error))
                    print(
                        f"CLEANUP FAIL: {error}; workspace={self.workspace}; records={self.records}",
                        file=sys.stderr,
                    )
            summary["cleanup"] = "failed" if errors else "complete"
        summary["cleanup_errors"] = errors
        try:
            summary_path.write_text(json.dumps(summary))
        except OSError as error:
            print(
                f"RECORD FAIL: {error}; workspace={self.workspace}; records={self.records}",
                file=sys.stderr,
            )
            return verification_code or 1
        return verification_code or (1 if errors else 0)
