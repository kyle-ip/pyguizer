import React from 'react';
import { WidgetSpec } from '../types/index';

interface WidgetFactoryProps {
  widget: WidgetSpec;
  value: any;
  onChange: (id: string, value: any) => void;
}

const WidgetFactory: React.FC<WidgetFactoryProps> = ({ widget, value, onChange }) => {
  const { id, label, type, required, constraints } = widget;
  const displayValue = value !== undefined ? value : widget.default;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    let newValue: any = e.target.value;
    
    // Handle boolean values
    if (type === 'boolean') {
      newValue = (e.target as HTMLInputElement).checked;
    }
    // Handle number values
    else if (type === 'number' || type === 'slider') {
      newValue = parseFloat(newValue);
      if (isNaN(newValue)) {
        newValue = widget.default;
      }
      // Ensure integer constraint is respected
      if (constraints.integer) {
        newValue = parseInt(newValue.toString());
      }
    }
    
    onChange(id, newValue);
  };

  const renderWidget = () => {
    switch (type) {
      case 'text':
        return (
          <input
            type="text"
            id={id}
            value={displayValue || ''}
            onChange={handleChange}
            placeholder={`Enter ${label.toLowerCase()}`}
          />
        );
        
      case 'number':
        return (
          <input
            type="number"
            id={id}
            value={displayValue || ''}
            onChange={handleChange}
            placeholder={`Enter ${label.toLowerCase()}`}
            step={constraints.integer ? 1 : 'any'}
          />
        );
        
      case 'slider':
        return (
          <input
            type="range"
            id={id}
            value={displayValue || 0}
            onChange={handleChange}
            min={constraints.min || 0}
            max={constraints.max || 100}
            step={constraints.step || 1}
          />
        );
        
      case 'boolean':
        return (
          <input
            type="checkbox"
            id={id}
            checked={!!displayValue}
            onChange={handleChange}
          />
        );
        
      case 'multi_select':
        return (
          <select
            id={id}
            multiple
            value={displayValue || []}
            onChange={(e) => {
              const selectedOptions = Array.from(e.target.selectedOptions, option => option.value);
              onChange(id, selectedOptions);
            }}
          >
            {constraints.options?.map((option: any) => (
              <option key={option.value} value={option.value}>
                {option.label || option.value}
              </option>
            )) || (
              <option value="">No options available</option>
            )}
          </select>
        );
        
      case 'select':
        return (
          <select
            id={id}
            value={displayValue || ''}
            onChange={handleChange}
          >
            <option value="">Select an option</option>
            {constraints.options?.map((option: any) => (
              <option key={option.value} value={option.value}>
                {option.label || option.value}
              </option>
            )) || (
              <option value="">No options available</option>
            )}
          </select>
        );
        
      case 'json':
        return (
          <textarea
            id={id}
            value={typeof displayValue === 'object' ? JSON.stringify(displayValue, null, 2) : displayValue || ''}
            onChange={(e) => {
              try {
                const jsonValue = JSON.parse(e.target.value);
                onChange(id, jsonValue);
              } catch (error) {
                // Don't update if JSON is invalid
              }
            }}
            rows={6}
            placeholder={`Enter JSON for ${label.toLowerCase()}`}
          />
        );
        
      case 'file_upload':
        return (
          <input
            type="file"
            id={id}
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) {
                // For now, we'll just send the file name
                // In a real app, you'd handle file uploads properly
                onChange(id, file.name);
              }
            }}
            accept={constraints.accept || '*/*'}
          />
        );
        
      case 'date':
        return (
          <input
            type="date"
            id={id}
            value={displayValue || ''}
            onChange={handleChange}
          />
        );
        
      case 'time':
        return (
          <input
            type="time"
            id={id}
            value={displayValue || ''}
            onChange={handleChange}
          />
        );
        
      case 'datetime':
        return (
          <input
            type="datetime-local"
            id={id}
            value={displayValue || ''}
            onChange={handleChange}
          />
        );
        
      case 'color':
        return (
          <input
            type="color"
            id={id}
            value={displayValue || '#000000'}
            onChange={handleChange}
          />
        );
        
      default:
        return (
          <input
            type="text"
            id={id}
            value={displayValue || ''}
            onChange={handleChange}
            placeholder={`Enter ${label.toLowerCase()}`}
          />
        );
    }
  };

  return (
    <div className="form-group">
      {type !== 'boolean' ? (
        <label htmlFor={id}>
          {label} {required && <span style={{ color: 'red' }}>*</span>}
        </label>
      ) : (
        <div className="checkbox-group">
          {renderWidget()}
          <label htmlFor={id}>
            {label} {required && <span style={{ color: 'red' }}>*</span>}
          </label>
        </div>
      )}
      {type !== 'boolean' && renderWidget()}
      {type === 'slider' && (
        <div style={{ marginTop: '8px', fontWeight: '500' }}>
          {displayValue}
        </div>
      )}
    </div>
  );
};

export default WidgetFactory;
