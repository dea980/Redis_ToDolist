import React, { useEffect, useState } from "react";

const API_URL = "http://localhost:8000";

function App() {
  const [todos, setTodos] = useState([]);
  const [task, setTask] = useState("");

  useEffect(() => {
    fetch(`${API_URL}/todos`)
      .then((res) => res.json())
      .then((data) => setTodos(Object.entries(data)));
  }, []);

  const addTodo = () => {
    const todoId = `todo-${Date.now()}`;
    fetch(`${API_URL}/todos/${todoId}?task=${task}`, { method: "POST" })
      .then(() => setTodos([...todos, [todoId, task]]));
  };

  return (
    <div>
      <h1>To-Do List</h1>
      <input value={task} onChange={(e) => setTask(e.target.value)} />
      <button onClick={addTodo}>Add Task</button>
      <ul>
        {todos.map(([id, task]) => (
          <li key={id}>{task}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
