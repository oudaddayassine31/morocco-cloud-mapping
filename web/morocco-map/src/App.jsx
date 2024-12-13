// src/App.jsx
import React from 'react';
import Map from './components/Map';
import TimeSlider from './components/TimeSlider';
import DataControls from './components/DataControls';
import './styles/global.css';

function App() {
  const [selectedTime, setSelectedTime] = React.useState(0);
  const [dataVariable, setDataVariable] = React.useState('t2m');

  return (
    <div className="app">
      <Map 
        selectedTime={selectedTime}
        dataVariable={dataVariable}
      />
      <div className="controls">
        <TimeSlider 
          value={selectedTime}
          onChange={setSelectedTime}
        />
        <DataControls 
          variable={dataVariable}
          onVariableChange={setDataVariable}
        />
      </div>
    </div>
  );
}

export default App;