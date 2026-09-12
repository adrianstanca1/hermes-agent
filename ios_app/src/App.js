import React, { useState } from 'react';
import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input) return;
    const userMsg = { role: 'user', text: input };
    setMessages([...messages, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://85.190.100.68:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: input }),
      });
      const data = await response.json();
      setMessages(prev => [...prev, { role: 'ai', text: data.response }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'ai', text: 'Error connecting to VPS.' }]);
    }
    setLoading(false);
  };

  return (
    <div className="app-container">
      <header className="app-header">Hermes AI Agent</header>
      <div className="chat-window">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>{msg.text}</div>
        ))}
        {loading && <div className="message ai">Thinking...</div>}
      </div>
      <div className="input-area">
        <input value={input} onChange={(e) => setInput(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && sendMessage()} placeholder="Ask your agent..." />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}
export default App;
