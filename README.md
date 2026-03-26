# Coding-Agent

A lightweight coding agent that uses function-calling to safely interact with files and run Python scripts inside a workspace.

## What this project does

This repository implements a small CLI agent that:

1. Accepts a natural-language prompt.
2. Lets an LLM decide whether to call a predefined function.
3. Executes only supported local functions (for file listing, file reading/writing, and Python execution).
4. Returns the function result back to the model to generate a final answer.

It is designed as a practical learning project for controlled tool use with an AI assistant.

## Repository structure

- `main.py`: CLI entry point and orchestration loop.
- `call_function.py`: Routes model-requested function calls to Python implementations.
- `config.py`: Centralized configuration.
- `functions/`:
  - `get_files_info.py`: List files and metadata.
  - `get_file_content.py`: Read file contents.
  - `write_file.py`: Write/create files.
  - `run_python.py`: Run Python files safely in workspace context.
- `calculator/`: Example target project used by the agent.
- `test_run_python_file.py`: Tests for Python execution behavior.
- `README.md`: Project documentation (this file).

## How it works

1. You run the CLI with a prompt, for example:
   - “run tests.py”
   - “what files are in the root?”
   - “create a new README.md file with the contents '# calculator'”
2. The model may produce a function call.
3. `call_function.py` validates and executes the call against local functions.
4. The result is fed back into the conversation for a final response.

## Prerequisites

- Python 3.11+ (recommended)
- [`uv`](https://docs.astral.sh/uv/) installed
- Required environment variables/API access for your selected LLM provider (if applicable in your local setup)

## Setup

```bash
# from repo root
uv sync