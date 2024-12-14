import React from 'react';
import { Box, AppBar, Toolbar, Typography, Paper } from '@mui/material';
import { DeviceThermostat, WaterDrop, Public } from '@mui/icons-material';
import Map from './components/Map';
import TimeSlider from './components/TimeSlider';
import DataControls from './components/DataControls';
import Legend from './components/Legend';

const App = () => {
  const [selectedTime, setSelectedTime] = React.useState(0);
  const [dataVariable, setDataVariable] = React.useState('t2m');

  return (
    <Box className="app-container">
      {/* Map as the base layer */}
      <Map selectedTime={selectedTime} dataVariable={dataVariable} />

      {/* Floating Elements Container */}
      <Box className="floating-elements" sx={{ position: 'absolute', inset: 0, pointerEvents: 'none' }}>
        {/* Header */}
        <Paper 
          elevation={0}
          sx={{ 
            position: 'absolute',
            top: '20px',
            left: '50%',
            transform: 'translateX(-50%)',
            background: 'linear-gradient(135deg, rgba(25,118,210,0.95) 0%, rgba(21,101,192,0.95) 100%)',
            borderRadius: '12px',
            padding: '8px 24px',
            pointerEvents: 'auto'
          }}
        >
          <Box display="flex" alignItems="center" gap={2}>
            <Public sx={{ color: 'white' }} />
            <Typography 
              variant="h6" 
              sx={{ 
                color: 'white', 
                fontWeight: 600,
                textAlign: 'center'
              }}
            >
              Morocco Climate 2023
            </Typography>
          </Box>
        </Paper>

        {/* Legend and Controls Panel */}
        <Paper 
          className="control-panel glass-panel"
          sx={{
            position: 'absolute',
            top: '20px',
            right: '20px',
            width: '280px',
            overflow: 'hidden',
            pointerEvents: 'auto'
          }}
        >
          {/* Legend Section */}
          <Box sx={{ p: 2, borderBottom: '1px solid rgba(0,0,0,0.1)' }}>
            <Legend variable={dataVariable} />
          </Box>
          
          {/* Data Controls Section */}
          <Box sx={{ p: 2 }}>

            <DataControls 
              variable={dataVariable} 
              onVariableChange={setDataVariable} 
            />
          </Box>
        </Paper>

        {/* Time Slider */}
        <Paper 
          elevation={0}
          className="glass-panel"
          sx={{
            position: 'absolute',
            bottom: '20px',
            left: '50%',
            transform: 'translateX(-50%)',
            width: 'auto',
            minWidth: '600px',
            maxWidth: '90%',
            borderRadius: '12px',
            padding: '16px 24px',
            pointerEvents: 'auto'
          }}
        >
          <TimeSlider 
            value={selectedTime} 
            onChange={setSelectedTime} 
          />
        </Paper>
      </Box>
    </Box>
  );
};

export default App;