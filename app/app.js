import Map from 'ol/Map.js';
import View from 'ol/View.js';
import OSM from 'ol/source/OSM.js';
import ImageWMS from 'ol/source/ImageWMS.js';
import {Tile as TileLayer} from 'ol/layer.js';
import {Image as ImageLayer} from 'ol/layer.js';

const image = new ImageLayer({
  source: new ImageWMS({
    url: 'http://localhost:8000/geoserver/cite/wms',
    params: {LAYERS: 'cite:assets_location', TIMESTAMP: new Date().getTime()},
    serverType: 'geoserver',
  }),
});

const layers = [
  new TileLayer({
    source: new OSM(),
  }),
  image,
];

const map = new Map({
  target: 'map',
  layers: layers,
  view: new View({
    center: [0, 0],
    zoom: 2,
  }),
});

setInterval(() => {
  //only way to refresh the image without zooming in/out
  image.getSource().updateParams({TIMESTAMP: new Date().getTime()});
  console.log('refreshed');
}, 1000);
