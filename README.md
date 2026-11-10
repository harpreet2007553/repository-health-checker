# Repository Health Checker

A beginner-friendly Python tool that checks the basic health of a software repository by looking for important files and directories and calculating a health score.

## Features

- Checks whether `README.md` exists.
- Checks whether `LICENSE` exists.
- Checks whether `.gitignore` exists.
- Checks whether the `src/` directory exists.
- Checks whether the `tests/` directory exists and is non-empty.
- Lists missing files and directories in the report.
- Displays a repository health score based on the checks passed.
- Supports both interactive prompts and command-line arguments.
- Supports `--json` machine-readable output and `--fail-under` thresholds for CI/CD workflows.

## Requirements

- Python 3.10 or later
- Git (for cloning the repository)

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/sAKshiiSYS/repository-health-checker.git
cd repository-health-checker
```

### 2. Install the project

```bash
py -m pip install -e ".[dev]"
```

### 3. Run the checker

You can run the checker using the installed console script:

```bash
# Run interactively (prompts for repository path)
repo-health-checker

# Or provide the repository path directly
repo-health-checker path/to/repo

# Output JSON report
repo-health-checker path/to/repo --json

# Enforce a minimum health score threshold (useful in CI)
repo-health-checker path/to/repo --fail-under 80
```

Alternatively, you can run it via Python directly:

```bash
py -m repo_health_checker.cli path/to/repo
```

### 4. Run the tests

```bash
py -m pytest
```

## Project Structure

```text
repository-health-checker/
├── src/
│   └── repo_health_checker/
│       ├── __init__.py
│       ├── cli.py
│       └── checker.py
├── tests/
│   ├── test_checker.py
│   └── test_cli.py
├── .gitignore
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml
└── README.md
```

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before making changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

##Testing 
just checking if github app is working or not
