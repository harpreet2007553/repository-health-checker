import argparse
import json
import sys
from pathlib import Path

from repo_health_checker.checker import check_repository


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Check repository health for essential files and directories."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=None,
        help="Path to the repository to check (prompts if omitted).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format.",
    )
    parser.add_argument(
        "--fail-under",
        type=float,
        default=None,
        metavar="PERCENT",
        help="Minimum health score percentage (0-100) required to exit successfully.",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    if args.path is not None:
        repo_path = args.path.strip()
    else:
        repo_path = input("Enter the repository path: ").strip()

    target = Path(repo_path)
    if not target.is_dir():
        if args.json:
            print(json.dumps({"error": f"Folder '{repo_path}' does not exist."}))
        else:
            print("Error: That folder does not exist.")
        return 1

    results = check_repository(repo_path)
    found = sum(results.values())
    total = len(results)
    score = (found / total) * 100 if total else 0
    missing_items = [
        filename
        for filename, exists in results.items()
        if not exists
    ]

    if args.json:
        report = {
            "path": str(target.resolve()),
            "score": round(score, 2),
            "passed": found,
            "total": total,
            "results": results,
            "missing": missing_items,
        }
        print(json.dumps(report, indent=2))
    else:
        print("\nRepository Health Report")
        print("-" * 30)

        for filename, exists in results.items():
            status = "FOUND" if exists else "MISSING"
            print(f"{filename}: {status}")

        print("-" * 30)

        if missing_items:
            print("Missing items: " + ", ".join(missing_items))
        else:
            print("Great job! All checks passed.")

        print(f"Health score: {score:.0f}% ({found}/{total} checks passed)")

    if args.fail_under is not None and score < args.fail_under:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
