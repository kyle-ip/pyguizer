import React, { useState, useEffect, useMemo, useRef } from 'react';
import { 
  getAppSpec, 
  runFunction, 
  getTask, 
  getPresets, 
  createPreset, 
  deletePreset, 
  Preset, 
  PresetCreate 
} from './services/api';
import { 
  AppSpec, 
  Container, 
  Section, 
  TaskStatus, 
  WidgetSpec, 
  FunctionInfo
} from './types/index';
import ReactMarkdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';
import rehypeSanitize from 'rehype-sanitize';
import WidgetFactory from './components/WidgetFactory';

// Container Renderer Component
const ContainerRenderer: React.FC<{
  container: Container;
  inputs: Record<string, any>;
  onChange: (id: string, value: any) => void;
}> = ({ container, inputs, onChange }) => {
  // Render widgets for this container
  const renderWidgets = (widgets: WidgetSpec[]) => {
    return widgets.map((widget: WidgetSpec) => (
      <WidgetFactory
        key={`widget-${widget.id}`}
        widget={widget}
        value={inputs[widget.id]}
        onChange={onChange}
      />
    ));
  };

  // Render content (nested containers) for this container
  const renderContent = (content?: Container[]) => {
    if (!content || content.length === 0) return null;
    
    return content.map((nestedContainer, index) => (
      <ContainerRenderer
        key={`nested-${container.name}-${index}`}
        container={nestedContainer}
        inputs={inputs}
        onChange={onChange}
      />
    ));
  };

  // Render based on container type
  switch (container.type) {
    case 'tabs':
      return (
        <div className="form-section tabs-container">
          <div className="tabs">
            {container.tabs?.map((tab) => (
              <div key={`tab-${tab.name}`} className="tab">
                <h3>{tab.name}</h3>
                {renderWidgets(tab.widgets)}
                {renderContent(tab.content)}
              </div>
            ))}
          </div>
        </div>
      );

    case 'accordion':
      return (
        <div className="form-section accordion-container">
          <div className="accordion">
            {container.items?.map((item) => (
              <div key={`accordion-${item.name}`} className="accordion-item">
                <div className="accordion-header">
                  <h3>{item.name}</h3>
                </div>
                <div className="accordion-content">
                  {renderWidgets(item.widgets)}
                  {renderContent(item.content)}
                </div>
              </div>
            ))}
          </div>
        </div>
      );

    case 'grid':
      return (
        <div className="form-section grid-container">
          <div className="grid">
            {container.rows?.map((row, rowIndex) => (
              <div key={`grid-row-${rowIndex}`} className="grid-row">
                {row.columns?.map((col, colIndex) => (
                  <div key={`grid-col-${rowIndex}-${colIndex}`} className="grid-col">
                    {renderWidgets(col.widgets)}
                    {renderContent(col.content)}
                  </div>
                ))}
              </div>
            ))}
          </div>
        </div>
      );

    case 'section':
    default:
      return (
        <div key={`section-${container.name}`} className="form-section">
          <h2>{container.name}</h2>
          {renderWidgets(container.widgets)}
          {renderContent(container.content)}
        </div>
      );
  }
};

