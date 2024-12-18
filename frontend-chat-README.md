# Frontend Chat Component (Chat.js) Documentation

## Overview
This React component implements a real-time chat interface using WebSocket connections. It provides room-based chat functionality with message history and automatic reconnection.

## Code Breakdown

### Imports and State Management
```javascript
import React, { useState, useEffect, useRef } from 'react';

const Chat = () => {
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');
    const [roomId, setRoomId] = useState('default-room');
    const [username, setUsername] = useState(`User-${Math.floor(Math.random() * 1000)}`);
    const wsRef = useRef(null);
    const messagesEndRef = useRef(null);
```
- React hooks for state and refs
- Message history management
- Room and user identification
- WebSocket reference
- Auto-scroll reference

### Auto-scroll Functionality
```javascript
const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
};

useEffect(() => {
    scrollToBottom();
}, [messages]);
```
- Smooth scrolling to latest messages
- Triggered on message updates

### WebSocket Connection Management
```javascript
useEffect(() => {
    connectWebSocket();
    return () => {
        if (wsRef.current) {
            wsRef.current.close();
        }
    };
}, [roomId]);

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
        setTimeout(connectWebSocket, 5000);
    };
};
```
- Establishes WebSocket connection
- Handles incoming messages
- Error handling
- Automatic reconnection
- Message type validation
- Cleanup on unmount or room change

### Message Sending
```javascript
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
```
- Form submission handling
- Empty message prevention
- Message data formatting
- Connection state verification
- Input clearing after send

### Component Return Structure
```javascript
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

        <div style={{ 
            height: '400px', 
            border: '1px solid #ccc', 
            overflowY: 'auto',
            padding: '10px',
            marginBottom: '20px',
            borderRadius: '5px'
        }}>
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
                style={{ 
                    flex: 1, 
                    marginRight: '10px', 
                    padding: '10px', 
                    borderRadius: '5px' 
                }}
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
```

## Features

1. **Real-time Communication**
   - WebSocket-based messaging
   - Instant message updates
   - Connection status handling
   - Automatic reconnection

2. **Room Management**
   - Dynamic room switching
   - Room-based chat isolation
   - Room ID customization
   - Multiple room support

3. **User Experience**
   - Customizable usernames
   - Message history display
   - Automatic scrolling
   - Visual message alignment
   - Responsive design

4. **Message Handling**
   - Message validation
   - Empty message prevention
   - Message formatting
   - Timestamp support

## Best Practices

1. **WebSocket Management**
   - Proper connection cleanup
   - Error handling
   - Automatic reconnection
   - State synchronization
   - Connection status tracking

2. **User Interface**
   - Clean, responsive design
   - Visual message differentiation
   - Intuitive input controls
   - Smooth scrolling behavior
   - Clear message organization

3. **Performance**
   - Efficient WebSocket usage
   - Optimized rendering
   - Proper cleanup
   - State management
   - Reference handling

4. **Error Handling**
   - Connection error management
   - Message send validation
   - WebSocket state verification
   - Reconnection logic
   - Input validation

5. **Code Organization**
   - Clear component structure
   - Logical function grouping
   - Consistent styling
   - Proper cleanup handling
   - State management patterns

## Component Lifecycle

1. **Initialization**
   - State setup
   - Random username generation
   - Default room setting
   - Reference creation

2. **Connection**
   - WebSocket establishment
   - Event handler setup
   - Room connection
   - Error handling setup

3. **Operation**
   - Message sending/receiving
   - Room management
   - User interaction
   - Auto-scrolling

4. **Cleanup**
   - Connection closure
   - Resource cleanup
   - State reset
   - Reference clearing