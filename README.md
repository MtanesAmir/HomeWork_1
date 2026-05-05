# HomeWork_1

A professional, enterprise-ready Python package constructed in strict accordance with the **Guidelines for Writing Professional Software at the Highest Level of Excellence**.

---

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Installation Instructions](#installation-instructions)
- [Usage Guide](#usage-guide)
- [Configuration](#configuration)
- [Lints and Tests](#lints-and-tests)
- [Contribution Guidelines](#contribution-guidelines)
- [License](#license)

---

## Architecture Overview

This project implements a **Layered SDK Architecture** as specified in the guidelines:

1. **SDK Layer (`src/homework_1/sdk`)**: The sole public entrypoint for external applications, CLI scripts, or third-party integrations.
2. **Domain Layer (`src/homework_1/services`)**: Implements business logic and processes core data algorithms.
3. **Infrastructure/Shared Layer (`src/homework_1/shared`)**: Provides configuration loading, version tracking, and API rate limit shielding.

---

## Project Structure

Conforms fully to section **2.4 Recommended Project Structure**:

```text
HomeWork_1/
├── src/                      # Source code
│   ├── homework_1/           # Primary Python package
│   │   ├── __init__.py
│   │   ├── sdk/              # SDK layer interface
│   │   │   ├── __init__.py
│   │   │   └── sdk.py
│   │   ├── services/         # Business logic domain
│   │   │   └── __init__.py
│   │   ├── shared/           # Shared cross-cutting utilities
│   │   │   ├── __init__.py
│   │   │   ├── gatekeeper.py # API gatekeeper / rate limiter
│   │   │   ├── config.py     # Configuration loader
│   │   │   └── version.py    # Version tracking
│   │   └── constants.py
│   └── main.py
├── tests/                    # Automated test suites
│   ├── unit/
│   └── integration/
├── docs/                     # Mandatory documents
│   ├── PRD.md                # Product Requirements Document
│   ├── PLAN.md               # Technical Architecture Plan
│   └── TODO.md               # Progress tracking
├── config/                   # External config templates
│   ├── setup.json
│   └── rate_limits.json
└── pyproject.toml            # Standard project and linter configs
```

---

## Installation Instructions

### Prerequisites
- **Python 3.10+** is required.
- **uv** package manager (Recommended) or standard `pip`.

### Step-by-Step Installation

1. **Clone the repository**:
   ```bash
   git clone git@github.com:MtanesAmir/HomeWork_1.git
   cd HomeWork_1
   ```

2. **Set up a Virtual Environment**:
   Using `uv` (Recommended):
   ```bash
   uv venv
   source .venv/bin/activate
   ```
   Using standard Python:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   Using `uv`:
   ```bash
   uv sync
   ```
   Using standard `pip`:
   ```bash
   pip install -e .[dev]
   ```

4. **Configure Environment Variables**:
   Duplicate `.env-example` to `.env` and populate actual credentials:
   ```bash
   cp .env-example .env
   ```

---

## Usage Guide

### Running the Main Entry Point
To verify the complete setup and bootstrap execution, run:
```bash
python3 src/main.py
```

---

## Configuration

All configuration details are fully isolated from the codebase (no hardcoded settings):
* **Application configurations** are stored in `config/setup.json`.
* **API rate limits** are handled dynamically in `config/rate_limits.json`.
* **Credentials and Keys** are parsed via environment variables (`.env`).

---

## Lints and Tests

### Linting with Ruff
To check lint rules, style guide compliance, and syntax correctness, run:
```bash
ruff check src
```

### Running Tests with Coverage
To execute test cases and verify that coverage is above the **85% threshold**:
```bash
pytest
```

---

## Contribution Guidelines

1. Maintain full code modularity: Keep logical features strictly separated.
2. Ensure that all source code files **do not exceed the 150-line limit** (Section 3.2).
3. Every class, module, and function must include detailed **Docstrings** explaining its purpose.

---

## License

This project is licensed under the **MIT License** - see the [docs/PLAN.md](file:///Users/amirmt/Desktop/ME/Me/MSC-ComputerScience/2025-B/agent%20AI/hw1/HomeWork_1/docs/PLAN.md) or contact Dr. Segal Yoram for licensing questions.
