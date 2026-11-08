"""Native exception type used by the public serialization regression."""

class _ArrowError(Exception): ...

# Preserve the native export while keeping the local declaration's Error suffix.
ArrowException = _ArrowError
