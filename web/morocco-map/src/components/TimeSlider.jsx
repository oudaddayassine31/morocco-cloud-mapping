import React from 'react';
import { Slider } from '@mui/material';

const TimeSlider = ({ value, onChange }) => {
  return (
    <div className="time-slider">
      <h3>Période</h3>
      <Slider
        value={value}
        onChange={(_, newValue) => onChange(newValue)}
        min={0}
        max={2}
        step={1}
        marks={[
          { value: 0, label: 'Jan 2023' },
          { value: 1, label: 'Feb 2023' },
          { value: 2, label: 'Mar 2023' },
        ]}
      />
    </div>
  );
};

export default TimeSlider;