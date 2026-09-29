# helper

## 1. Project Overview

Project name: Uni_helper

Platform: Windows Desktop Application

Primary language: Python

UI framework: PySide6

Database: SQLite

ORM: SQLAlchemy

AI provider: Google Gemini API

Testing: Pytest

Version: V1 (MVP)

Uni_helper is an AI-powered university learning assistant designed to help students organize subjects, study course materials, understand concepts, assess their knowledge, identify knowledge gaps, and track learning progress.

The application must be developed incrementally, module by module.

## 2. V1 Modules

V1 consists of exactly four main modules:

1. Core & Dashboard
2. Subjects & Materials
3. AI Learning
4. Assessment & Progress

Each module must have clearly defined responsibilities and boundaries.

Do not implement all modules at once.

Do not introduce additional major product modules without explicit approval.

## 3. Architecture Principles

Use a modular monolith architecture.

Follow SOLID principles, especially the Single Responsibility Principle.

Separate the application into:

* Presentation Layer: PySide6 UI.
* Application Layer: use cases and orchestration.
* Domain Layer: entities, business rules, and domain logic.
* Infrastructure Layer: database, file system, and external API integrations.

Dependency rules:

* The UI must not directly execute database queries.
* Business logic must not depend on PySide6 widgets.
* Domain logic must not depend on external API providers.
* Infrastructure implementations must be accessed through clearly defined interfaces.
* Avoid circular dependencies.
* Avoid unnecessary abstractions and premature optimization.

## 4. Coding Standards

* Use Python type hints.
* Write clear, descriptive names.
* Keep functions and classes focused on one responsibility.
* Prefer small, cohesive modules.
* Follow PEP 8.
* Add docstrings to public interfaces and complex logic.
* Avoid duplicated business logic.
* Handle errors explicitly.
* Do not use global mutable state.
* Do not place business logic inside UI widgets.
* Use dependency injection where it improves testability.

## 5. Database Rules

* Use SQLite with SQLAlchemy.
* Keep database models separate from UI code.
* Use repositories or equivalent data-access abstractions.
* Keep database sessions properly managed.
* Define relationships and constraints explicitly.
* Use migrations when schema evolution requires them.
* Do not delete or reset existing user data without explicit approval.

## 6. Gemini API Rules

* Use a dedicated GeminiService abstraction.
* Keep Gemini API integration separate from application and domain logic.
* Never hardcode API keys.
* Never commit API keys or secrets.
* Load credentials from secure configuration.
* Handle network errors, rate limits, and invalid responses.
* Do not block the UI thread during API requests.
* Keep prompts and response parsing organized.
* Clearly distinguish source-grounded information from AI-generated content.
* Do not claim that a student has a knowledge gap without supporting assessment evidence.

## 7. UI/UX Rules

* Design for Windows desktop.
* Use a simple, modern, minimal interface.
* Use a consistent color palette, spacing, typography, and component style.
* Keep navigation predictable.
* Avoid unnecessary visual clutter.
* Display loading, success, empty, and error states.
* Keep the interface responsive during long-running tasks.
* Reuse shared UI components where appropriate.

## 8. Testing Rules

* Use Pytest.
* Add unit tests for business logic.
* Add integration tests for database and service interactions.
* Mock external Gemini API calls in automated tests.
* Test error handling and edge cases.
* Do not mark a feature complete until its relevant tests pass.
* Run regression tests after integrating a module.

## 9. Git Rules

* Inspect the current Git status before modifying files.
* Never overwrite unrelated user changes.
* Do not delete files without a clear reason and approval.
* Do not commit, push, reset, or rewrite Git history without explicit authorization.
* Keep changes focused on the current module.
* Summarize modified files and important decisions after each task.

## 10. Development Workflow

For every module:

1. Inspect the existing repository and its instructions.
2. Review the current architecture and dependencies.
3. Define module responsibilities and acceptance criteria.
4. Propose the implementation plan.
5. Implement only the approved scope.
6. Add and run tests.
7. Review code for SRP, SOLID, security, and maintainability.
8. Integrate with existing modules.
9. Run regression tests.
10. Report completion status, test results, and remaining issues.

Do not proceed to the next module until the current module meets its acceptance criteria.

If requirements are ambiguous or a change could affect existing architecture, stop and ask for clarification.

## 11. Scope Control

* Do not add unrequested features.
* Do not replace the selected technology stack without approval.
* Do not introduce microservices.
* Do not build a web application or mobile application as part of V1.
* Do not introduce unnecessary dependencies.
* Do not refactor unrelated code during a module implementation.

## 12. Completion Report

At the end of each task, report:

* What was implemented.
* Which files were created or modified.
* Which tests were executed and their results.
* Known limitations and unresolved issues.
* Whether the module meets its acceptance criteria.
* Recommended next step.

Never claim a test passed unless it was actually executed and passed.
