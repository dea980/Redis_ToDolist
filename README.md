# Redis Todo List and Chat Application

This is a full-stack application featuring a todo list and real-time chat functionality, built with FastAPI, Redis, and React.

## Features

- Todo List Management (Create, Read, Update, Delete)
- Real-time Chat System
- Redis-based Data Storage
- WebSocket Communication
- Multiple Chat Rooms Support

## Prerequisites

- Python 3.7+
- Node.js and npm
- Redis Server
- Docker and Docker Compose (optional)

## Project Structure

```
Redis_ToDolist/
├── todo_app-backend/     # FastAPI Backend
│   ├── app/
│   │   ├── routers/     # API routes
│   │   ├── main.py      # Main application
│   │   └── redis.py     # Redis configuration
│   ├── Dockerfile
│   └── requirements.txt
├── todo-frontend/       # React Frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   └── App.js       # Main React component
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

## Installation & Setup

### Using Docker Compose (Recommended)

1. Clone the repository
2. Run the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. Access the application at http://localhost:3000

### Manual Setup

#### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd todo_app-backend
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd todo-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```

#### Redis Setup

Ensure Redis server is running locally on default port (6379), or update the connection settings in `todo_app-backend/app/redis.py`

## Usage

1. Access the application at http://localhost:3000
2. Use the navigation buttons at the top to switch between Todo List and Chat features
3. Todo List:
   - Add new tasks
   - Edit existing tasks
   - Delete tasks
   - View Redis debug data
4. Chat:
   - Enter your username
   - Enter a room ID (or use default)
   - Start chatting in real-time
   - Messages are persisted in Redis

## API Endpoints

### Todo Endpoints
- `GET /todos` - Get all todos
- `POST /todos/{todo_id}` - Create a new todo
- `PUT /todos/{todo_id}` - Update a todo
- `DELETE /todos/{todo_id}` - Delete a todo

### WebSocket Endpoints
- `ws://localhost:8000/ws/chat/{room_id}` - Chat WebSocket connection
- `ws://localhost:8000/ws` - Todo list WebSocket connection

## Development

The application uses WebSocket connections for real-time updates in both the todo list and chat features. The frontend automatically reconnects if the connection is lost.

## Troubleshooting

1. If the frontend can't connect to the backend:
   - Ensure the backend server is running
   - Check if the ports (8000 for backend, 3000 for frontend) are available
   - Verify the WebSocket connection URLs in the frontend code

2. If Redis connection fails:
   - Verify Redis server is running
   - Check Redis connection settings in `todo_app-backend/app/redis.py`

3. For Docker-related issues:
   - Ensure Docker and Docker Compose are installed and running
   - Try rebuilding the containers: `docker-compose up --build`