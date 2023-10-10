import React, { useState } from 'react';
import { LogsDisplay } from './LogsDisplay';
import { LogsProvider } from 'app/contexts/LogsContext';
import { Fragment } from 'react';
import { Button, Paper, Typography } from '@mui/material';
import {
  Grid, styled, Box
} from '@mui/material';
import axios from 'axios';
import useLogs from 'app/hooks/useLogs';

const Analytics = () => {

  const [file, setFile] = useState(null);
  const { logs, addLog } = useLogs();

  
  const onFileChange = (event) => {
    console.log("file ==== "+event.target.files[0]);
    setFile(event.target.files[0]);
  };

  const onFileUpload = async () => {
 
      // Create an object of formData
      const formData = new FormData();

      // Update the formData object
      formData.append("file", file);
      formData.append("id", "1");

      // Details of the uploaded file
      console.log(file);

      // Request made to the backend api
      // Send formData object
      

      try {
        const response = await axios.post('http://localhost:8081/upload', formData);
        console.log(response);
        const intervalId = setInterval(() => {
          fetchData();
        }, 2000);
        
      } catch (error) {
        // Handle errors
        console.error(error);
      }

  };

  const fetchData = async () => {
    try {
      // Make your API call here
      const response = await fetch('http://localhost:8081/response');
      const data = await response.json();
      console.log(data.data);
      addLog(data.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const fileData = () => {
    console.log("file ==== "+file);
    if (file) {
        return (
            <div>
                <h2>File Details:</h2>
                <p>File Name: {file.name}</p>

                <p>File Type: {file.type}</p>

                <p>
                    Last Modified:{" "}
                    {file.lastModifiedDate ? file.lastModifiedDate.toDateString() : ""}
                </p>

            </div>
        );
    } else {
        return (
            <div>
            </div>
        );
    }
};

const ContentBox = styled(Box)(({ theme }) => ({
  display: 'flex',
  flexWrap: 'wrap',
  alignItems: 'center',
  '& small': { color: theme.palette.text.secondary },
  '& .icon': { opacity: 0.6, fontSize: '44px', color: theme.palette.primary.main },
}));


  return (

    <Paper style={{ padding: '16px', margin: '16px' }}>
      <input type="file" onChange={onFileChange} />
            <button onClick={onFileUpload}>
                Upload!
            </button>
            {fileData()}
            <div>
          <LogsDisplay />
        </div>
    </Paper>

    
  );
};
export default Analytics;
