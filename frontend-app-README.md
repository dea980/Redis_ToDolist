# Frontend App Component (App.js) Documentation

## Overview
This is the main React component that manages the todo list application and chat functionality. It handles state management, API interactions, and view switching between todos and chat.

## Code Breakdown

### Imports and Constants
```javascript
import React, { useEffect, useState } from "react";
import Chat from "./components/Chat";

const API_URL = "http://localhost:8000";
```
- React and necessary hooks
- Chat component
- Backend API URL constant

### State Management
```javascript
const [activeView, setActiveView] = useState('todos');
const [todos, setTodos] = useState([]);
const [task, setTask] = useState("");
const [editingId, setEditingId] = useState(null);
const [editTask, setEditTask] = useState("");
const [debugData, setDebugData] = useState([]);
```
- **activeView**: Controls view switching (todos/chat)
- **todos**: Stores todo list items
- **task**: New task input value
- **editingId**: Currently editing todo ID
- **editTask**: Editing task input value
- **debugData**: Redis debugging information

### Data Fetching
```javascript
useEffect(() => {
    fetchTodos();
    fetchDebugData();
}, []);
```
- Loads initial data on component mount
- Fetches todos and debug data

### Todo Operations

#### Fetch Todos
```javascript
const fetchTodos = async () => {
    try {
        const response = await fetch(`${API_URL}/todos`);
        if (!response.ok) {
            throw new Error(`Failed to fetch todos: ${response.statusText}`);
        }
        const data = await response.json();
        const formattedTodos = Object.entries(data.todos || {}).map(([key, value]) => ({
            id: key,
            task: value,
        }));
        setTodos(formattedTodos);
    } catch (error) {
        console.error("Error fetching todos:", error);
    }
};
```
- Fetches todos from backend
- Formats response data
- Updates todos state
- Handles errors

#### Add Todo
```javascript
const addTodo = async () => {
    if (!task.trim()) return;
    const todoId = `todo-${Date.now()}`;
    try {
        const response = await fetch(`${API_URL}/todos/${todoId}?task=${encodeURIComponent(task)}`, { 
            method: "POST" 
        });
        if (!response.ok) {
            throw new Error(`Failed to add todo: ${response.statusText}`);
        }
        setTask("");
        fetchTodos();
        fetchDebugData();
    } catch (error) {
        console.error("Error adding todo:", error);
    }
};
```
- Validates input
- Generates unique ID
- Creates new todo
- Refreshes data
- Clears input

#### Save Edit
```javascript
const saveEdit = (id) => {
    if (!editTask.trim()) {
        alert("Task cannot be empty.");
        return;
    }

    fetch(`${API_URL}/todos/${encodeURIComponent(id)}?task=${encodeURIComponent(editTask)}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Failed to update task");
            }
            return response.json();
        })
        .then(() => {
            setEditingId(null);
            setEditTask("");
            fetchTodos();
            fetchDebugData();
        })
        .catch((err) => console.error("Error updating todo:", err));
};
```
- Validates edit input
- Updates todo
- Resets edit state
- Refreshes data
- Handles errors

#### Delete Todo
```javascript
const deleteTodo = async (id) => {
    try {
        const response = await fetch(`${API_URL}/todos/${encodeURIComponent(id)}`, { 
            method: "DELETE" 
        });
        if (!response.ok) {
            throw new Error(`Failed to delete todo: ${response.statusText}`);
        }
        fetchTodos();
        fetchDebugData();
    } catch (error) {
        console.error("Error deleting todo:", error);
    }
};
```
- Deletes todo by ID
- Refreshes data
- Handles errors

### UI Components

#### View Switching Buttons
```javascript
<div style={{ marginBottom: "20px" }}>
    <button 
        onClick={() => setActiveView('todos')} 
        style={{ 
            padding: "10px 20px", 
            marginRight: "10px",
            backgroundColor: activeView === 'todos' ? '#007bff' : '#6c757d',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
        }}
    >
        Todo List
    </button>
    <button onClick={() => setActiveView('chat')}>Chat</button>
</div>
```
- Toggles between todo and chat views
- Visual feedback for active view

#### Todo List View
```javascript
{activeView === 'todos' ? (
    <>
        <h1>할 일 목록</h1>
        {/* Todo input and list */}
    </>
) : (
    <Chat />
)}
```
- Conditional rendering based on activeView
- Todo list or chat component

#### Todo Input
```javascript
<input
    value={task}
    onChange={(e) => setTask(e.target.value)}
    placeholder="할 일을 입력하세요..."
    style={{ padding: "10px", marginRight: "10px" }}
/>
<button onClick={addTodo}>Add Task</button>
```
- Input field for new todos
- Add button

#### Todo List
```javascript
<ul style={{ listStyle: "none", padding: "0" }}>
    {todos.map((todo) => (
        <li key={todo.id}>
            {editingId === todo.id ? (
                // Edit mode
            ) : (
                // Display mode
            )}
        </li>
    ))}
</ul>
```
- Maps through todos
- Conditional rendering for edit mode
- Edit and delete buttons

#### Debug Data Display
```javascript
<h2>Redis Debugging Data</h2>
<ul style={{ listStyle: "none", padding: "0", background: "#f4f4f4" }}>
    {debugData.map((data) => (
        <li key={data.id}>
            <strong>{data.id}:</strong> {data.task}
        </li>
    ))}
</ul>
```
- Shows Redis data
- Scrollable container
- Formatted display

## Styling

### Common Styles
- Clean, minimal design
- Consistent padding and margins
- Responsive layout
- Visual feedback for interactions

### Button Styles
```javascript
{
    padding: "10px 20px",
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer'
}
```

### List Styles
```javascript
{
    listStyle: "none",
    padding: "0",
    borderBottom: "1px solid #ccc"
}
```

## Best Practices

1. **State Management**
   - Centralized state
   - Clear update patterns
   - Proper error handling

2. **API Interactions**
   - Error handling
   - Loading states
   - Data validation

3. **User Experience**
   - Input validation
   - Visual feedback
   - Responsive design

4. **Code Organization**
   - Logical grouping
   - Clear naming
   - Consistent formatting

5. **Performance**
   - Efficient rendering
   - Proper cleanup
   - Optimized state updates