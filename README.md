# Playground

A sandbox repository for experimenting with Python code and scientific libraries.

## Features

- **Type Checking Demo** (`match_case.py`):
  - Demonstrates Python's structural pattern matching and type checking using dataclasses.

- **Beta-binomial Distribution Notebook** (`beta_bin.ipynb`):
  - Demonstrates Bayesian analysis of binomial processes using the beta-binomial distribution.
  - Visualizes the probability mass function (PMF) and cumulative distribution function (CDF).
  - Calculates and plots confidence intervals for the expected number of successes.
  - Shows how to determine the upper threshold for the expected number of new trials needed to achieve a given confidence level.
  - Includes a brief explanation of the Bayesian perspective and the use of the Beta distribution as a conjugate prior.

- **Experimental Code** (`experimental/`):
  - Contains notebooks and scripts for experiments.

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management.

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd playground
   ```
2. Install dependencies:
   ```bash
   poetry install
   ```

## Usage

- **Run the type checking demo:**
  ```bash
  poetry run python match_case.py
  ```
- **Explore the beta-binomial notebook:**
  ```bash
  poetry run jupyter notebook beta_bin.ipynb
  ```
