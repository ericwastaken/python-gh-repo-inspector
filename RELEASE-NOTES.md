# Release Notes

## [1.0.0] - 2026-02-22

Initial release of **GitHub Repo Inspector**, a robust Python-based command-line tool for systematic retrieval of metadata, commit history, and repository structure from GitHub.

### Features

- **Multi-Repo Analysis**: Process a list of repositories in a single run using a simple YAML configuration.
- **Detailed Commit Extraction**: Retrieve comprehensive commit logs including SHA hashes, author information, timestamps, subject lines, and full commit messages.
- **File-Level Detail**: Track every filename changed across all retrieved commits for in-depth analysis of repository evolution.
- **Flexible Date Filtering**: Support for natural language ranges like "last 90 days", "this year", or specific explicit date spans (powered by Pendulum).
- **Regex Author Filtering**: Narrow down results to specific contributors using powerful regular expressions.
- **README Retrieval**: Automatically download and store the primary README file for each inspected repository.
- **Structured CSV Output**: Exports all commit and file data into clean, analysis-ready CSV files (`commit_messages.csv` and `commit_files.csv`).
- **Configuration Persistence**: Automatically saves the specific configuration used for each repository in its output directory for reproducibility.
- **Secure Authentication**: Integrated support for GitHub Personal Access Tokens (PAT) via environment variables or `.env` files, enabling higher API rate limits.
- **Comprehensive Logging**: Detailed console output with configurable log levels (DEBUG, INFO, WARNING, ERROR) to track progress and troubleshoot issues.

### Technical Specifications

- **Python Version**: Requires Python 3.11 or higher.
- **Dependencies**: Built on top of `click`, `requests`, `pyyaml`, `pendulum`, and `python-dotenv`.
- **Installation**: Includes automated bootstrap scripts for both standard and developer (editable) installations.
