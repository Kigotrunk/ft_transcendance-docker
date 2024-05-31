import axios from "axios";
import { createContext, useState, useEffect } from "react";
import { useHistory } from 'react-router-dom'

const AuthContext = createContext();

const AuthProvider = ({ children }) => {

	
  const [refreshToken, setRefreshToken] = useState(localStorage.getItem('refreshToken'));

  const history = useHistory();
  
  const loginUser = async (event) => {
    event.preventDefault();
    setError('');
    try {
        const response = await axios.post('http://localhost:8000/api/login/', {
            email: username,
            password: password,
        });
        console.log(response);
        setAccessToken(response.data.access);
        setRefreshToken(response.data.refresh);
        history.push('/');
    }
    catch (err) {
        setError('Invalid Credentials');
    }
  };

  useEffect(() => {
    if (accessToken) {
      axios.defaults.headers.common['Authorization'] = 'Bearer ' + accessToken;
      localStorage.setItem('accessToken', accessToken);
    } else {
      delete axios.defaults.headers.common["Authorization"];
      localStorage.removeItem('accessToken')
    }
  }, [accessToken]);

  const contextData = {
    user:user,
  }

  return(
    <AuthContext.Provider value={contextData} >
      {children}
    </AuthContext.Provider>
  )
}

export default AuthProvider;