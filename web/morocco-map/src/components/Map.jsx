import React, { useEffect, useRef } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import Legend from './Legend';

// Configure Mapbox token
mapboxgl.accessToken = 'pk.eyJ1IjoiZWxhb3VuaWphc3NpbSIsImEiOiJjbGF5ZmswaXIwNzhvM3FtbHhiZ2o3eG94In0.2D5g4-DntItXKK1ylEJsrQ';

const BACKEND_URL = 'http://localhost:8000';

const Map = ({ selectedTime, dataVariable }) => {
  const mapContainer = useRef(null);
  const map = useRef(null);
  const sourceAdded = useRef(false);

  useEffect(() => {
    if (!map.current) {
      map.current = new mapboxgl.Map({
        container: mapContainer.current,
        style: 'mapbox://styles/mapbox/satellite-v9', // Changed to satellite view
        center: [-6, 32],
        zoom: 5,
        maxZoom: 12,
        bounds: [
          [-13, 21],
          [0, 36]
        ]
      });

      map.current.addControl(new mapboxgl.NavigationControl(), 'top-right');
    }

    const initializeSource = () => {
      if (!sourceAdded.current && map.current.isStyleLoaded()) {
        try {
          // Remove existing source and layer if they exist
          if (map.current.getSource('climate-data')) {
            map.current.removeLayer('climate-layer');
            map.current.removeSource('climate-data');
          }

          map.current.addSource('climate-data', {
            type: 'raster',
            tiles: [
              `${BACKEND_URL}/api/tiles/{z}/{x}/{y}?variable=${dataVariable}&time=${selectedTime}`
            ],
            tileSize: 256
          });

          map.current.addLayer({
            id: 'climate-layer',
            type: 'raster',
            source: 'climate-data',
            paint: {
              'raster-opacity': 0.7,
              'raster-resampling': 'linear'
            }
          });

          sourceAdded.current = true;
        } catch (error) {
          console.error('Error adding source:', error);
        }
      }
    };

    if (map.current) {
      if (map.current.isStyleLoaded()) {
        initializeSource();
      } else {
        map.current.on('load', initializeSource);
      }
    }

    // Update tiles when parameters change
    if (map.current && sourceAdded.current) {
      try {
        const source = map.current.getSource('climate-data');
        if (source) {
          source.setTiles([
            `${BACKEND_URL}/api/tiles/{z}/{x}/{y}?variable=${dataVariable}&time=${selectedTime}`
          ]);
        }
      } catch (error) {
        console.error('Error updating tiles:', error);
      }
    }

    // Add error handling for tile loading
    const handleTileError = (event) => {
      console.error('Tile loading error:', event);
    };

    map.current?.on('tile.error', handleTileError);

    return () => {
      map.current?.off('tile.error', handleTileError);
      map.current?.off('load', initializeSource);
    };
  }, [selectedTime, dataVariable]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (map.current) {
        map.current.remove();
        map.current = null;
        sourceAdded.current = false;
      }
    };
  }, []);

  const mapStyle = {
    position: 'absolute',
    top: 0,
    bottom: 0,
    left: 0,
    right: 0
  };

  const containerStyle = {
    position: 'relative',
    width: '100%',
    height: '100vh'
  };

  return (
    <div style={containerStyle}>
      <div ref={mapContainer} style={mapStyle} />
      <Legend variable={dataVariable} />
    </div>
  );
};

export default Map;