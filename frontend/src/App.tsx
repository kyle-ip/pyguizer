import React, { useState, useEffect } from 'react';
import { getAppSpec, runFunction } from './services/api';
import { AppSpec, Section } from './types';
import WidgetFactory from './components/WidgetFactory';

const App: React.FC = () => {
  const [appSpec, setAppSpec] = useState<AppSpec | null>(null);
  const [inputs, setInputs] = useState<Record<string, any>>({});
  const [result, setResult] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch app specification on mount
  useEffect(() => {
    const fetchAppSpec = async () => {
      try {
        const spec = await getAppSpec();
        setAppSpec(spec);
        
        // Initialize inputs with default values
        const defaultInputs: Record<string, any> = {};
        spec.layout.sections.forEach((section: Section) => {
          section.widgets.forEach(widget => {
            if (widget.default !== undefined) {
              defaultInputs[widget.id] = widget.default;
            }
          });
        });
        setInputs(defaultInputs);
      } catch (err) {
        setError('Failed to fetch application specification. Please check if the backend is running.');
        console.error('Error fetching app spec:', err);
      }
    };

    fetchAppSpec();
  }, []);

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
      
      const response = await runFunction(inputs);
      setResult(response.result);
    } catch (err) {
      setError('Failed to execute function. Please check your inputs and try again.');
      console.error('Error running function:', err);
    } finally {
      setIsLoading(false);
    }
  };

  if (error) {
    return (
      <div className="container">
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
      <div className="container">
        <div className="app-header">
          <h1>PyGUIzer</h1>
          <div className="loading"></div>
          <p>Loading application specification...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="app-header">
        <h1>{appSpec.name}</h1>
        <p>{appSpec.description}</p>
      </div>

      <form onSubmit={handleSubmit}>
        {appSpec.layout.sections.map((section: Section, sectionIndex: number) => (
          <div key={sectionIndex} className="form-section">
            <h2>{section.name}</h2>
            {section.widgets.map(widget => (
              <WidgetFactory
                key={widget.id}
                widget={widget}
                value={inputs[widget.id]}
                onChange={handleInputChange}
              />
            ))}
          </div>
        ))}

        <div className="form-actions">
          <button type="submit" className="btn btn-primary" disabled={isLoading}>
            {isLoading ? (
              <> <div className="loading"></div> Running... </>
            ) : (
              'Run Function'
            )}
          </button>
        </div>
      </form>

      {result !== null && (
        <div className="result-section">
          <h2>Result</h2>
          <div className="result-content">
            {typeof result === 'object' ? JSON.stringify(result, null, 2) : String(result)}
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
