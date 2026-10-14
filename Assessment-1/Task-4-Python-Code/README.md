# CareerIQ — AI Career Intelligence Platform

CareerIQ is an AI-powered career intelligence platform that matches candidates with relevant jobs, explains skill gaps, and provides personalized learning paths through a grounded AI assistant. Recruiters can post jobs and review applicants, while candidates can upload resumes, evaluate their fit for different roles, and discover skills they need to develop.

**Core principle:** AI responses are grounded in data computed by CareerIQ. The language model does not directly query the database.

## Table of Contents

- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Design and Security Decisions](#design-and-security-decisions)
- [My Contributions](#my-contributions)
- [Testing and Verification](#testing-and-verification)
- [Current Limitations](#current-limitations)

## Key Features

### Career Intelligence and NLP/ML
- Resume and job description parsing.
- Skill extraction using a predefined skill taxonomy.
- Job matching using baseline, TF-IDF, and semantic approaches.
- Skill-gap analysis and job ranking.
- Prioritized skill gaps, learning recommendations, and personalized career plans.

### Recruitment Workflow
- Recruiters can post jobs and review applicants.
- Candidates can explore job matches and understand their suitability.
- Job application workflow for managing applications.

### AI Assistant and RAG
- Gemini-powered assistant using an OpenAI-compatible endpoint.
- Retrieval-augmented generation (RAG) over chunked job descriptions.
- Similarity-based retrieval with access-control filtering at query time.
- Conversation memory with message-count and approximate token-budget limits.
- Older conversation turns are condensed into short summaries.
- Users can delete their conversations, with ownership checks enforced by the backend.

### Agent Layer
- The model can request operations only through a fixed set of 10 read-only tools.
- Tool arguments are validated against strict schemas.
- Unknown argument keys are rejected.
- Loop and execution-time limits help constrain agent behavior.
- User identity comes from the authenticated login token, not model-generated output.

## Technology Stack

| Component | Technologies |
|---|---|
| Language | Python 3.12 |
| Backend | FastAPI |
| ORM and migrations | SQLAlchemy 2.x, Alembic |
| Database | PostgreSQL |
| Authentication | JWT, role-based access control |
| NLP/ML | Scikit-learn, TF-IDF, semantic matching |
| AI provider | Gemini through an OpenAI-compatible endpoint |
| Frontend | React, TypeScript, Vite, Tailwind CSS |
| Deployment | Docker |
| Testing | Python unit tests |

## Architecture

CareerIQ uses a layered backend architecture in which API routes call services, and services interact with repositories.

| Layer | Responsibilities |
|---|---|
| NLP/ML engine | Parses resumes and job descriptions, extracts skills, scores job matches, analyzes skill gaps, and ranks jobs. |
| Backend API | Exposes application endpoints and provides consistent structured error responses. |
| Authentication and security | Enforces JWT authentication, candidate/recruiter/admin roles, and resource ownership checks. |
| Career intelligence | Generates prioritized skill gaps, learning recommendations, career plans, and application workflows. |
| AI assistant | Integrates Gemini with retry and backoff behavior and distinguishes authentication errors from rate-limit errors. |
| RAG | Chunks job descriptions, retrieves relevant content by similarity, and applies document-access rules at query time. |
| Agent layer | Executes validated requests through a fixed set of read-only tools with loop and time limits. |
| Frontend | Provides job intelligence pages, assistant chat, and application views. |

### API Error Handling

The backend uses a consistent JSON error structure:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Description of the error",
    "request_id": "request-id"
  }
}
```

## Design and Security Decisions

### 1. Grounded AI Responses
The assistant relies on career data computed by the application. The model cannot directly query the database, helping keep application logic and data access under backend control.

### 2. Restricted Agent Capabilities
The agent has access to a fixed set of 10 read-only tools. There are no tools for arbitrary SQL execution, shell commands, URL access, or file access. Tool arguments are checked against strict schemas, and unknown keys are rejected.

### 3. Authentication and Ownership
The application supports three roles: candidate, recruiter, and admin. Ownership checks prevent users from accessing another user's protected data. Candidate identity is derived from the login token rather than model output.

### 4. Graceful Degradation
If Scikit-learn or the LLM provider is unavailable, the affected feature returns a structured HTTP 503 response while other application functionality can continue working.

Heavy ML imports are loaded lazily, and a cached Scikit-learn capability check helps the application start on restricted Windows environments where native extensions may be blocked.

### 5. Conversation Memory Limits
Conversation history is bounded by message count and an approximate token budget. Older turns are condensed into summaries to limit memory growth. Users can delete conversations, and only the conversation owner can perform owner-restricted operations.

## My Contributions

**Sudarshan Mali — System Design and Implementation**

I designed the system and developed CareerIQ in phases, using Claude Code as an AI pair-programmer.

- Built the NLP/ML engine for job matching, skill-gap analysis, recommendations, and training and evaluation scripts.
- Developed the backend foundation, including structured error handling, PostgreSQL integration, database migrations, and JWT-based role access.
- Built the React and TypeScript frontend.
- Implemented the job application workflow.
- Improved startup reliability on restricted Windows environments through lazy loading and a cached Scikit-learn capability check.
- Added career intelligence features, including skill-gap prioritization, learning recommendations, career plans, and the AI assistant.
- Migrated the assistant from OpenAI to Gemini and added resilience against service errors and timeouts.
- Implemented the RAG layer and the agent layer, including conversation memory limits, as part of CareerIQ 2.0.

## Testing and Verification

**Verified:** 133 unit tests pass.

The tests cover:
- Resume parsing and job matching logic.
- RAG chunking and document-access rules.
- Agent tools.
- LLM provider retry behavior.
- Conversation memory.

**Not yet verified:** The following have not been tested against live services in the development sandbox:
- A live Gemini API key.
- A real PostgreSQL database.
- The complete FastAPI application stack.

The passing unit tests should therefore not be interpreted as proof that all live integrations or end-to-end workflows have been verified.

## Current Limitations and Future Work

The following items are not yet implemented or complete:

- Real ML evaluation datasets.
- Background task processing.
- Metrics and health endpoints.
- CI/CD pipeline.
- Remaining security hardening.

These are areas for further development and validation.

## Project Status

CareerIQ has implemented its core career intelligence, backend, frontend, RAG, and agent capabilities. Its unit-tested components are verified, while live integrations, full-stack execution, and the remaining operational and security work still require validation.

