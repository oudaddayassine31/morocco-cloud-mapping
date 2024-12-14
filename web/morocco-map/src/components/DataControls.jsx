import React from 'react';
import { Box, FormControl, Select, MenuItem, Typography, Paper } from '@mui/material';
import { DeviceThermostat, WaterDrop } from '@mui/icons-material'; // Changed icons

const DataControls = ({ variable, onVariableChange }) => {
  return (
    <Paper elevation={0} className="data-controls-container">

      <FormControl fullWidth size="small">
        <Select
          value={variable}
          onChange={(e) => onVariableChange(e.target.value)}
          className="variable-select"
        >
          <MenuItem value="t2m">
            <Box display="flex" alignItems="center" gap={1}>
              <DeviceThermostat fontSize="small" />
              Temperature
            </Box>
          </MenuItem>
          <MenuItem value="tp">
            <Box display="flex" alignItems="center" gap={1}>
              <WaterDrop fontSize="small" />
              Precipitation
            </Box>
          </MenuItem>
        </Select>
      </FormControl>
    </Paper>
  );
};

export default DataControls; 