// TimeSlider.jsx
import React from 'react';
import { Box, Slider, Typography, Paper } from '@mui/material';
import { CalendarMonth } from '@mui/icons-material';

const TimeSlider = ({ value, onChange }) => {
  const months = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
  ];

  const marks = months.map((month, index) => ({
    value: index,
    label: month,
  }));

  return (
    <Paper elevation={0} className="time-slider-container">
      <Box display="flex" alignItems="center" gap={2}>
        <CalendarMonth color="primary" />
        <Box flex={1}>
          <Typography variant="subtitle2" color="primary" gutterBottom>
            Time Period - 2023
          </Typography>
          <Slider
            value={value}
            onChange={(_, newValue) => onChange(newValue)}
            min={0}
            max={11}
            step={1}
            marks={marks}
            valueLabelDisplay="auto"
            valueLabelFormat={(value) => `${months[value]} 2023`}
          />
        </Box>
      </Box>
    </Paper>
  );
};

export default  TimeSlider;