import React from 'react';
import { render, fireEvent, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Prompts from './Prompts';
import { usePlayGroundContext } from '../../context/AIProvider';

jest.mock('../../context/AIProvider', () => ({
  ...jest.requireActual('../../context/AIProvider'),
  usePlayGroundContext: jest.fn(),
}));

describe('Prompts', () => {
  const mockUsePlayGroundContext = usePlayGroundContext as jest.Mock;

  beforeEach(() => {
    mockUsePlayGroundContext.mockReturnValue({
      templatesList: [],
      deleteTemplate: jest.fn(),
      updateTemplateList: jest.fn(),
    });
  });

  test('renders Prompts component with default state', () => {
    render(<Prompts />);
    expect(screen.getByText('Search...')).toBeInTheDocument();
    expect(screen.getByText('Add Template')).toBeInTheDocument();
    expect(screen.queryByText('No templates available')).toBeInTheDocument();
  });

  test('renders Prompts component with template data', async () => {
    const mockTemplates = [
      { id: '1', name: 'Template 1', config: { model: 'Model A' }, description: 'Description 1', lastUpdateDate: '2023-10-01' },
      { id: '2', name: 'Template 2', config: { model: 'Model B' }, description: 'Description 2', lastUpdateDate: '2023-10-02' },
    ];
    mockUsePlayGroundContext.mockReturnValue({
      templatesList: mockTemplates,
      deleteTemplate: jest.fn(),
      updateTemplateList: jest.fn(),
    });

    render(<Prompts />);
    mockTemplates.forEach(template => {
      expect(screen.getByText(template.name)).toBeInTheDocument();
      expect(screen.getByText(template.config.model)).toBeInTheDocument();
      expect(screen.getByText(template.description)).toBeInTheDocument();
      expect(screen.getByText(getTimeDifference(template.lastUpdateDate))).toBeInTheDocument();
    });
  });

  test('handles template deletion', async () => {
    const mockTemplates = [
      { id: '1', name: 'Template 1', config: { model: 'Model A' }, description: 'Description 1', lastUpdateDate: '2023-10-01' },
      { id: '2', name: 'Template 2', config: { model: 'Model B' }, description: 'Description 2', lastUpdateDate: '2023-10-02' },
    ];
    mockUsePlayGroundContext.mockReturnValue({
      templatesList: mockTemplates,
      deleteTemplate: jest.fn(),
      updateTemplateList: jest.fn(),
    });

    render(<Prompts />);
    
    // Trigger delete for a template
    fireEvent.click(screen.getByTestId('delete-button-1'));

    // Confirm delete in the dialog
    fireEvent.click(screen.getByText('Yes'));

    // Wait for the asynchronous operations (if any) to complete
    await waitFor(() => {
      expect(screen.queryByText('Template 1')).not.toBeInTheDocument();
    });
  });

  test('handles cancellation of template deletion', async () => {
    const mockTemplates = [
      { id: '1', name: 'Template 1', config: { model: 'Model A' }, description: 'Description 1', lastUpdateDate: '2023-10-01' },
      { id: '2', name: 'Template 2', config: { model: 'Model B' }, description: 'Description 2', lastUpdateDate: '2023-10-02' },
    ];
    mockUsePlayGroundContext.mockReturnValue({
      templatesList: mockTemplates,
      deleteTemplate: jest.fn(),
      updateTemplateList: jest.fn(),
    });

    render(<Prompts />);
    
    // Trigger delete for a template
    fireEvent.click(screen.getByTestId('delete-button-1'));

    // Cancel delete in the dialog
    fireEvent.click(screen.getByText('No'));

    // Add assertions based on the expected behavior after cancellation
    expect(screen.getByText('Template 1')).toBeInTheDocument();
  });

  test('handles search input', async () => {
    const mockTemplates = [
      { id: '1', name: 'Template 1', config: { model: 'Model A' }, description: 'Description 1', lastUpdateDate: '2023-10-01' },
      { id: '2', name: 'Template 2', config: { model: 'Model B' }, description: 'Description 2', lastUpdateDate: '2023-10-02' },
    ];
    mockUsePlayGroundContext.mockReturnValue({
      templatesList: mockTemplates,
      deleteTemplate: jest.fn(),
      updateTemplateList: jest.fn(),
    });

    render(<Prompts />);
    
    // Trigger search input
    fireEvent.change(screen.getByPlaceholderText('Search...'), { target: { value: 'Template 1' } });

    // Wait for the asynchronous operations (if any) to complete
    await waitFor(() => {
      expect(screen.getByText('Template 1')).toBeInTheDocument();
      expect(screen.queryByText('Template 2')).not.toBeInTheDocument();
    });
  });

  test('handles adding a new template', async () => {
    render(<Prompts />);
    
    // Trigger add template
    fireEvent.click(screen.getByTestId('add-button'));

    // Wait for the asynchronous operations (if any) to complete
    await waitFor(() => {
      // Add assertions based on the expected behavior after adding a new template
      expect(screen.getByText('New Template')).toBeInTheDocument(); // Assuming a default name for a new template
    });
  });

  test('navigates to playground when "View Details" is clicked', async () => {
    const mockTemplates = [
      { id: '1', name: 'Template 1', config: { model: 'Model A' }, description: 'Description 1', lastUpdateDate: '2023-10-01' },
    ];
    mockUsePlayGroundContext.mockReturnValue({
      templatesList: mockTemplates,
      deleteTemplate: jest.fn(),
      updateTemplateList: jest.fn(),
    });

    render(<Prompts />);
    
    // Trigger "View Details" click
    fireEvent.click(screen.getByTestId('view-details-button-1'));

    // Wait for the asynchronous operations (if any) to complete
    await waitFor(() => {
      // Add assertions based on the expected behavior after "View Details" click
      expect(screen.getByText('Details for Template 1')).toBeInTheDocument(); // Adjust based on your component behavior
    });
  });

  // Additional Test Cases

  test('handles an empty template list', () => {
    render(<Prompts />);
    expect(screen.getByText('No templates available')).toBeInTheDocument();
  });

  test('handles search input with no matching templates', async () => {
    const mockTemplates = [
      { id: '1', name: 'Template 1', config: { model: 'Model A' }, description: 'Description 1', lastUpdateDate: '2023-10-01' },
      { id: '2', name: 'Template 2', config: { model: 'Model B' }, description: 'Description 2', lastUpdateDate: '2023-10-02' },
    ];
    mockUsePlayGroundContext.mockReturnValue({
      templatesList: mockTemplates,
      deleteTemplate: jest.fn(),
      updateTemplateList: jest.fn(),
    });

    render(<Prompts />);
    
    // Trigger search input
    fireEvent.change(screen.getByPlaceholderText('Search...'), { target: { value: 'Template 3' } });

    // Wait for the asynchronous operations (if any) to complete
    await waitFor(() => {
      expect(screen.getByText('No templates available')).toBeInTheDocument();
    });
  });

  test('handles template details for a new template', async () => {
    render(<Prompts />);
    
    // Trigger add template
    fireEvent.click(screen.getByTestId('add-button'));

    // Wait for the asynchronous operations (if any) to complete
    await waitFor(() => {
      // Add assertions based on the expected behavior after adding a new template
      expect(screen.getByText('Details for New Template')).toBeInTheDocument();
    });
  });

  test('handles errors during template deletion', async () => {
    const mockTemplates = [
      { id: '1', name: 'Template 1', config: { model: 'Model A' }, description: 'Description 1', lastUpdateDate: '2023-10-01' },
      { id: '2', name: 'Template 2', config: { model: 'Model B' }, description: 'Description 2', lastUpdateDate: '2023-10-02' },
    ];
    const mockDeleteTemplate = jest.fn(() => {
      throw new Error('Deletion failed');
    });
    mockUsePlayGroundContext.mockReturnValue({
      templatesList: mockTemplates,
      deleteTemplate: mockDeleteTemplate,
      updateTemplateList: jest.fn(),
    });

    render(<Prompts />);
    
    // Trigger delete for a template
    fireEvent.click(screen.getByTestId('delete-button-1'));

    // Confirm delete in the dialog
    fireEvent.click(screen.getByText('Yes'));

    // Wait for the asynchronous operations (if any) to complete
    await waitFor(() => {
      expect(screen.getByText('Error deleting template')).toBeInTheDocument();
    });
  });

  // Add more test cases based on different features, edge cases, or requirements
});
