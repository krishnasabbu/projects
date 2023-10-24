import React, { useContext,  useReducer } from 'react';

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

interface LogsContextData {
  logs: string,
  addLog: (message: string) => void;
}

// Initial state
const initialState = [];

// Context setup
const LogsContext = React.createContext<LogsContextData | undefined>(undefined);

// LogsProvider component
export default function LogsProvider ({ children }) {
  const [logs, dispatch] = useReducer(logsReducer, initialState);

  const addLog = (message: string) => {
    dispatch(addLogAction(message));
  };

  const contextValue: LogsContextData = {
    logs,
    addLog
  };


  return <LogsContext.Provider value={contextValue}>{children}</LogsContext.Provider>;
};

export const useLogs = () => useContext(LogsContext);