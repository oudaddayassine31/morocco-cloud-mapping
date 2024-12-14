import React, { useEffect, useRef } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { Paper } from '@mui/material';
import Legend from './Legend';



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
        style: 'mapbox://styles/mapbox/satellite-v9',
        center: [-6, 32],
        zoom: 5,
        maxZoom: 12,
        minZoom: 4,
        bounds: [
          [-13, 21],
          [0, 36]
        ]
      });

      map.current.addControl(
        new mapboxgl.NavigationControl({ showCompass: false }),
        'top-right'
      );
    }

    const initializeSource = () => {
      if (!sourceAdded.current && map.current.isStyleLoaded()) {
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
      }
    };

    if (map.current.isStyleLoaded()) {
      initializeSource();
    } else {
      map.current.on('load', initializeSource);
    }

    if (sourceAdded.current) {
      const source = map.current.getSource('climate-data');
      if (source) {
        source.setTiles([
          `${BACKEND_URL}/api/tiles/{z}/{x}/{y}?variable=${dataVariable}&time=${selectedTime}`
        ]);
      }
    }

    return () => {
      map.current?.off('load', initializeSource);
    };
  }, [selectedTime, dataVariable]);

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%' }}>
      <div ref={mapContainer} style={{ position: 'absolute', inset: 0 }} />
      <Legend variable={dataVariable} />
    </div>
  );
};

export default Map;