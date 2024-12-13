import React from 'react';

const Legend = ({ variable }) => {
  const legendContainer = {
    position: 'absolute',
    bottom: '32px',
    right: '32px',
    zIndex: 1,
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    padding: '16px',
    borderRadius: '8px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.3)',
    minWidth: '200px'
  };

  const gradientStyle = {
    width: '100%',
    height: '20px',
    margin: '10px 0',
    borderRadius: '4px'
  };

  const getGradient = () => {
    if (variable === 't2m') {
      return {
        ...gradientStyle,
        background: 'linear-gradient(to right, #053061, #2166ac, #4393c3, #92c5de, #f7f7f7, #f4a582, #d6604d, #b2182b, #67001f)'
      };
    }
    return {
      ...gradientStyle,
      background: 'linear-gradient(to right, #f7fbff, #deebf7, #c6dbef, #9ecae1, #6baed6, #4292c6, #2171b5, #08519c, #08306b)'
    };
  };

  const getLegendValues = () => {
    if (variable === 't2m') {
      return {
        title: 'Temperature',
        min: '-2°C',
        max: '28°C',
        note: 'Average temperature at 2m height'
      };
    }
    return {
      title: 'Precipitation',
      min: '0mm',
      max: '100mm',
      note: 'Total precipitation'
    };
  };

  const legendValues = getLegendValues();

  return (
    <div style={legendContainer}>
      <div style={{ fontWeight: 500, marginBottom: '8px' }}>
        {legendValues.title}
      </div>
      <div style={getGradient()} />
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        fontSize: '12px',
        marginTop: '4px'
      }}>
        <span>{legendValues.min}</span>
        <span>{legendValues.max}</span>
      </div>
      <div style={{ 
        fontSize: '11px', 
        color: '#666', 
        marginTop: '8px' 
      }}>
        {legendValues.note}
      </div>
    </div>
  );
};

export default Legend;