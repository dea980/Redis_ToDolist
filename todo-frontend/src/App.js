import React, { useEffect, useState } from "react";
import Chat from "./components/Chat";

const API_URL = "http://localhost:8000";

function App() {
  const [activeView, setActiveView] = useState('todos'); // 'todos' or 'chat'
  const [todos, setTodos] = useState([]); // 할 일 목록
  const [task, setTask] = useState(""); // 새로운 작업 입력 값
  const [editingId, setEditingId] = useState(null); // 수정 중인 작업 ID
  const [editTask, setEditTask] = useState(""); // 수정 중인 작업 내용
  const [debugData, setDebugData] = useState([]); // Redis Debugging Data (배열 형태)

  // 작업 불러오기
  useEffect(() => {
    fetchTodos();
    fetchDebugData(); // Redis Debugging Data 가져오기
  }, []);

  const fetchTodos = async () => {
    try {
      const response = await fetch(`${API_URL}/todos`);
      if (!response.ok) {
        throw new Error(`Failed to fetch todos: ${response.statusText}`);
      }
      const data = await response.json();
      console.log("Todos API Response:", data); // 디버깅용 로그
      const formattedTodos = Object.entries(data.todos || {}).map(([key, value]) => ({
        id: key,
        task: value,
      }));
      setTodos(formattedTodos);
    } catch (error) {
      console.error("Error fetching todos:", error);
    }
  };

  const fetchDebugData = async () => {
    try {
      const response = await fetch(`${API_URL}/debug/redis`);
      if (!response.ok) {
        throw new Error(`Failed to fetch debug data: ${response.statusText}`);
      }
      const data = await response.json();
      console.log("Debug Data API Response:", data); // 디버깅용 로그
      const formattedDebugData = Object.entries(data.debug_data || {}).map(([key, value]) => ({
        id: key,
        task: value,
      }));
      setDebugData(formattedDebugData);
    } catch (error) {
      console.error("Error fetching debug data:", error);
    }
  };

  // 작업 추가
  const addTodo = async () => {
    if (!task.trim()) return;
    const todoId = `todo-${Date.now()}`;
    try {
      const response = await fetch(`${API_URL}/todos/${todoId}?task=${encodeURIComponent(task)}`, { method: "POST" });
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

  // 작업 수정
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
        setEditingId(null); // 수정 모드 종료
        setEditTask(""); // 수정 입력 초기화
        fetchTodos(); // 목록 다시 불러오기
        fetchDebugData(); // Debug 데이터 업데이트
      })
      .catch((err) => console.error("Error updating todo:", err));
  };
  
  // 작업 삭제
  const deleteTodo = async (id) => {
    try {
      const response = await fetch(`${API_URL}/todos/${encodeURIComponent(id)}`, { method: "DELETE" });
      if (!response.ok) {
        throw new Error(`Failed to delete todo: ${response.statusText}`);
      }
      fetchTodos();
      fetchDebugData();
    } catch (error) {
      console.error("Error deleting todo:", error);
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
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
        <button 
          onClick={() => setActiveView('chat')} 
          style={{ 
            padding: "10px 20px",
            backgroundColor: activeView === 'chat' ? '#007bff' : '#6c757d',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          Chat
        </button>
      </div>

      {activeView === 'todos' ? (
        <>
          <h1>할 일 목록</h1>
          <input
            value={task}
            onChange={(e) => setTask(e.target.value)}
            placeholder="할 일을 입력하세요..."
            style={{ padding: "10px", marginRight: "10px" }}
          />
          <button onClick={addTodo} style={{ padding: "10px 20px" }}>
            Add Task
          </button>
          <ul style={{ listStyle: "none", padding: "0" }}>
            {todos.map((todo) => (
              <li key={todo.id} style={{ padding: "10px", borderBottom: "1px solid #ccc" }}>
                {editingId === todo.id ? (
                  <>
                    <input
                      value={editTask}
                      onChange={(e) => setEditTask(e.target.value)}
                      style={{ marginRight: "10px" }}
                    />
                    <button onClick={() => saveEdit(todo.id)}>Save</button>
                    <button onClick={() => setEditingId(null)}>Cancel</button>
                  </>
                ) : (
                  <>
                    {todo.task}
                    <button
                      onClick={() => {
                        setEditingId(todo.id);
                        setEditTask(todo.task);
                      }}
                      style={{ marginLeft: "10px" }}
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => deleteTodo(todo.id)}
                      style={{ marginLeft: "10px", color: "red" }}
                    >
                      Delete
                    </button>
                  </>
                )}
              </li>
            ))}
          </ul>

          {/* Redis Debugging Data */}
          <h2>Redis Debugging Data</h2>
          <ul style={{ listStyle: "none", padding: "0", background: "#f4f4f4", maxHeight: "300px", overflowY: "auto" }}>
            {debugData.map((data) => (
              <li key={data.id} style={{ padding: "10px", borderBottom: "1px solid #ccc" }}>
                <strong>{data.id}:</strong> {data.task}
              </li>
            ))}
          </ul>
        </>
      ) : (
        <Chat />
      )}
    </div>
  );
}

export default App;
