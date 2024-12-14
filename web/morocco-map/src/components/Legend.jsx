import React from 'react';
import { Box, Typography } from '@mui/material';
import { DeviceThermostat, WaterDrop } from '@mui/icons-material';

const Legend = ({ variable }) => {
  const getLegendConfig = () => {
    if (variable === 't2m') {
      return {
        title: 'Temperature',
        min: '-2°C',
        max: '40°C',
        gradientClass: 'temperature-gradient',
        note: 'Average temperature at 2m height',
        icon: <DeviceThermostat fontSize="small" color="primary" />
      };
    }
    return {
      title: 'Precipitation',
      min: '0mm',
      max: '500mm',
      gradientClass: 'precipitation-gradient',
      note: 'Total precipitation',
      icon: <WaterDrop fontSize="small" color="primary" />
    };
  };

  const config = getLegendConfig();

  return (
    <Box>
      <Box display="flex" alignItems="center" gap={1} mb={1}>
        {config.icon}
        <Typography variant="subtitle2" color="primary">
          {config.title}
        </Typography>
      </Box>
      <div className={`legend-gradient ${config.gradientClass}`} />
      <Box display="flex" justifyContent="space-between" mb={1}>
        <Typography variant="caption">{config.min}</Typography>
        <Typography variant="caption">{config.max}</Typography>
      </Box>
      <Typography variant="caption" color="textSecondary">
        {config.note}
      </Typography>
    </Box>
  );
};

export default Legend;