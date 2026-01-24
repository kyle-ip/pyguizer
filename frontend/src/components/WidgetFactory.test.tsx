import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import WidgetFactory from './WidgetFactory';
import { WidgetSpec } from '../types';

describe('WidgetFactory Component', () => {
  const mockOnChange = jest.fn();

  beforeEach(() => {
    mockOnChange.mockClear();
  });

  describe('Text Widget', () => {
    it('should render a text input', () => {
      const textWidget: WidgetSpec = {
        id: 'name',
        label: 'Name',
        type: 'text',
        default: '',
        required: true,
        data_type: 'string',
        constraints: {}
      };

      render(<WidgetFactory widget={textWidget} value={''} onChange={mockOnChange} />);
      
      const input = screen.getByRole('textbox', { name: /name/i });
      expect(input).toBeInTheDocument();
      expect(input).toHaveAttribute('type', 'text');
    });

    it('should call onChange when text input value changes', () => {
      const textWidget: WidgetSpec = {
        id: 'name',
        label: 'Name',
        type: 'text',
        default: '',
        required: true,
        data_type: 'string',
        constraints: {}
      };

      render(<WidgetFactory widget={textWidget} value={''} onChange={mockOnChange} />);
      
      const input = screen.getByRole('textbox', { name: /name/i });
      fireEvent.change(input, { target: { value: 'John' } });
      
      expect(mockOnChange).toHaveBeenCalledWith('name', 'John');
    });

    it('should display required indicator for required text fields', () => {
      const textWidget: WidgetSpec = {
        id: 'name',
        label: 'Name',
        type: 'text',
        default: '',
        required: true,
        data_type: 'string',
        constraints: {}
      };

      render(<WidgetFactory widget={textWidget} value={''} onChange={mockOnChange} />);
      
      const label = screen.getByText(/name/i);
      expect(label).toHaveTextContent('*');
    });
  });

  describe('Number Widget', () => {
    it('should render a number input', () => {
      const numberWidget: WidgetSpec = {
        id: 'age',
        label: 'Age',
        type: 'number',
        default: 30,
        required: false,
        data_type: 'integer',
        constraints: { integer: true }
      };

      render(<WidgetFactory widget={numberWidget} value={30} onChange={mockOnChange} />);
      
      const input = screen.getByRole('spinbutton', { name: /age/i });
      expect(input).toBeInTheDocument();
      expect(input).toHaveAttribute('type', 'number');
    });

    it('should call onChange with numeric value when number input changes', () => {
      const numberWidget: WidgetSpec = {
        id: 'age',
        label: 'Age',
        type: 'number',
        default: 30,
        required: false,
        data_type: 'integer',
        constraints: { integer: true }
      };

      render(<WidgetFactory widget={numberWidget} value={30} onChange={mockOnChange} />);
      
      const input = screen.getByRole('spinbutton', { name: /age/i });
      fireEvent.change(input, { target: { value: '25' } });
      
      expect(mockOnChange).toHaveBeenCalledWith('age', 25);
    });

    it('should respect integer constraint', () => {
      const numberWidget: WidgetSpec = {
        id: 'count',
        label: 'Count',
        type: 'number',
        default: 0,
        required: true,
        data_type: 'integer',
        constraints: { integer: true }
      };

      render(<WidgetFactory widget={numberWidget} value={0} onChange={mockOnChange} />);
      
      const input = screen.getByRole('spinbutton', { name: /count/i });
      expect(input).toHaveAttribute('step', '1');
    });
  });

  describe('Boolean Widget', () => {
    it('should render a checkbox', () => {
      const booleanWidget: WidgetSpec = {
        id: 'active',
        label: 'Active',
        type: 'boolean',
        default: true,
        required: false,
        data_type: 'boolean',
        constraints: {}
      };

      render(<WidgetFactory widget={booleanWidget} value={true} onChange={mockOnChange} />);
      
      const checkbox = screen.getByRole('checkbox', { name: /active/i });
      expect(checkbox).toBeInTheDocument();
      expect(checkbox).toBeChecked();
    });

    it('should call onChange with false when checkbox is toggled from true to false', () => {
      const booleanWidget: WidgetSpec = {
        id: 'active',
        label: 'Active',
        type: 'boolean',
        default: true,
        required: false,
        data_type: 'boolean',
        constraints: {}
      };

      render(<WidgetFactory widget={booleanWidget} value={true} onChange={mockOnChange} />);
      
      const checkbox = screen.getByRole('checkbox', { name: /active/i });
      
      // Toggle from true to false
      fireEvent.click(checkbox);
      expect(mockOnChange).toHaveBeenCalledWith('active', false);
      expect(mockOnChange).toHaveBeenCalledTimes(1);
    });

    it('should call onChange with true when checkbox is toggled from false to true', () => {
      const booleanWidget: WidgetSpec = {
        id: 'active',
        label: 'Active',
        type: 'boolean',
        default: true,
        required: false,
        data_type: 'boolean',
        constraints: {}
      };

      render(<WidgetFactory widget={booleanWidget} value={false} onChange={mockOnChange} />);
      
      const checkbox = screen.getByRole('checkbox', { name: /active/i });
      
      // Toggle from false to true
      fireEvent.click(checkbox);
      expect(mockOnChange).toHaveBeenCalledWith('active', true);
      expect(mockOnChange).toHaveBeenCalledTimes(1);
    });
  });

  describe('Slider Widget', () => {
    it('should render a range input', () => {
      const sliderWidget: WidgetSpec = {
        id: 'score',
        label: 'Score',
        type: 'slider',
        default: 50,
        required: false,
        data_type: 'float',
        constraints: { min: 0, max: 100, step: 0.1 }
      };

      render(<WidgetFactory widget={sliderWidget} value={50} onChange={mockOnChange} />);
      
      const slider = screen.getByRole('slider', { name: /score/i });
      expect(slider).toBeInTheDocument();
      expect(slider).toHaveAttribute('type', 'range');
    });

    it('should call onChange with numeric value when slider is moved', () => {
      const sliderWidget: WidgetSpec = {
        id: 'score',
        label: 'Score',
        type: 'slider',
        default: 50,
        required: false,
        data_type: 'float',
        constraints: { min: 0, max: 100, step: 1 }
      };

      render(<WidgetFactory widget={sliderWidget} value={50} onChange={mockOnChange} />);
      
      const slider = screen.getByRole('slider', { name: /score/i });
      fireEvent.change(slider, { target: { value: '75' } });
      
      expect(mockOnChange).toHaveBeenCalledWith('score', 75);
    });

    it('should display current slider value', () => {
      const sliderWidget: WidgetSpec = {
        id: 'score',
        label: 'Score',
        type: 'slider',
        default: 50,
        required: false,
        data_type: 'float',
        constraints: { min: 0, max: 100, step: 1 }
      };

      render(<WidgetFactory widget={sliderWidget} value={75} onChange={mockOnChange} />);
      
      const valueDisplay = screen.getByText('75');
      expect(valueDisplay).toBeInTheDocument();
    });
  });

  describe('Select Widget', () => {
    it('should render a select dropdown', () => {
      const selectWidget: WidgetSpec = {
        id: 'operation',
        label: 'Operation',
        type: 'select',
        default: 'add',
        required: true,
        data_type: 'string',
        constraints: { options: ['add', 'subtract', 'multiply', 'divide'] }
      };

      render(<WidgetFactory widget={selectWidget} value={'add'} onChange={mockOnChange} />);
      
      const select = screen.getByRole('combobox', { name: /operation/i });
      expect(select).toBeInTheDocument();
    });

    it('should call onChange when select value changes', () => {
      const selectWidget: WidgetSpec = {
        id: 'operation',
        label: 'Operation',
        type: 'select',
        default: 'add',
        required: true,
        data_type: 'string',
        constraints: { options: ['add', 'subtract', 'multiply', 'divide'] }
      };

      render(<WidgetFactory widget={selectWidget} value={'add'} onChange={mockOnChange} />);
      
      const select = screen.getByRole('combobox', { name: /operation/i });
      fireEvent.change(select, { target: { value: 'multiply' } });
      
      expect(mockOnChange).toHaveBeenCalledWith('operation', 'multiply');
    });
  });

  describe('JSON Widget', () => {
    it('should render a textarea for JSON input', () => {
      const jsonWidget: WidgetSpec = {
        id: 'config',
        label: 'Config',
        type: 'json',
        default: {},
        required: false,
        data_type: 'object',
        constraints: {}
      };

      render(<WidgetFactory widget={jsonWidget} value={{}} onChange={mockOnChange} />);
      
      const textarea = screen.getByRole('textbox', { name: /config/i });
      expect(textarea).toBeInTheDocument();
      expect(textarea.tagName).toBe('TEXTAREA');
    });

    it('should call onChange with parsed JSON when valid JSON is entered', () => {
      const jsonWidget: WidgetSpec = {
        id: 'config',
        label: 'Config',
        type: 'json',
        default: {},
        required: false,
        data_type: 'object',
        constraints: {}
      };

      render(<WidgetFactory widget={jsonWidget} value={{}} onChange={mockOnChange} />);
      
      const textarea = screen.getByRole('textbox', { name: /config/i });
      fireEvent.change(textarea, { target: { value: '{"key": "value"}' } });
      
      expect(mockOnChange).toHaveBeenCalledWith('config', { key: 'value' });
    });

    it('should not call onChange when invalid JSON is entered', () => {
      const jsonWidget: WidgetSpec = {
        id: 'config',
        label: 'Config',
        type: 'json',
        default: {},
        required: false,
        data_type: 'object',
        constraints: {}
      };

      render(<WidgetFactory widget={jsonWidget} value={{}} onChange={mockOnChange} />);
      
      const textarea = screen.getByRole('textbox', { name: /config/i });
      fireEvent.change(textarea, { target: { value: '{invalid json' } });
      
      expect(mockOnChange).not.toHaveBeenCalled();
    });
  });

  describe('Default Widget Type', () => {
    it('should render a text input for unknown widget types', () => {
      const unknownWidget: WidgetSpec = {
        id: 'unknown',
        label: 'Unknown Field',
        type: 'unknown_type' as any,
        default: '',
        required: false,
        data_type: 'string',
        constraints: {}
      };

      render(<WidgetFactory widget={unknownWidget} value={''} onChange={mockOnChange} />);
      
      const input = screen.getByRole('textbox', { name: /unknown field/i });
      expect(input).toBeInTheDocument();
      expect(input).toHaveAttribute('type', 'text');
    });
  });
});
