# Webhook Repository

Flask application that receives GitHub webhook events and displays them in a UI.

## Features

- Receives GitHub webhooks for Push, Pull Request, and Merge events
- Stores events in MongoDB
- Real-time UI with 15-second polling
- Dockerized application

## Prerequisites

- Docker & Docker Compose
- ngrok (for local development)
- GitHub account

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/webhook-repo.git
cd webhook-repo
```

### 2. Start the application

```bash
docker-compose up --build -d
```

The application will run on `http://localhost:5001`

### 3. Expose local server using ngrok

```bash
ngrok http 5001
```

Copy the ngrok HTTPS URL (e.g., `https://abc123.ngrok.io`)

### 4. Configure GitHub Webhook

1. Go to your `action-repo` repository on GitHub
2. Navigate to **Settings** → **Webhooks** → **Add webhook**
3. Configure:
   - **Payload URL**: `https://YOUR-NGROK-URL.ngrok.io/webhook`
   - **Content type**: `application/json`
   - **Let me select individual events**: Select "Pushes" and "Pull requests"
   - **Active**: ✅ Checked
4. Click **Add webhook**

## Usage

Visit `http://localhost:5001` to view the events dashboard.

Events are automatically refreshed every 15 seconds.

## Event Formats

**Push Event:**

```
"Author" pushed to "branch" on 1st April 2021 - 9:30 PM UTC
```

**Pull Request Event:**

```
"Author" submitted a pull request from "source-branch" to "target-branch" on 1st April 2021 - 9:00 AM UTC
```

**Merge Event:**

```
"Author" merged branch "source-branch" to "target-branch" on 2nd April 2021 - 12:00 PM UTC
```

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Frontend**: HTML, CSS, JavaScript
- **Containerization**: Docker, Docker Compose
- **Package Manager**: uv

## API Endpoints

- `POST /webhook` - Receives GitHub webhook events
- `GET /events` - Returns list of events (JSON)
- `GET /` - UI dashboard

## Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up --build -d
```

## MongoDB Access

```bash
# Enter MongoDB shell
docker exec -it webhook-repo-mongo-1 mongosh

# View events
use github_webhooks
db.events.find().pretty()
```

## Project Structure

```
webhook-repo/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image configuration
├── docker-compose.yml    # Docker services configuration
├── .dockerignore         # Docker ignore file
├── .gitignore           # Git ignore file
├── README.md            # Documentation
└── templates/
    └── index.html       # UI dashboard
```
