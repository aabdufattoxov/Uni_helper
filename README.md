# Uni_helper

**Project Purpose:** An AI-powered university learning assistant designed to help students organize subjects, study course materials, understand concepts, assess their knowledge, identify knowledge gaps, and track learning progress.

**Current Version:** V1 (MVP)  
**Platform:** Windows Desktop Application  

## Technology Stack
- **Language:** Python 3
- **UI Framework:** PySide6
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **AI Provider:** Google Gemini API
- **Testing:** Pytest

## Current Modules
- Module 1: Core & Dashboard (Implemented)
- Module 2: Subjects & Materials (Subject management in progress; Materials pending)
- Module 3: AI Learning (Pending)
- Module 4: Assessment & Progress (Pending)

### Module 2: Subject management

The current Module 2 increment supports creating, listing, editing, and deleting
subjects. Each subject has a required name and an optional description. Subject
records are stored in the per-user SQLite database. Material management is not
implemented yet.

## Basic Development Setup

1. **Environment Setup:**
   Ensure you have Python installed. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   python -m uni_helper.main
   ```

4. **Run Tests:**
   ```bash
   pytest
   ```
