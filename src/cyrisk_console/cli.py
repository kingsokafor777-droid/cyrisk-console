"""Local development-server command; no deployment or daemon claim."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

import uvicorn


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the local synthetic Cyrisk Console reference."
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args(argv)
    uvicorn.run("cyrisk_console.app:create_app", host=args.host, port=args.port, factory=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