// Simple component without ErrorBoundary that prevents the removeChild error
const App: React.FC = () => {
  const [appSpec, setAppSpec] = useState<AppSpec | null>(null);
  const [functions, setFunctions] = useState<FunctionInfo[]>([]);
  const [selectedFunction, setSelectedFunction] = useState<FunctionInfo | null>(null);
  const [inputs, setInputs] = useState<Record<string, any>>({});
  const [result, setResult] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [taskId, setTaskId] = useState<string | null>(null);
  const [taskStatus, setTaskStatus] = useState<TaskStatus | null>(null);
  const [taskProgress, setTaskProgress] = useState<number | null>(null);
  const [taskMessage, setTaskMessage] = useState<string | null>(null);
  
  // Preset management state
  const [presets, setPresets] = useState<Preset[]>([]);
  const [showPresetModal, setShowPresetModal] = useState(false);
  const [newPresetName, setNewPresetName] = useState('');
  const [newPresetDescription, setNewPresetDescription] = useState('');
  
  // Use ref to track if component is mounted to prevent state updates after unmount
  const isMountedRef = useRef(true);
  
  // Initialize component mounted state
  useEffect(() => {
    isMountedRef.current = true;
    
    return () => {
      isMountedRef.current = false;
    };
  }, []);

  // Fetch app specification and functions on mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        const spec = await getAppSpec();
        if (isMountedRef.current) {
          setAppSpec(spec);
          
          // Set functions from spec
          setFunctions(spec.functions || []);
          
          // Select the first function by default if available
          if (spec.functions && spec.functions.length > 0) {
            setSelectedFunction(spec.functions[0]);
          }
        }
      } catch (err) {
        if (isMountedRef.current) {
          setError('Failed to fetch application specification. Please check if the backend is running.');
          console.error('Error fetching app spec:', err);
        }
      }
    };

    fetchData();
  }, []);


  // Initialize inputs when selected function changes
  useEffect(() => {
    if (!selectedFunction) return;
    
    // Initialize inputs with default values
    const defaultInputs: Record<string, any> = {};
    
    // Function to collect widgets from containers recursively
    const collectWidgets = (container: any) => {
      // Add widgets from this container - use optional chaining for extra safety
      container.widgets?.forEach((widget: WidgetSpec) => {
        if (widget.default !== undefined) {
          defaultInputs[widget.id] = widget.default;
        }
      });
      
      // Process nested containers based on type
      const containerType = container.type || 'section';
      
      if (containerType === 'tabs') {
        container.tabs?.forEach(collectWidgets);
      } else if (containerType === 'accordion') {
        container.items?.forEach(collectWidgets);
      } else if (containerType === 'section') {
        container.content?.forEach(collectWidgets);
      } else if (containerType === 'grid') {
        container.rows?.forEach((row: any) => {
          row.columns?.forEach((col: any) => {
            collectWidgets(col);
          });
        });
      }
    };
    
    // Collect widgets from all containers - use optional chaining for layout itself
    selectedFunction.layout?.containers?.forEach(collectWidgets);
    
    // For backward compatibility, also check sections - use optional chaining
    selectedFunction.layout?.sections?.forEach(collectWidgets);
    
    setInputs(defaultInputs);
  }, [selectedFunction]);

  // Fetch presets when appSpec is loaded
  useEffect(() => {
    const fetchPresets = async () => {
      if (appSpec) {
        try {
          const presetsData = await getPresets();
          if (isMountedRef.current) {
            setPresets(presetsData);
          }
        } catch (err) {
          console.error('Error fetching presets:', err);
        }
      }
    };

    fetchPresets();
  }, [appSpec]);

  // Load preset values into inputs
  const handleLoadPreset = (preset: Preset) => {
    setInputs(preset.values);
  };

  // Save current inputs as a new preset
  const handleSavePreset = async () => {
    if (!newPresetName.trim()) return;

    try {
      const presetData: PresetCreate = {
        name: newPresetName,
        description: newPresetDescription,
        values: inputs
      };
      
      const newPreset = await createPreset(presetData);
      if (isMountedRef.current) {
        setPresets(prev => [...prev, newPreset]);
        setShowPresetModal(false);
        setNewPresetName('');
        setNewPresetDescription('');
      }
    } catch (err) {
      console.error('Error saving preset:', err);
    }
  };

  // Delete preset
  const handleDeletePreset = async (presetId: string) => {
    try {
      await deletePreset(presetId);
      if (isMountedRef.current) {
        setPresets(prev => prev.filter(preset => preset.id !== presetId));
      }
    } catch (err) {
      console.error('Error deleting preset:', err);
    }
  };

  // Poll task status if we have a task ID and it's not completed
  useEffect(() => {
    let intervalId: NodeJS.Timeout | null = null;
    
    const pollTaskStatus = async () => {
      if (!taskId) return;
      
      try {
        const task = await getTask(taskId);
        if (isMountedRef.current) {
          setTaskStatus(task.status);
          setTaskProgress(task.progress ?? null);
          setTaskMessage(task.message ?? null);
          
          if (task.status === TaskStatus.SUCCESS) {
            setResult(task.result);
            setIsLoading(false);
          } else if (task.status === TaskStatus.FAILED || task.status === TaskStatus.CANCELLED) {
            setError(task.error || task.message || 'Task failed');
            setIsLoading(false);
          }
        }
      } catch (err) {
        console.error('Error fetching task status:', err);
      }
    };
    
    if (taskId && taskStatus && ![TaskStatus.SUCCESS, TaskStatus.FAILED, TaskStatus.CANCELLED].includes(taskStatus)) {
      // Start polling immediately
      pollTaskStatus();
      // Then poll every 1 second
      intervalId = setInterval(pollTaskStatus, 1000);
    }
    
    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [taskId, taskStatus]);

  // Handle input changes
  const handleInputChange = (id: string, value: any) => {
    setInputs(prev => ({
      ...prev,
      [id]: value
    }));
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedFunction) return;
    
    try {
      setIsLoading(true);
      setError(null);
      setResult(null);
      setTaskId(null);
      setTaskStatus(null);
      setTaskProgress(null);
      setTaskMessage(null);
      
      // Get task ID from API with function name
      const response = await runFunction(selectedFunction.name, inputs);
      const newTaskId = response.task_id;
      if (isMountedRef.current) {
        setTaskId(newTaskId);
        setTaskStatus(response.status);
      }
      
    } catch (err: any) {
      if (isMountedRef.current) {
        setError(err.response?.data?.detail || 'Failed to execute function. Please check your inputs and try again.');
        console.error('Error running function:', err);
        setIsLoading(false);
      }
    }
  };

  // Stable key for the app container
  const appKey = useMemo(() => appSpec?.name || 'pyguizer-app', [appSpec]);


  // Simple error handling without ErrorBoundary
  if (error) {
    return (
      <div className="container" key="error-container">
        <div className="app-header">
          <h1>PyGUIzer</h1>
        </div>
        <div className="result-section" style={{ borderLeftColor: '#e74c3c', backgroundColor: '#ffebee' }}>
          <h2>Error</h2>
          <div className="result-content" style={{ backgroundColor: '#ffcdd2' }}>
            {error}
          </div>
        </div>
      </div>
    );
  }

  if (!appSpec) {
    return (
      <div className="container" key="loading-container">
        <div className="app-header">
          <h1>PyGUIzer</h1>
          <div className="loading"></div>
          <p>Loading application specification...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container" key={appKey}>
      <div className="app-header" key="app-header">
        <h1>{appSpec.name}</h1>
        <p>{appSpec.description}</p>
      </div>

      <div className="app-layout">
        {/* Function Sidebar */}
        <div className="function-sidebar">
          <h2>Functions</h2>
          <div className="function-list">
            {functions.map(func => (
              <div 
                key={func.name} 
                className={`function-item ${selectedFunction?.name === func.name ? 'selected' : ''}`}
                onClick={() => setSelectedFunction(func)}
              >
                <h3>{func.display_name}</h3>
                <p>{func.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Main Content */}
        <div className="main-content">
          {selectedFunction ? (
            <>
              {/* Preset Management Section */}
              <div className="form-section" key="preset-section">
                <h2>Presets</h2>
                <div className="preset-controls">
                  <div className="preset-list">
                    {presets.length > 0 ? (
                      presets.map(preset => (
                        <div key={preset.id} className="preset-item">
                          <div className="preset-info">
                            <h3>{preset.name}</h3>
                            {preset.description && <p>{preset.description}</p>}
                          </div>
                          <div className="preset-actions">
                            <button 
                              type="button" 
                              className="btn btn-secondary"
                              onClick={() => handleLoadPreset(preset)}
                            >
                              Load
                            </button>
                            <button 
                              type="button" 
                              className="btn btn-danger"
                              onClick={() => handleDeletePreset(preset.id)}
                            >
                              Delete
                            </button>
                          </div>
                        </div>
                      ))
                    ) : (
                      <p>No presets saved yet.</p>
                    )}
                  </div>
                  <button 
                    type="button" 
                    className="btn btn-secondary"
                    onClick={() => setShowPresetModal(true)}
                  >
                    Save Current Inputs as Preset
                  </button>
                </div>
              </div>

              <form onSubmit={handleSubmit} key="pyguizer-form">
                {/* Render containers from selected function */}
                {selectedFunction.layout.containers?.map((container: Container) => (
                  <ContainerRenderer
                    key={`container-${container.name || 'unnamed'}`}
                    container={container}
                    inputs={inputs}
                    onChange={handleInputChange}
                  />
                ))}

                {/* For backward compatibility, render sections if containers is empty */}
                {(!selectedFunction.layout.containers || selectedFunction.layout.containers.length === 0) && 
                 selectedFunction.layout.sections?.map((section: Section) => (
                  <ContainerRenderer
                    key={`backward-section-${section.name}`}
                    container={section}
                    inputs={inputs}
                    onChange={handleInputChange}
                  />
                ))}

                <div className="form-actions" key="form-actions">
                  <button type="submit" className="btn btn-primary" disabled={isLoading}>
                    {isLoading ? (
                      <> <div className="loading"></div> Running... </>
                    ) : (
                      'Run Function'
                    )}
                  </button>
                </div>
              </form>
            </>
          ) : (
            <div className="no-function-selected">
              <h2>No Function Selected</h2>
              <p>Please select a function from the sidebar to get started.</p>
            </div>
          )}
        </div>
      </div>

      {/* Save Preset Modal */}
      {showPresetModal && (
        <div className="modal-overlay" key="preset-modal">
          <div className="modal">
            <div className="modal-header">
              <h2>Save Preset</h2>
              <button 
                type="button" 
                className="btn-close"
                onClick={() => setShowPresetModal(false)}
              >
                ×
              </button>
            </div>
            <div className="modal-body">
              <div className="form-group">
                <label htmlFor="preset-name">Preset Name *</label>
                <input
                  type="text"
                  id="preset-name"
                  value={newPresetName}
                  onChange={(e) => setNewPresetName(e.target.value)}
                  placeholder="Enter preset name"
                />
              </div>
              <div className="form-group">
                <label htmlFor="preset-description">Description (optional)</label>
                <textarea
                  id="preset-description"
                  value={newPresetDescription}
                  onChange={(e) => setNewPresetDescription(e.target.value)}
                  placeholder="Enter preset description"
                  rows={3}
                />
              </div>
            </div>
            <div className="modal-footer">
              <button 
                type="button" 
                className="btn btn-secondary"
                onClick={() => setShowPresetModal(false)}
              >
                Cancel
              </button>
              <button 
                type="button" 
                className="btn btn-primary"
                onClick={handleSavePreset}
                disabled={!newPresetName.trim()}
              >
                Save Preset
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Task Progress */}
      {isLoading && taskStatus && (
        <div className="result-section" key="task-progress" style={{ borderLeftColor: '#3498db', backgroundColor: '#ebf5fb' }}>
          <h2>Task Status</h2>
          <div className="result-content" style={{ backgroundColor: '#d4e6f1' }}>
            <p><strong>Status:</strong> {taskStatus}</p>
            {taskProgress !== null && (
              <div className="progress-container">
                <div 
                  className="progress-bar" 
                  style={{ 
                    width: `${(taskProgress || 0) * 100}%`,
                    backgroundColor: '#3498db'
                  }}
                ></div>
                <span className="progress-text">{Math.round((taskProgress || 0) * 100)}%</span>
              </div>
            )}
            {taskMessage && <p><strong>Message:</strong> {taskMessage}</p>}
          </div>
        </div>
      )}

      {/* Task Result */}
      {result !== null && (
        <div className="result-section" key="task-result">
          <h2>Result</h2>
          <div className="result-content">
            {typeof result === 'object' ? (
              JSON.stringify(result, null, 2)
            ) : (
              <ReactMarkdown
                rehypePlugins={[rehypeRaw, rehypeSanitize]}
                components={{
                  code({ className, children, ...props }) {
                    return (
                      <code
                        className={className}
                        {...props}
                        style={{
                          backgroundColor: '#f5f5f5',
                          padding: '2px 4px',
                          borderRadius: '4px',
                          fontFamily: 'monospace',
                          fontSize: '0.9em'
                        }}
                      >
                        {children}
                      </code>
                    );
                  },
                  pre({ children }) {
                    return (
                      <div
                        style={{
                          backgroundColor: '#f5f5f5',
                          padding: '12px',
                          borderRadius: '6px',
                          overflow: 'auto',
                          marginTop: '8px',
                          marginBottom: '8px'
                        }}
                      >
                        {children}
                      </div>
                    );
                  },
                  h1({ children }) {
                    return <h1 style={{ marginTop: '16px', marginBottom: '8px' }}>{children}</h1>;
                  },
                  h2({ children }) {
                    return <h2 style={{ marginTop: '16px', marginBottom: '8px' }}>{children}</h2>;
                  },
                  h3({ children }) {
                    return <h3 style={{ marginTop: '12px', marginBottom: '6px' }}>{children}</h3>;
                  },
                  p({ children }) {
                    return <p style={{ margin: '8px 0' }}>{children}</p>;
                  },
                  ul({ children }) {
                    return <ul style={{ margin: '8px 0', paddingLeft: '24px' }}>{children}</ul>;
                  },
                  ol({ children }) {
                    return <ol style={{ margin: '8px 0', paddingLeft: '24px' }}>{children}</ol>;
                  },
                  li({ children }) {
                    return <li style={{ margin: '4px 0' }}>{children}</li>;
                  },
                  a({ href, children }) {
                    return (
                      <a
                        href={href}
                        style={{
                          color: '#3498db',
                          textDecoration: 'underline',
                          cursor: 'pointer'
                        }}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        {children}
                      </a>
                    );
                  },
                  blockquote({ children }) {
                    return (
                      <blockquote
                        style={{
                          borderLeft: '4px solid #e0e0e0',
                          margin: '12px 0',
                          padding: '8px 12px',
                          backgroundColor: '#fafafa',
                          fontStyle: 'italic'
                        }}
                      >
                        {children}
                      </blockquote>
                    );
                  },
                  table({ children }) {
                    return (
                      <table
                        style={{
                          borderCollapse: 'collapse',
                          width: '100%',
                          marginTop: '12px',
                          marginBottom: '12px'
                        }}
                      >
                        {children}
                      </table>
                    );
                  },
                  th({ children }) {
                    return (
                      <th
                        style={{
                          border: '1px solid #e0e0e0',
                          padding: '8px',
                          backgroundColor: '#f5f5f5',
                          textAlign: 'left',
                          fontWeight: 'bold'
                        }}
                      >
                        {children}
                      </th>
                    );
                  },
                  td({ children }) {
                    return (
                      <td
                        style={{
                          border: '1px solid #e0e0e0',
                          padding: '8px'
                        }}
                      >
                        {children}
                      </td>
                    );
                  }
                }}
              >
                {String(result)}
              </ReactMarkdown>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
