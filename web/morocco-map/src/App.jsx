import React from 'react';
import { ThemeProvider, createTheme, AppBar, Toolbar, Typography, Box } from '@mui/material';
import { DeviceThermostat, WaterDrop } from '@mui/icons-material'; // Changed icons
import Map from './components/Map';
import TimeSlider from './components/TimeSlider';
import DataControls from './components/DataControls';

import './App.css'


const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    h6: {
      fontWeight: 500,
    },
  },
  components: {
    MuiSlider: {
      styleOverrides: {
        markLabel: {
          fontSize: '0.75rem',
        },
      },
    },
  },
});

const App = () => {
  const [selectedTime, setSelectedTime] = React.useState(0);
  const [dataVariable, setDataVariable] = React.useState('t2m');

  return (
    <ThemeProvider theme={theme}>
      <div className="app-container">
        <AppBar position="static" elevation={0} color="transparent">
          <Toolbar>
            <Box display="flex" alignItems="center" gap={1}>
              {dataVariable === 't2m' ? (
                <DeviceThermostat color="primary" />
              ) : (
                <WaterDrop color="primary" />
              )}
              <Typography variant="h6" color="primary">
                Morocco Climate Data Visualization
              </Typography>
            </Box>
          </Toolbar>
        </AppBar>

        <main className="main-content">
          <Map selectedTime={selectedTime} dataVariable={dataVariable} />
        </main>

        <div className="controls-panel">
          <div className="controls-container">
            <TimeSlider value={selectedTime} onChange={setSelectedTime} />
            <DataControls variable={dataVariable} onVariableChange={setDataVariable} />
          </div>
        </div>
      </div>
    </ThemeProvider>
  );
};

export default App;