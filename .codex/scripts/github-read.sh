#!/bin/sh
# Repository development helper. Usage: sh .codex/scripts/github-read.sh ENDPOINT
# Optional arguments: --paginate, --slurp, --jq EXPRESSION.
set -eu
fail() {
    printf '%s\n' "$1" >&2
    exit 2
}
[ "$#" -gt 0 ] || fail 'An endpoint is required.'
endpoint=$1
shift
# Only relative, literal repository paths; reject URLs, traversal and query strings.
case "$endpoint" in
    ''|/*|*[!a-zA-Z0-9_./-]*|*..*|*//*) fail 'Invalid repository endpoint.' ;;
esac
case "$endpoint" in
    issues|issues/*|pulls|pulls/*|actions/runs|actions/runs/*|actions/workflows|actions/workflows/*|releases|releases/*|commits|commits/*) ;;
    *) fail 'Unsupported repository read endpoint.' ;;
esac
# Validate every caller-supplied option before forwarding any of them.
validate_options() {
    while [ "$#" -gt 0 ]; do
        case "$1" in
            --paginate|--slurp) shift ;;
            --jq)
                [ "$#" -ge 2 ] || fail '--jq requires an expression.'
                shift 2
                ;;
            *) fail 'Only --paginate, --slurp and --jq are supported.' ;;
        esac
    done
}
validate_options "$@"
exec gh api --hostname github.com --method GET \
    "repos/jimthompson5802/agentic-ml/$endpoint" "$@"
