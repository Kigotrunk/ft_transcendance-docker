import { createContext, useState } from "react";

const AuthContext = createContext();

function AuthProvider(props) {
  const [isLog, setIsLog] = useState(false);
  const [access, setAccess] = useState(null);

  const login = (access) => {
    setIsLog(true);
    setAccess(access);
  };

  const logout = () => {
    setIsLog(false);
    setAccess(null);
  };

  const value = {
    isLog,
    access,
    login,
    logout,
  };

  return <AuthContext.Provider value={value} {...props} />;
}

export { AuthContext, AuthProvider };
