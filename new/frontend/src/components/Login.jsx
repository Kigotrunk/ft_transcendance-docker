import React, { useState } from 'react';
import axios from 'axios';

const Login = ({ setAccessToken }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/api/login/', {
                'email': username,
                'password': password,
            });
            console.log(response);
            setAccessToken(response.data.access);
            localStorage.setItem('accessToken', response.data.access);
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + response.data.access;
            setError('');
        } catch (err) {
            setError('Invalid Credentials');
        }
    };

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Username:</label>
                    <input type="text" value={username} onChange={(e) => setUsername(e.target.value)}/>
                </div>
                <div>
                    <label>Password:</label>
                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)}/>
                </div>
                <button type="submit">Login</button>
            </form>
            {error && <p>{error}</p>}
        </div>
    );
};

export default Login;
