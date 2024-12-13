import * as zarr from 'zarr';

export const loadZarrData = async (zoomLevel, variable, time) => {
  try {
    const store = new zarr.HTTPStore(`/api/data/processed/pyramids/zoom_${zoomLevel}`);
    const z = await zarr.open(store);
    return {
      data: await z.get([variable]),  // Changé de ['t2m'] à [variable]
      metadata: z.attrs
    };
  } catch (error) {
    console.error('Erreur chargement données:', error);
    throw error;
  }
};

export const getColorScale = (variable) => {
  if (variable === 't2m') {
    return {
      min: 273.15,  // 0°C
      max: 313.15,  // 40°C
      colormap: 'RdYlBu_r'
    };
  }
  return {
    min: 0,
    max: 0.1,  // 100mm
    colormap: 'Blues'
  };
};