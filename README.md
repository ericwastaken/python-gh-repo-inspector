# GitHub Repo Inspector

A robust Python-based command line tool to systematically retrieve metadata, commit history, and repository structure from GitHub. 

`gh-repo-inspector` allows you to analyze multiple repositories at once, extract specific commit details, download README files, and filter data by author and date range—all through a simple YAML configuration.

## Key Features

- **Multi-Repo Analysis:** Process a list of repositories in a single run.
- **Commit History Extraction:** Retrieve detailed commit logs including author, date, subject line, and full message.
- **File-Level Detail:** Track every filename changed across all retrieved commits.
- **Flexible Date Filtering:** Support for natural language ranges like "last 90 days", "this year", or specific date spans.
- **Regex Author Filtering:** Narrow down results to specific contributors using powerful regular expressions.
- **README Retrieval:** Automatically download and store the primary README file for each repository.
- **Structured CSV Output:** Exports all commit and file data into clean, analysis-ready CSV files.
- **Secure Authentication:** Integrated support for GitHub Personal Access Tokens via environment variables or `.env` files.

## Prerequisites

- **Python:** 3.11 or higher
- **GitHub Account:** A [Personal Access Token (PAT)](#authentication-and-rate-limits) is highly recommended to avoid strict API rate limits.

## Installation

### Quick Start

For a quick and automated installation, you can use the provided bootstrap script. This will create a virtual environment, install dependencies, and set up the package.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ericwastaken/gh-repo-inspector.git
   cd gh-repo-inspector
   ```

2. **Run the bootstrap script:**
   ```bash
   chmod +x x-bootstrap.sh
   ./x-bootstrap.sh
   ```

### Manual Installation

If you prefer to set up your environment manually:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ericwastaken/gh-repo-inspector.git
   cd gh-repo-inspector
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the package:**
   ```bash
   pip install .
   ```

## Authentication and Rate Limits

### Why use a Personal Access Token (PAT)?

GitHub's API imposes strict rate limits on unauthenticated requests. If you run this tool without a token, you are 
limited to **60 requests per hour** per IP address. For tools like `gh-repo-inspector` that may need to make multiple 
calls per repository (to fetch commits and file details), you will likely hit this limit very quickly.

By using a Personal Access Token (PAT), your limit is increased to **5,000 requests per hour**, which is usually more 
than enough for scanning dozens of repositories.

### How to generate a GitHub PAT

1.  **Log in to GitHub:** Go to [github.com](https://github.com).
2.  **Open Settings:** Click your profile photo in the top-right corner and select **Settings**.
3.  **Developer Settings:** Scroll down on the left sidebar and click **Developer settings**.
4.  **Personal Access Tokens:** Click **Personal access tokens**, then select **Fine-grained tokens**.
5.  **Generate Token:** Click **Generate new token**.
6.  **Configure Token:**
    *   **Token name:** Give your token a descriptive name (e.g., `gh-repo-inspector`).
    *   **Expiration:** Set an expiration date (e.g., 90 days).
    *   **Resource owner:** Select your username (or the organization if applicable).
    *   **Repository access:** 
        *   Choose **Public Repositories (read-only)** if you only need to inspect public repos.
        *   Choose **All repositories** or **Only select repositories** if you need to inspect private ones.
    *   **Permissions:**
        *   Open **Repository permissions**.
        *   Set **Contents** to **Read-only** (required to fetch READMEs and commit details).
        *   *Note: **Metadata** is automatically set to Read-only.*
7.  **Generate & Copy:** Click **Generate token** at the bottom of the page.
8.  **Save Securely:** Copy the token immediately. **GitHub will not show it to you again.**

### Setup in the Project

To use your token with `gh-repo-inspector`:

1.  **Recommended:** Create a custom `.env` file inside the `./config` directory. This directory is excluded from source control by default, keeping your credentials safe.
    ```bash
    cp template.env config/my-project.env
    ```
2.  Edit the new file and paste your token:
    ```env
    GITHUB_TOKEN=github_pat_your_token_here
    ```

**Note:** You can then specify your environment file using the `--env` flag:
```bash
gh-repo-inspector --config config/my-config.yaml --outputDirectory ./output --env config/my-project.env
```

## Development

If you're looking to contribute or modify the tool, use the developer installation.

### Quick Start for Developers

The developer bootstrap script sets up the package in **editable mode**, allowing changes to the source code to be reflected immediately without re-installing.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ericwastaken/gh-repo-inspector.git
   cd gh-repo-inspector
   ```

2. **Run the developer bootstrap script:**
   ```bash
   chmod +x x-bootstrap-developer.sh
   ./x-bootstrap-developer.sh
   ```

### Manual Developer Install

For a manual developer setup:

1. **Clone and enter the directory:**
   ```bash
   git clone https://github.com/ericwastaken/gh-repo-inspector.git
   cd gh-repo-inspector
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the package in editable mode:**
   ```bash
   pip install -e .
   ```

## Configuration

The tool relies on a YAML configuration file to define which repositories to inspect and what data to extract. It is recommended to keep these files in the `./config` directory.

### Sample `config.yaml`

```yaml
repos:
  - url: https://github.com/ericwastaken/gh-repo-inspector
    getMainReadme: true
    getAllCommitMessages: true
    getAllCommitFilenames: true
    authorFilter: "^Eric"
    dateRange: "last 90 days"
  - url: https://github.com/psf/requests
    getMainReadme: false
    getAllCommitMessages: true
    getAllCommitFilenames: false
    dateRange: "2023-01-01 to 2023-12-31"
```

### Configuration Options

| Option | Type | Description |
| :--- | :--- | :--- |
| `url` | String | The full URL of the GitHub repository. |
| `getMainReadme` | Boolean | If `true`, downloads the repository's `README.md`. |
| `getAllCommitMessages` | Boolean | If `true`, extracts commit metadata to `commit_messages.csv`. |
| `getAllCommitFilenames` | Boolean | If `true`, extracts changed filenames to `commit_files.csv`. |
| `authorFilter` | String | (Optional) Regex pattern to filter commits by author name. |
| `dateRange` | String | (Optional) Date range for commit retrieval (e.g., "last 30 days", "this year", "YYYY-MM-DD to YYYY-MM-DD"). |

## Usage

Run the tool by specifying the configuration file and the desired output directory. It is recommended to keep your configuration files in the `./config` directory and redirect all output to the `./output` directory, as both are excluded from source control.

```bash
gh-repo-inspector --config config/my-config.yaml --outputDirectory ./output --logLevel INFO
```

### CLI Arguments

- `--config`: **(Required)** Path to your YAML configuration file.
- `--outputDirectory`: **(Required)** Path where the extracted data will be saved.
- `--env`: Path to an arbitrary `.env` file containing `GITHUB_TOKEN`.
- `--logLevel`: Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`). Defaults to `INFO`.

