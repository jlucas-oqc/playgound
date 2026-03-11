# Playground

A sandbox repository for experimenting with Python code and scientific libraries. So far, it
includes:

- **Type Checking Demo** (`match_case.py`):

  - Demonstrates Python's structural pattern matching and type checking using dataclasses.

- **Beta-binomial Distribution Notebook** (`beta_bin.ipynb`):

  - Demonstrates Bayesian analysis of binomial processes using the beta-binomial distribution,
    including how to determine the upper threshold for the expected number of new trials needed to
    achieve a given confidence level.

- **Experimental Code** (`experimental/`):

  - Contains notebooks and scripts for experiments.

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management.

1. Clone the repository:

   ```bash
   git clone git@github.com:jlucas-oqc/playgound.git
   cd playground
   ```

1. Install dependencies:

   ```bash
   poetry install

   ```

1. Install pre-commit hooks:

   ```bash
   pre-commit install
   ```

### Pre-commit Hooks

This repository uses pre-commit hooks to maintain code quality. The following hooks are configured:

- **black**: Formats code to comply with the Black code style.
- **isort**: Sorts and organizes imports.
- **flake8**: Checks for style and programming errors.
- **mypy**: Performs static type checking.
- **trailing-whitespace**: Removes trailing whitespace from lines.
- **end-of-file-fixer**: Ensures files end with a newline.

## Usage

- **Run the type checking demo:**
  ```bash
  poetry run python match_case.py
  ```
- **Explore the beta-binomial notebook:**
  ```bash
  poetry run jupyter notebook beta_bin.ipynb
  ```
