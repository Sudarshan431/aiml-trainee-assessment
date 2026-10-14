# Task 5 — FlowSync Database Code

## Project Overview

FlowSync is an AI-powered employee productivity platform developed using Java 21 and Spring Boot. Its PostgreSQL database supports organization management, project planning, task tracking, communication, attendance, leave management, notifications, and audit logging.

This task showcases the database schema and migration code used by the FlowSync backend.

## Technology Stack

- **Database:** PostgreSQL
- **Schema migrations:** Flyway
- **Backend:** Java 21, Spring Boot 3.5.3
- **Persistence:** Spring Data JPA and Hibernate
- **Infrastructure:** Docker Compose

## Database Design

The database uses relational tables, UUID primary keys, foreign-key relationships, unique constraints, and indexes to maintain data integrity and support efficient queries.

### Main Functional Areas

| Area | Tables and Purpose |
|---|---|
| Organization | `companies`, `departments`, `teams`, `users` |
| Authentication | `user_roles`, `refresh_tokens`, `password_reset_tokens`, `email_verification_tokens` |
| Project management | `projects`, `project_members`, `sprints`, `tasks` |
| Task collaboration | `task_labels`, `task_comments`, `task_attachments`, `task_checklist_items`, `task_dependencies`, `task_history` |
| Communication | `chat_rooms`, `chat_memberships`, `chat_messages`, `message_receipts` |
| Employee operations | `attendance_entries`, `leave_requests`, `leave_balances`, `holidays`, `calendar_events` |
| Platform services | `notifications`, `stored_files`, `audit_logs` |

## Database Implementation

The initial schema is maintained as a Flyway migration:

`src/main/resources/db/migration/V1__init_schema.sql`

The migration includes:

- Table definitions and column data types.
- Primary and foreign keys.
- Required fields and unique constraints.
- Indexes for selected lookup and filtering operations.
- UUID generation using PostgreSQL's `pgcrypto` extension.
- Timestamp fields and common auditing/versioning columns.
- Referential actions such as cascading deletes where explicitly configured.

## Database Migration

FlowSync integrates Flyway to version and manage database schema changes. The initial migration establishes the tables and relationships required by the application.

To start the project and its configured infrastructure, use the instructions in the original repository:

```bash
docker compose up --build
```

Review the environment configuration before running the application. Database credentials and other secrets should be configured appropriately.

## Source Code

- **FlowSync repository:** https://github.com/Sudarshan431/flowsync
- **Initial database migration:** https://github.com/Sudarshan431/flowsync/blob/main/src/main/resources/db/migration/V1__init_schema.sql

## Deliverables

This assessment folder contains the database migration source code, project documentation, and a link to the complete FlowSync repository.