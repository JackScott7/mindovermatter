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
mom --help
```

### Add a task
```bash
mom add "Task content" "Task title" --shorthand-title shorty --tags work,urgent
```

### Read a task
```bash
mom read <task_id>
mom read <task_id> --output json
```

### Delete a task
```bash
mom delete <task_id>
```

### List tasks
```bash
mom list --status active --limit 10
mom list ''--output json
```

### Search for task(s)
```bash
mom search work
mom search todo
```

### Mark a task
```bash
mom mark completed todo
# 'todo' here is a short-title which you can set when creating the task
mom mark pending "2e00e64a-cd4b-4b95-b6d0-fff06eeaf0a0"
```

## Status Values
- `active`
- `pending`
- `completed`

## Notes
- Duplicate tasks (same content/title/shorthand, depending on DB constraints) return an error.

## License
Check out the here [LICENSE](LICENSE).
