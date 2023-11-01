import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Prompts from './Prompts';
import { usePlayGroundContext } from '../../context/AIProvider';

// Mocking AIProvider to simulate the context values
jest.mock('../../context/AIProvider');

// Mocking fetch for API calls
global.fetch = jest.fn();

const mockTemplatesList = [
  {
    id: '1',
    name: 'Template 1',
    config: { model: 'Model 1' },
    description: 'Description 1',
    lastUpdateDate: '2023-10-01T12:00:00Z',
  },
  {
    id: '2',
    name: 'Template 2',
    config: { model: 'Model 2' },
    description: 'Description 2',
    lastUpdateDate: '2023-10-02T12:00:00Z',
  },
];

const mockUpdateTimeDifference = jest.fn(() => '2 hours ago');

// Mocking the implementation of the getTimeDifference utility
jest.mock('app/utils/utils.js', () => ({
  getTimeDifference: mockUpdateTimeDifference,
}));

// Mocking the useContext hook for theme
usePlayGroundContext.mockReturnValue({
  templatesList: mockTemplatesList,
  deleteTempalte: jest.fn(),
  updateTemplateList: jest.fn(),
});

describe('Prompts Component', () => {
  it('renders Prompts component with template data', async () => {
    render(<Prompts />);

    // Check if the templates are rendered
    expect(screen.getByText('Template 1')).toBeInTheDocument();
    expect(screen.getByText('Template 2')).toBeInTheDocument();
    expect(screen.getByText('Model 1')).toBeInTheDocument();
    expect(screen.getByText('Model 2')).toBeInTheDocument();
    expect(screen.getByText('Description 1')).toBeInTheDocument();
    expect(screen.getByText('Description 2')).toBeInTheDocument();

    // Check if the "Last edited" information is displayed
    expect(screen.getByText('Last edited')).toBeInTheDocument();
    expect(screen.getByText('2 hours ago')).toBeInTheDocument();
  });

  it('deletes a template on confirmation', async () => {
    render(<Prompts />);

    // Click the delete button on the first template
    userEvent.click(screen.getAllByTitle('Delete Template')[0]);

    // Check if the confirmation dialog is opened
    expect(screen.getByText('Are you sure you want to delete the template?')).toBeInTheDocument();

    // Confirm the delete action
    userEvent.click(screen.getByText('Yes'));

    // Check if the deleteTemplate function is called
    await waitFor(() => {
      expect(usePlayGroundContext().deleteTempalte).toHaveBeenCalledWith('1');
    });
  });

  it('does not delete a template on cancellation', async () => {
    render(<Prompts />);

    // Click the delete button on the first template
    userEvent.click(screen.getAllByTitle('Delete Template')[0]);

    // Check if the confirmation dialog is opened
    expect(screen.getByText('Are you sure you want to delete the template?')).toBeInTheDocument();

    // Cancel the delete action
    userEvent.click(screen.getByText('No'));

    // Check if the deleteTemplate function is not called
    await waitFor(() => {
      expect(usePlayGroundContext().deleteTempalte).not.toHaveBeenCalled();
    });
  });

  it('searches for templates based on input', async () => {
    render(<Prompts />);

    // Type in the search input
    fireEvent.change(screen.getByPlaceholderText('Search...'), { target: { value: 'Template 1' } });

    // Check if the filtered template is displayed
    expect(screen.getByText('Template 1')).toBeInTheDocument();
    expect(screen.queryByText('Template 2')).not.toBeInTheDocument();
  });

  it('clears search input and displays all templates', async () => {
    render(<Prompts />);

    // Type in the search input
    fireEvent.change(screen.getByPlaceholderText('Search...'), { target: { value: 'Template 1' } });

    // Clear the search input
    fireEvent.change(screen.getByPlaceholderText('Search...'), { target: { value: '' } });

    // Check if all templates are displayed
    expect(screen.getByText('Template 1')).toBeInTheDocument();
    expect(screen.getByText('Template 2')).toBeInTheDocument();
  });

  // Add more test cases for different scenarios as needed
});
