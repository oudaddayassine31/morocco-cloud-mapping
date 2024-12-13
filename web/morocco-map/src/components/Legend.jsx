import React from 'react';
import { Paper, Typography, Box } from '@mui/material';
import { DeviceThermostat, WaterDrop } from '@mui/icons-material'

const Legend = ({ variable }) => {
  const getLegendConfig = () => {
    if (variable === 't2m') {
      return {
        title: 'Temperature',
        min: '-2°C',
        max: '40°C',
        gradient: 'linear-gradient(to right, #053061, #2166ac, #4393c3, #92c5de, #f7f7f7, #f4a582, #d6604d, #b2182b, #67001f)',
        note: 'Average temperature at 2m height',
        icon: <DeviceThermostat fontSize="small" />
      };
    }
    return {
      title: 'Precipitation',
      min: '0mm',
      max: '3000mm',
      gradient: 'linear-gradient(to right, #f7fbff, #deebf7, #c6dbef, #9ecae1, #6baed6, #4292c6, #2171b5, #08519c, #08306b)',
      note: 'Total precipitation',
      icon: <WaterDrop fontSize="small" />
    };
  };

  const config = getLegendConfig();

  return (
    <Paper
      elevation={3}
      className="legend-container"
    >
      <Box display="flex" alignItems="center" gap={1} mb={1}>
        {config.icon}
        <Typography variant="subtitle2" color="primary">
          {config.title}
        </Typography>
      </Box>
      <div className="legend-gradient" />
      <Box display="flex" justifyContent="space-between" mb={1}>
        <Typography variant="caption">{config.min}</Typography>
        <Typography variant="caption">{config.max}</Typography>
      </Box>
      <Typography variant="caption" color="textSecondary">
        {config.note}
      </Typography>
    </Paper>
  );
};
export default Legend;