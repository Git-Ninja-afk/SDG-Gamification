import React, { useState } from 'react';

function App() {
  const [email, setEmail] = useState('demo@example.com');
  const [password, setPassword] = useState('demo123');

  const handleLogin = (e) => {
    e.preventDefault();
    console.log('Login clicked with:', email, password);
    alert('Login clicked! Email: ' + email);
  };

  return (
    <div style={{ 
      fontFamily: 'Arial, sans-serif', 
      maxWidth: '400px', 
      margin: '100px auto', 
      padding: '20px', 
      border: '2px solid #007bff',
      borderRadius: '8px',
      boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
    }}>
      <h1 style={{ textAlign: 'center', color: '#333' }}>🌍 Gamify SDG</h1>
      <p style={{ textAlign: 'center', color: '#666' }}>Login to start playing!</p>
      
      <form onSubmit={handleLogin}>
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>Email:</label>
          <input 
            type="email" 
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{ 
              width: '100%', 
              padding: '10px', 
              border: '1px solid #ddd',
              borderRadius: '4px',
              boxSizing: 'border-box'
            }}
            required
          />
        </div>
        
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>Password:</label>
          <input 
            type="password" 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ 
              width: '100%', 
              padding: '10px', 
              border: '1px solid #ddd',
              borderRadius: '4px',
              boxSizing: 'border-box'
            }}
            required
          />
        </div>
        
        <button type="submit" style={{ 
          width: '100%', 
          padding: '12px', 
          background: '#007bff', 
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '16px',
          fontWeight: 'bold'
        }}>
          Login
        </button>
      </form>

      <div style={{ marginTop: '20px', padding: '15px', background: '#f0f0f0', borderRadius: '4px' }}>
        <p style={{ margin: '0 0 10px 0', fontWeight: 'bold' }}>✅ Demo Credentials:</p>
        <p style={{ margin: '5px 0' }}>📧 Email: demo@example.com</p>
        <p style={{ margin: '5px 0' }}>🔐 Password: demo123</p>
      </div>
    </div>
  );
}

export default App;
