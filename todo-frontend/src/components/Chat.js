import React, { useState, useEffect, useRef } from 'react';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [roomId, setRoomId] = useState('default-room');
  const [username, setUsername] = useState(`User-${Math.floor(Math.random() * 1000)}`);
  const wsRef = useRef(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    connectWebSocket();
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [roomId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const connectWebSocket = () => {
    const ws = new WebSocket(`ws://localhost:8000/ws/chat/${roomId}`);
    wsRef.current = ws;

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'messages') {
        setMessages(data.messages);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
      console.log('WebSocket connection closed');
      // Attempt to reconnect after 5 seconds
      setTimeout(connectWebSocket, 5000);
    };
  };

  const sendMessage = (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    const messageData = {
      username,
      content: newMessage,
      room_id: roomId
    };

    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(messageData));
      setNewMessage('');
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <div style={{ marginBottom: '20px' }}>
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Your username"
          style={{ marginRight: '10px', padding: '5px' }}
        />
        <input
          value={roomId}
          onChange={(e) => setRoomId(e.target.value)}
          placeholder="Room ID"
          style={{ padding: '5px' }}
        />
      </div>

      <div 
        style={{ 
          height: '400px', 
          border: '1px solid #ccc', 
          overflowY: 'auto',
          padding: '10px',
          marginBottom: '20px',
          borderRadius: '5px'
        }}
      >
        {messages.map((msg, index) => (
          <div 
            key={index}
            style={{
              marginBottom: '10px',
              textAlign: msg.username === username ? 'right' : 'left'
            }}
          >
            <div
              style={{
                display: 'inline-block',
                maxWidth: '70%',
                padding: '8px 15px',
                borderRadius: '15px',
                backgroundColor: msg.username === username ? '#007bff' : '#e9ecef',
                color: msg.username === username ? 'white' : 'black'
              }}
            >
              <div style={{ fontSize: '0.8em', marginBottom: '3px' }}>
                {msg.username}
              </div>
              <div>{msg.content}</div>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={sendMessage} style={{ display: 'flex' }}>
        <input
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type your message..."
          style={{ flex: 1, marginRight: '10px', padding: '10px', borderRadius: '5px' }}
        />
        <button 
          type="submit"
          style={{
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default Chat;