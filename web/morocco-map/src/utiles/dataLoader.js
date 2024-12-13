// dataLoader.js

export const getColorScale = (variable) => {
  const scales = {
    't2m': {
      min: 273.15,  // 0°C
      max: 313.15,  // 40°C
      colormap: 'RdYlBu_r',
      formatValue: (val) => `${(val - 273.15).toFixed(1)}°C`
    },
    'tp': {
      min: 0,
      max: 0.1,  // 100mm
      colormap: 'Blues',
      formatValue: (val) => `${(val * 1000).toFixed(1)}mm`
    }
  };
  
  return scales[variable] || scales.t2m;
};

export const getVariableConfig = (variable) => {
  const configs = {
    't2m': {
      name: 'Temperature',
      unit: '°C',
      description: 'Average temperature at 2m height',
      range: {
        min: '-2°C',
        max: '28°C'
      }
    },
    'tp': {
      name: 'Precipitation',
      unit: 'mm',
      description: 'Total precipitation',
      range: {
        min: '0mm',
        max: '100mm'
      }
    }
  };
  
  return configs[variable] || configs.t2m;
};

export const formatValue = (value, variable) => {
  const scale = getColorScale(variable);
  return scale.formatValue(value);
};

export const getMonthName = (index) => {
  const months = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
  ];
  return months[index] || months[0];
};

export const getLegendGradient = (variable) => {
  if (variable === 't2m') {
    return 'linear-gradient(to right, #053061, #2166ac, #4393c3, #92c5de, #f7f7f7, #f4a582, #d6604d, #b2182b, #67001f)';
  }
  return 'linear-gradient(to right, #f7fbff, #deebf7, #c6dbef, #9ecae1, #6baed6, #4292c6, #2171b5, #08519c, #08306b)';
};

export const normalizeValue = (value, variable) => {
  const scale = getColorScale(variable);
  return (value - scale.min) / (scale.max - scale.min);
};

const API_BASE_URL = 'http://localhost:8000';

export const getTileUrl = (z, x, y, variable, time) => {
  return `${API_BASE_URL}/api/tiles/${z}/${x}/${y}?variable=${variable}&time=${time}`;
};