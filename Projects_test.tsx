import React from 'react';
import { render, screen, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import axios from 'axios';
import Projects from './Projects';
import { usePlayGroundContext } from '../../context/AIProvider';

// Mocking axios to prevent actual API calls during testing
jest.mock('axios');
// Mocking AIProvider to simulate the context values
jest.mock('../../context/AIProvider');

describe('Projects Component', () => {
  beforeEach(() => {
    // Reset the mock state before each test
    jest.clearAllMocks();
  });

  it('renders Projects component with default data', async () => {
    // Mocking the axios post function to return data
    axios.post.mockResolvedValue({
      data: {
        templates: [{/* mock template data */}],
        users: [{/* mock user data */}],
      },
    });

    // Mocking the useContext hook for theme
    usePlayGroundContext.mockReturnValue({
      updateTemplateList: jest.fn(),
      updateSystemMessagesList: jest.fn(),
      updateSystemMessagesMap: jest.fn(),
    });

    await act(async () => {
      render(<Projects toggleTheme={jest.fn()} theme="light" />);
    });

    // Assertions for rendered elements
    expect(screen.getByLabelText('lab API tabs example')).toBeInTheDocument();
    expect(screen.getByLabelText('Templates')).toBeInTheDocument();
    expect(screen.getByLabelText('Members')).toBeInTheDocument();
    expect(screen.getByLabelText('Settings')).toBeInTheDocument();

    // Simulating a tab change
    userEvent.click(screen.getByLabelText('Members'));

    // Assertions for the content rendered after tab change
    // Modify these assertions based on your actual content
    expect(screen.getByText('Item Three')).toBeInTheDocument();
  });

  it('renders Projects component with empty data', async () => {
    // Mocking the axios post function to return empty data
    axios.post.mockResolvedValue({
      data: {
        templates: [],
        users: [],
      },
    });

    // Mocking the useContext hook for theme
    usePlayGroundContext.mockReturnValue({
      updateTemplateList: jest.fn(),
      updateSystemMessagesList: jest.fn(),
      updateSystemMessagesMap: jest.fn(),
    });

    await act(async () => {
      render(<Projects toggleTheme={jest.fn()} theme="light" />);
    });

    // Assertions for rendered elements when data is empty
    // Modify these assertions based on your actual content
    expect(screen.getByText('No templates available')).toBeInTheDocument();
    expect(screen.getByText('No members available')).toBeInTheDocument();
  });

  it('handles API call failure', async () => {
    // Mocking the axios post function to simulate API call failure
    axios.post.mockRejectedValue(new Error('API call failed'));

    // Mocking the useContext hook for theme
    usePlayGroundContext.mockReturnValue({
      updateTemplateList: jest.fn(),
      updateSystemMessagesList: jest.fn(),
      updateSystemMessagesMap: jest.fn(),
    });

    await act(async () => {
      render(<Projects toggleTheme={jest.fn()} theme="light" />);
    });

    // Assertions for handling API call failure
    // Modify these assertions based on your actual error handling logic
    expect(screen.getByText('Error loading data. Please try again later.')).toBeInTheDocument();
  });

  // Add more test cases for corner scenarios as needed
});
