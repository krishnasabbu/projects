import React, { createContext,  useReducer } from 'react';

// Action types
const ADD_LOG = 'ADD_LOG';

// Action creator
const addLogAction = (message) => ({
  type: ADD_LOG,
  payload: message
});

// Reducer function
const logsReducer = (state, action) => {
  switch (action.type) {
    case ADD_LOG:
      return [...state, action.payload];
    default:
      return state;
  }
};

// Initial state
const initialState = [];

// Context setup
const LogsContext = createContext();

// LogsProvider component
export const LogsProvider = ({ children }) => {
  const [logs, dispatch] = useReducer(logsReducer, initialState);

  const addLog = (message) => {
    dispatch(addLogAction(message));
  };

  return <LogsContext.Provider value={{ logs, addLog }}>{children}</LogsContext.Provider>;
};

export default LogsContext;