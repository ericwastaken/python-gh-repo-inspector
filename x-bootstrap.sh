#!/bin/bash
# x-bootstrap.sh - Production install

install_package() {
    set -e
    echo "Ensuring required directories exist..."
    if [ ! -d "./config" ]; then
        mkdir "./config"
        echo "Created ./config directory"
    else
        echo "./config directory already exists"
    fi
    if [ ! -d "./output" ]; then
        mkdir "./output"
        echo "Created ./output directory"
    else
        echo "./output directory already exists"
    fi

    echo "Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo "Installing package..."
    pip install .
}

if (install_package); then
    source .venv/bin/activate
    
    echo "Checking installation..."
    if command -v gh-repo-inspector >/dev/null 2>&1; then
        echo "Successfully installed gh-repo-inspector"
        gh-repo-inspector --help
    else
        echo "Installation failed: gh-repo-inspector not found in PATH"
        if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then exit 1; else return 1; fi
    fi

    if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
        if [[ -t 0 ]]; then
            echo ""
            echo "Entering virtual environment. Type 'exit' to leave."
            exec $SHELL
        else
            echo ""
            echo "Installation complete. To activate the virtual environment, run:"
            echo "source .venv/bin/activate"
        fi
    else
        echo "Virtual environment is now active."
    fi
else
    echo "Bootstrap failed."
    if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then exit 1; else return 1; fi
fi
