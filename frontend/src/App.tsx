import React, { useState, useEffect, useMemo, useRef } from 'react';
import { getAppSpec, runFunction, getTask, getPresets, createPreset, deletePreset, Preset, PresetCreate } from './services/api';
import { AppSpec, Section, TaskStatus, WidgetSpec } from './types/index';
import ReactMarkdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';
import rehypeSanitize from 'rehype-sanitize';
import WidgetFactory from './components/WidgetFactory';

// Simple component without ErrorBoundary that prevents the removeChild error
const App: React.FC = () => {
  const [appSpec, setAppSpec] = useState<AppSpec | null>(null);
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

  // Fetch app specification on mount
  useEffect(() => {
    const fetchAppSpec = async () => {
      try {
        const spec = await getAppSpec();
        if (isMountedRef.current) {
          setAppSpec(spec);
          
          // Initialize inputs with default values
          const defaultInputs: Record<string, any> = {};
          spec.layout.sections.forEach((section: Section) => {
            section.widgets.forEach((widget: WidgetSpec) => {
              if (widget.default !== undefined) {
                defaultInputs[widget.id] = widget.default;
              }
            });
          });
          setInputs(defaultInputs);
        }
      } catch (err) {
        if (isMountedRef.current) {
          setError('Failed to fetch application specification. Please check if the backend is running.');
          console.error('Error fetching app spec:', err);
        }
      }
    };

    fetchAppSpec();
  }, []);

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
    
    if (!appSpec) return;
    
    try {
      setIsLoading(true);
      setError(null);
      setResult(null);
      setTaskId(null);
      setTaskStatus(null);
      setTaskProgress(null);
      setTaskMessage(null);
      
      // Get task ID from API
      const response = await runFunction(inputs);
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
        {appSpec.layout.sections.map((section: Section) => (
          <div key={`section-${section.name}`} className="form-section">
            <h2>{section.name}</h2>
            {section.widgets.map((widget: WidgetSpec) => (
              <WidgetFactory
                key={`widget-${widget.id}`}
                widget={widget}
                value={inputs[widget.id]}
                onChange={handleInputChange}
              />
            ))}
          </div>
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
