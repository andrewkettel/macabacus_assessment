# macabacus_assessment#

This is a basic FastAPI application that manages tasks using an in-memory list.

## Prerequisites

Before you start, ensure you have the following installed:

- Python 3.12 or higher
- uv (https://docs.astral.sh/uv/)

## Cloning the App

1. Clone the repository:
   ```sh
   git clone git@github.com:andrewkettel/macabacus_assessment.git
   cd macabacus_assessment
   ```

## Installing the App with uv

1. Create a virtual environment and install dependencies
   ```sh
   uv sync
   ```

## Running the App

1. Start the FastAPI Dev server:
   ```sh
   uv run fastapi dev
   ```

## Running Unit Tests

1. Run the unit tests:
   ```sh
   . .venv/bin/activate
   pytest
   ```
    or to run the full lint and test with coverage
   ```sh
   uv run black . && uv run mypy . && uv run ruff check --fix && uv run pytest --cov
   ```
