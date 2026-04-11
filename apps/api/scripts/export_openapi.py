import json
import sys
from pathlib import Path

from app.asgi import app


def export_openapi_schema(output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    _ = output_path.write_text(
        json.dumps(app.openapi_schema.to_schema(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python scripts/export_openapi.py <output-path>")

    export_openapi_schema(Path(sys.argv[1]))


if __name__ == "__main__":
    main()
