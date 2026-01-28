import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions,
} from 'chart.js';
import { Line, Bar, Pie, Doughnut } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

interface ChartProps {
  data: any;
  type?: 'line' | 'bar' | 'pie' | 'doughnut';
  title?: string;
}

const Chart: React.FC<ChartProps> = ({ data, type = 'line', title = 'Chart' }) => {
  // Process data based on type
  const processData = () => {
    if (Array.isArray(data)) {
      // Array of numbers or objects
      if (data.every(item => typeof item === 'number')) {
        // Simple array of numbers
        return {
          labels: data.map((_, index) => `Item ${index + 1}`),
          datasets: [{
            label: 'Values',
            data: data,
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.5)',
            tension: 0.1,
          }],
        };
      } else if (data.every(item => typeof item === 'object' && item !== null)) {
        // Array of objects
        const keys = Object.keys(data[0]);
        if (keys.length === 2) {
          // Assume first key is label, second is value
          const labelKey = keys[0];
          const valueKey = keys[1];
          return {
            labels: data.map(item => item[labelKey]),
            datasets: [{
              label: valueKey.charAt(0).toUpperCase() + valueKey.slice(1),
              data: data.map(item => item[valueKey]),
              borderColor: 'rgb(75, 192, 192)',
              backgroundColor: 'rgba(75, 192, 192, 0.5)',
              tension: 0.1,
            }],
          };
        }
      }
    } else if (typeof data === 'object' && data !== null) {
      // Object with key-value pairs
      return {
        labels: Object.keys(data),
        datasets: [{
          label: 'Values',
          data: Object.values(data),
          borderColor: 'rgb(75, 192, 192)',
          backgroundColor: 'rgba(75, 192, 192, 0.5)',
          tension: 0.1,
        }],
      };
    }
    return {
      labels: [],
      datasets: [],
    };
  };

  const chartData = processData();

  const options: ChartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: title,
      },
    },
  };

  const renderChart = () => {
    switch (type) {
      case 'bar':
        return <Bar options={options} data={chartData} />;
      case 'pie':
        return <Pie options={options} data={chartData} />;
      case 'doughnut':
        return <Doughnut options={options} data={chartData} />;
      case 'line':
      default:
        return <Line options={options} data={chartData} />;
    }
  };

  return (
    <div style={{ marginTop: '16px', marginBottom: '16px' }}>
      {renderChart()}
    </div>
  );
};

export default Chart;