## Output Structure

The tool creates a sub-directory for each repository within your specified `outputDirectory`. It is recommended to use the `./output` directory, which is excluded from source control.

```text
output/
├── gh-repo-inspector/
│   ├── README.md
│   ├── commit_messages.csv
│   └── commit_files.csv
└── requests/
    └── commit_messages.csv
```

### CSV Formats

**`commit_messages.csv`**
- `commit_hash`: Full SHA-1 hash.
- `author_date`: ISO-8601 timestamp of the commit.
- `author_name`: Name of the commit author.
- `subject_line`: The first line of the commit message.
- `full_message`: The complete commit message body.

**`commit_files.csv`**
- `commit_hash`: SHA-1 hash connecting the file to a commit.
- `filename`: The path of the file that was modified.

## Supported Date Ranges

The `dateRange` field in your configuration file is powered by [Pendulum](https://pendulum.eustace.io/) and supports several formats:

- **Relative:** `last 7 days`, `last 30 days`, `last 365 days`
- **Fixed:** `this year`
- **Explicit Span:** `2023-01-01 to 2023-06-30`
- **Single Date:** `2024-01-01` (retrieves from that date until now)
- **Default:** If omitted, it defaults to the `last 30 days`.

## Logging

Logs are printed to the console to help you track progress and identify issues (like rate limiting or private repo access errors). Use `--logLevel DEBUG` for verbose output including API request details.
