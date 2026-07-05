# macabacus_assessment#

This is a basic FastAPI application that manages tasks using an in-memory list.

## Prerequisites

Before you start, ensure you have the following installed:

- Python 3.12 or higher
- uv (https://docs.astral.sh/uv/), poetry (https://python-poetry.org/), or other python virtual environment manager

## Cloning the App

Clone the repository:
   ```sh
   git clone git@github.com:andrewkettel/macabacus_assessment.git
   cd macabacus_assessment
   ```

## Installing the App

Create a virtual environment and install dependencies with uv
   ```sh
   uv sync
   ```
or with poetry:
   ```sh
   poetry install
   ```

## Running the App

Start the FastAPI Dev server:
   ```sh
   uv run fastapi dev
   ```
or with poetry:
   ```sh
   poetry run fastapi dev
   ```

## Running Unit Tests

Run the unit tests:
   ```sh
   uv run pytest
   ```
or with poetry:
   ```sh
   peotry run pytest
   ```
   
or to run the full lint and test with coverage
   ```sh
   uv run black . && uv run mypy . && uv run ruff check --fix && uv run pytest --cov
   ```
