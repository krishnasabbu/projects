import React from "react";

interface AuthContextData {
    token: string,
    authenticate: (userName: string, password: string) => void;
}

const AuthContext = React.createContext<AuthContextData | undefined>(undefined);

export default function AuthProvider ({ children}) {

    const [token, setToken] = React.useState('');

    const authenticate = (userName: string, password: string) => {
        console.log("logging");
        setToken(userName);
    }

    const contextValue: AuthContextData = {
        token,
        authenticate
    };

    return(
        <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
    );
};

export const useAuth = () => React.useContext(AuthContext);