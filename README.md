# Playground

A sandbox repository for experimenting with Python code and scientific libraries. So far, it includes:

- **Type Checking Demo** (`match_case.py`):

  - Demonstrates Python's structural pattern matching and type checking using dataclasses.

- **Beta-binomial Distribution Notebook** (`beta_bin.ipynb`):

  - Demonstrates Bayesian analysis of binomial processes using the beta-binomial distribution, including how to
    determine the upper threshold for the expected number of new trials needed to achieve a given confidence level.

- **Experimental Code** (`experimental/`):

  - Contains notebooks and scripts for experiments.

- **Preselection/Post-selection Epic Plan** (`docs/preselection.md`):

  - Implementation plan, requirements, and technical overview for preselection and post-selection features in the
    compiler and runtime.
  - Details on MoSCoW prioritization, implementation order, and JIRA ticket mapping.
  - Clarified likelihood formula notation in the decoder section, including Bayesian modeling for shot success rates and
    confidence intervals.
  - Overview of future extensions for multi-state measurements and active reset.

- **Complex Pydantic Parsing Notebook** (`complex_pydantic_parsing.ipynb`):

  - Demonstrates advanced usage of Pydantic for parsing lists of complex numbers.
  - Shows how to serialize and deserialize complex number lists to and from JSON using Pydantic models.
  - Includes examples of validating and parsing both complex and real numbers, handling mixed input types, and custom
    JSON representations.

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
