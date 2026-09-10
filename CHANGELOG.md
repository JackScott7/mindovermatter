# Changelog

## [0.3.0] - 2026-09-10

### Added

- The `mark` command to set a task's status to `active`, `pending`, or `completed` using its task ID or shorthand title.
- Feedback when the task requested by the `mark` command cannot be found.

### Changed

- Updating a task's status now refreshes its last-updated timestamp.
- Plain-text task output now includes the task's status.

## [0.2.0] - 2026-09-10

### Added

- Task search by content, shorthand title, or full title using the `search` command.
- Search results displayed in a table with task IDs, titles, tags, and last-updated timestamps.
- Feedback for empty search queries and searches with no matching tasks.

### Changed

- Reduced the task-list loading delay from 0.4 seconds to 0.1 seconds.
