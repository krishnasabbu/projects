import React, { createContext, useContext, useReducer } from 'react';
import { Button, Paper, Typography } from '@mui/material';
import useLogs from 'app/hooks/useLogs';

// LogsDisplay component
export const LogsDisplay = () => {
  const { logs, addLog } = useLogs();

  return (
    <Paper style={{ padding: '16px', margin: '16px' }}>
      {logs.map((log, index) => (
        <Typography key={index}>{log}</Typography>
      ))}
    </Paper>
  );
};

export default useLogs;
