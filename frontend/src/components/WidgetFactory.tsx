import React from 'react';
import { WidgetSpec } from '../types/index';

interface WidgetFactoryProps {
  widget: WidgetSpec;
  value: any;
  onChange: (id: string, value: any) => void;
  isDarkMode?: boolean;
}

const WidgetFactory: React.FC<WidgetFactoryProps> = ({ widget, value, onChange, isDarkMode = false }) => {
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

  const inputStyle = {
    backgroundColor: isDarkMode ? '#444' : '#fff',
    color: isDarkMode ? '#fff' : '#000',
    border: `1px solid ${isDarkMode ? '#666' : '#ccc'}`,
    padding: '8px',
    borderRadius: '4px',
    width: '100%'
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
            style={inputStyle}
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
            style={inputStyle}
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
            style={{
              ...inputStyle,
              padding: '0'
            }}
          />
        );
        
      case 'boolean':
        return (
          <input
            type="checkbox"
            id={id}
            checked={!!displayValue}
            onChange={handleChange}
            style={{
              accentColor: isDarkMode ? '#007bff' : 'auto'
            }}
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
            style={{
              ...inputStyle,
              height: '120px'
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
            style={inputStyle}
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
            style={{
              ...inputStyle,
              fontFamily: 'monospace',
              resize: 'vertical'
            }}
          />
        );
        
      case 'file_upload':
        return (
          <div>
            <input
              type="file"
              id={id}
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) {
                  // Create a reader to handle the file
                  const reader = new FileReader();
                  reader.onloadstart = () => {
                    // Show initial progress
                    console.log('File upload started');
                  };
                  reader.onprogress = (event) => {
                    if (event.lengthComputable) {
                      const percentComplete = Math.round((event.loaded / event.total) * 100);
                      console.log(`File upload progress: ${percentComplete}%`);
                    }
                  };
                  reader.onload = () => {
                    // For now, we'll send the file name and size
                    // In a real app, you'd upload the file to the server
                    const fileInfo = {
                      name: file.name,
                      size: file.size,
                      type: file.type,
                      lastModified: file.lastModified
                    };
                    onChange(id, fileInfo);
                  };
                  reader.onerror = () => {
                    console.error('Error reading file');
                  };
                  // Read the file as ArrayBuffer (for binary files)
                  reader.readAsArrayBuffer(file);
                }
              }}
              accept={constraints.accept || '*/*'}
              style={inputStyle}
            />
            {displayValue && (
              <div style={{ marginTop: '8px', fontSize: '0.9em', color: isDarkMode ? '#aaa' : '#666' }}>
                {typeof displayValue === 'string' ? displayValue : displayValue.name}
              </div>
            )}
          </div>
        );
        
      case 'date':
        return (
          <input
            type="date"
            id={id}
            value={displayValue || ''}
            onChange={handleChange}
            style={inputStyle}
          />
        );
        
      case 'time':
        return (
          <input
            type="time"
            id={id}
            value={displayValue || ''}
            onChange={handleChange}
            style={inputStyle}
          />
        );
        
      case 'datetime':
        return (
          <input
            type="datetime-local"
            id={id}
            value={displayValue || ''}
            onChange={handleChange}
            style={inputStyle}
          />
        );
        
      case 'color':
        return (
          <input
            type="color"
            id={id}
            value={displayValue || '#000000'}
            onChange={handleChange}
            style={{
              ...inputStyle,
              padding: '2px'
            }}
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
            style={inputStyle}
          />
        );
    }
  };

  return (
    <div className="form-group" style={{ marginBottom: '16px' }}>
      {type !== 'boolean' ? (
        <label htmlFor={id} style={{ display: 'block', marginBottom: '4px', color: isDarkMode ? '#ddd' : '#000' }}>
          {label} {required && <span style={{ color: 'red' }}>*</span>}
        </label>
      ) : (
        <div className="checkbox-group">
          {renderWidget()}
          <label htmlFor={id} style={{ color: isDarkMode ? '#ddd' : '#000' }}>
            {label} {required && <span style={{ color: 'red' }}>*</span>}
          </label>
        </div>
      )}
      {type !== 'boolean' && renderWidget()}
      {type === 'slider' && (
        <div style={{ marginTop: '8px', fontWeight: '500', color: isDarkMode ? '#ddd' : '#000' }}>
          {displayValue}
        </div>
      )}
    </div>
  );
};

export default WidgetFactory;
