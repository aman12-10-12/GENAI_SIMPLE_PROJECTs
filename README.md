# Resume Analysis

A Python script that compares a resume with a job description using the Groq API.

## Setup

1. Install [uv](https://docs.astral.sh/uv/).
2. Install the project dependencies:

   ```bash
   uv sync
   ```

3. Create a local environment file and add your API key:

   ```bash
   cp .env.example .env
   ```

4. Put the resume PDF in the project root as `Aman_Raj.pdf`.
5. Run the analysis:

   ```bash
   uv run python analyzing_resume.py
   ```

The `.env` file, virtual environment, and PDF input are intentionally excluded
from Git. Never put API keys or personal resume documents in a commit.

## Project files

- `analyzing_resume.py` — resume analysis script
- `pyproject.toml` and `uv.lock` — project dependencies and locked versions
- `.python-version` — Python version used by the project
- `.env.example` — placeholder for required local environment variables
