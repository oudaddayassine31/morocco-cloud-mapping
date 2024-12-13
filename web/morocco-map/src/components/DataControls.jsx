import React from 'react';
import { FormControl, Select, MenuItem } from '@mui/material';

const DataControls = ({ variable, onVariableChange }) => {
  return (
    <div className="data-controls">
      <h3>Variable</h3>
      <FormControl>
        <Select
          value={variable}
          onChange={(e) => onVariableChange(e.target.value)}
        >
          <MenuItem value="t2m">Température</MenuItem>
          <MenuItem value="tp">Précipitations</MenuItem>
        </Select>
      </FormControl>
    </div>
  );
};

export default DataControls; 