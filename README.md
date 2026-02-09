# MindOverMatter

A lightweight CLI task manager backed by SQLite. Create, read, delete, and list tasks from the terminal with optional JSON output.

## Features
- Create tasks with titles, content, optional shorthand titles, and tags
- Read tasks by ID with plain or JSON output
- Delete tasks with confirmation
- List tasks by status with a configurable limit
- SQLite storage (default: `instance/mom.db`)

## Requirements
- Python 3.14+
- Dependencies: `typer`, `rich`

## Installation
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -e .
```

## Configuration
The database path can be overridden with an environment variable:
```bash
set MOM_DATABASE_URL=C:\path\to\mom.db
```
If not set, the database defaults to `instance/mom.db` in the project directory.

## Usage
Run the CLI:
```bash
python mom.py --help
```

### Add a task
```bash
python mom.py add "Task content" "Task title" --shorthand-title shorty --tags work,urgent
```

### Read a task
```bash
python mom.py read <task_id>
python mom.py read <task_id> --output json
```

### Delete a task
```bash
python mom.py delete <task_id>
```

### List tasks
```bash
python mom.py list --status active --limit 10
python mom.py list --output json
```

## Status Values
- `active`
- `pending`
- `completed`

## Notes
- `update`, `search`, and `mark` commands are stubbed and not implemented yet.
- Duplicate tasks (same content/title/shorthand, depending on DB constraints) return an error.

## Project Layout
- `mom.py`: CLI entrypoint
- `lib/db.py`: SQLite data access layer
- `lib/utils.py`: shared enums and task model
- `main.py`: placeholder entrypoint

## License
MIT
