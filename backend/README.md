# Atim Backend

This is the backend for the Atim AI Assistant, which enhances and develops the Nilotic Network blockchain.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set up environment variables by creating a `.env` file in the backend directory:

```
SECRET_KEY=your-secret-key-for-jwt
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
MAIL_DEFAULT_SENDER=noreply@example.com
GITHUB_TOKEN=your-github-token
```

3. Run the Flask API:

```bash
python app.py
```

This will start the API server at http://localhost:5000

## Atim's Core Functionality

Atim's core functionality is in `atim.py`. This script:

1. Analyzes the Nilotic Network codebase for issues
2. Suggests fixes for those issues
3. Creates pull requests with the fixes
4. Learns from feedback provided through the frontend

To run Atim's code analysis:

```bash
python atim.py
```

## API Endpoints

### Authentication

- `POST /api/register`: Register a new user
- `GET /api/verify?token=<token>`: Verify user email
- `POST /api/login`: Login user
- `GET /api/user`: Get current user

### Issues

- `GET /api/issues`: Get all issues
- `GET /api/issues/<issue_id>`: Get a specific issue

### Pull Requests

- `GET /api/prs`: Get all pull requests
- `GET /api/prs/<pr_id>`: Get a specific pull request
- `POST /api/prs/<pr_id>/feedback`: Submit feedback on a pull request

### Chat

- `GET /api/chat`: Get chat messages
- `POST /api/chat`: Send a chat message

### Kanban

- `GET /api/kanban`: Get items for the Kanban board

## Database

The backend uses SQLite for data storage. The database file is `db.sqlite` and the tables are created automatically when the app starts.

Tables:
- `users`: User accounts
- `email_tokens`: Email verification tokens
- `issues`: Detected issues in the codebase
- `pull_requests`: GitHub pull requests created by Atim
- `feedback`: User feedback on pull requests
- `chat_messages`: Messages between users and Atim

## Dependencies

See `requirements.txt` for a full list of dependencies.
