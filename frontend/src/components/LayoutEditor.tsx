import React, { useState } from 'react';
import { useDrag, useDrop } from 'react-dnd';
import { Container, WidgetSpec } from '../types/index';

interface LayoutEditorProps {
  layout: { containers: Container[] };
  onLayoutChange: (newLayout: { containers: Container[] }) => void;
}

interface DraggableItemProps {
  id: string;
  type: 'container' | 'widget';
  children: React.ReactNode;
}

const DraggableItem: React.FC<DraggableItemProps> = ({ id, type, children }) => {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: type,
    item: { id, type },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  }));

  return (
    <div
      ref={drag}
      style={{
        opacity: isDragging ? 0.5 : 1,
        cursor: 'move',
      }}
    >
      {children}
    </div>
  );
};

interface DroppableAreaProps {
  id: string;
  type: 'container' | 'widget';
  onDrop: (item: { id: string; type: string }, targetId: string) => void;
  children: React.ReactNode;
}

const DroppableArea: React.FC<DroppableAreaProps> = ({ id, type, onDrop, children }) => {
  const [{ isOver }, drop] = useDrop(() => ({
    accept: type,
    drop: (item) => onDrop(item, id),
    collect: (monitor) => ({
      isOver: monitor.isOver(),
    }),
  }));

  return (
    <div
      ref={drop}
      style={{
        backgroundColor: isOver ? '#f0f8ff' : 'transparent',
        padding: '8px',
        borderRadius: '4px',
        minHeight: '100px',
      }}
    >
      {children}
    </div>
  );
};

const LayoutEditor: React.FC<LayoutEditorProps> = ({ layout, onLayoutChange }) => {
  const [editingLayout, setEditingLayout] = useState(layout);

  const handleDrop = (item: { id: string; type: string }, targetId: string) => {
    console.log(`Dropped ${item.type} ${item.id} into ${targetId}`);
    // Implement layout rearrangement logic here
    // For now, just log the drop event
  };

  const renderContainer = (container: Container, index: number) => {
    return (
      <DraggableItem key={`container-${index}`} id={`container-${index}`} type="container">
        <div style={{ border: '1px solid #ddd', padding: '16px', marginBottom: '16px', borderRadius: '8px' }}>
          <h3>{container.name}</h3>
          <p>Type: {container.type}</p>
          
          <DroppableArea 
            id={`container-${index}`} 
            type="widget" 
            onDrop={handleDrop}
          >
            <h4>Widgets</h4>
            {container.widgets?.map((widget, widgetIndex) => (
              <DraggableItem 
                key={`widget-${index}-${widgetIndex}`} 
                id={`widget-${index}-${widgetIndex}`} 
                type="widget"
              >
                <div style={{ border: '1px solid #ccc', padding: '8px', margin: '4px 0', borderRadius: '4px' }}>
                  <p>{widget.label} ({widget.type})</p>
                </div>
              </DraggableItem>
            )) || <p>No widgets</p>}
          </DroppableArea>
          
          {container.content?.map((nestedContainer, nestedIndex) => (
            <div key={`nested-${index}-${nestedIndex}`} style={{ marginLeft: '20px', marginTop: '16px' }}>
              {renderContainer(nestedContainer, nestedIndex)}
            </div>
          ))}
        </div>
      </DraggableItem>
    );
  };

  return (
    <div className="layout-editor">
      <h2>Layout Editor</h2>
      <p>Drag and drop containers and widgets to rearrange the layout</p>
      
      <div className="layout-containers">
        {editingLayout.containers.map((container, index) => renderContainer(container, index))}
      </div>
      
      <div className="editor-actions" style={{ marginTop: '24px' }}>
        <button 
          className="btn btn-primary"
          onClick={() => onLayoutChange(editingLayout)}
        >
          Save Layout
        </button>
        <button 
          className="btn btn-secondary"
          onClick={() => setEditingLayout(layout)}
          style={{ marginLeft: '8px' }}
        >
          Reset
        </button>
      </div>
    </div>
  );
};

export default LayoutEditor;