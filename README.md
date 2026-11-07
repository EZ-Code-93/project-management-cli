# Project Management CLI

A robust, Object-Oriented command-line application built in Python for managing projects, collaborating with teams, tracking tasks, and generating automated progress risk assessments using a local AI client. 

## Features

- **Relational Object Model Configuration:** Designed using robust class composition patterns where users dynamically claim ownership of project registries, which in turn manage nested collections of task models.
- **Data Protection:** Implements encapsulation boundaries across all models using Python's `@property` decorators for protected attribute getters and setters.
- **Beautiful Terminal Interface:** Features color-coded diagnostic messaging, customized horizontal layouts, and nested task sub-tables powered by `rich`.
- **Local AI Analysis Engine:** Leverages a local model via Ollama to generate instantaneous project risk evaluations and suggested action timelines based on active task strings.
- **Isolated Testing Harness:** Equipped with an automated `pytest` test suite configured with isolated temporal mock directory parameters to guarantee stable code transitions.

---

## Architecture & Libraries Used

### Built-in Libraries (Standard Library)
These modules come bundled with Python and do not require external tracking installation procedures:
- `argparse` – Manages terminal entry route switching, sub-command routing, and flags validation.
- `datetime` – Handles automatic execution timestamp generation using ISO format string markers.
- `json` – Manages serialization and persistence transitions between active object arrays and the text mock DB layer.
- `os` & `sys` – Safely builds directory paths relative to runtime script locations to avoid subfolder path resolution crashes.

### External Libraries (Third-Party Dependencies)
These modules are managed via `Pipfile` tracking parameters:
- `rich` – Drives terminal rendering engines, column layouts, and custom diagnostic panels.
- `ollama` – Connects the application execution layer to your local large language model instance.
- `pytest` – Automates comprehensive testing via temporal directory sandboxing structures.

---

## Getting Started: Fork, Clone & Setup Instructions

Follow these instructions to clone the repository and configure your local workspace.

### Prerequisites
Ensure your local system has the following software packages installed:
1. **Python 3.10+**
2. **Pipenv** (`pip install pipenv`)
3. **Ollama Desktop Client** (Downloaded and running in the background)

### 1. Fork & Clone the Repository
First, fork this repository to your personal GitHub account. Then open your machine's terminal window and run:
```bash
git clone https://github.com
cd project-management-cli
```

### 2. Install Project Dependencies via Pipenv
Build the isolated project virtual environment wrapper and install the required dependencies by executing:
```bash
pipenv install --dev
```

### 3. Pull the Local AI Model
Ensure your local Ollama desktop client is active in the background, then pull the required open-source model instance to your device:
```bash
ollama pull llama3
```

---

## Usage Guide & Command Line Operations

Activate your virtual environment environment path framework before triggering commands:
```bash
pipenv shell
```

### 1. Create a User Profile
Before creating projects, initialize a user registry target:
```bash
python main.py create-user --name "Ezra"
```

### 2. Initialize a Project Record
Create a project by passing a title, short description, a valid future due date string (`YYYY-MM-DD`), and the target user:
```bash
python main.py create-project --title "Core Refactor" --desc "Implementing property decorators" --due "2026-11-30" --user "Ezra"
```

### 3. Add Nested Tasks
Add granular tasks inside the project context boundary by referencing its matching integer index ID:
```bash
python main.py add-task --project-id 1 --desc "Verify variable protection mapping gates"
```

### 4. Progress Task Status Categories
Advance active checklist elements through workflow states (`Pending`, `In Progress`, `Complete`):
```bash
python main.py update-task --project-id 1 --task-id 1 --status "In Progress"
```

### 5. Display the Project Board
Render a fully formatted grid layout mapping all stored projects alongside their nested checklist subsets:
```bash
python main.py list
```

### 6. Generate an AI Progress Risk Assessment
Pass full text data blocks to Ollama to return a high-level status summary outline panel:
```bash
python main.py analyze --project-id 1
```

---

## Running Automated Tests

To run the full suite of unit test files without writing fake test logs into your actual `data/project_data.json` storage file, trigger the `pytest` engine from your root folder location:

```bash
pytest
```
