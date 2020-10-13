import React from 'react';
import {createContext, useContext} from 'react';

export const AuthContext = createContext();

function AuthProvider(props) {
    const login = () => { };
    const register = () => { };
    const logout = () => { };

    return (
        <AuthContext.Provider value={{ login, logout, register }} {...props} />
    );
}

function useAuth() {
    return useContext(AuthContext);
}

export {AuthProvider, useAuth}