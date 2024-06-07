(function () {
  var map = new ol.Map({
    target: 'map',
    layers: [
      new ol.layer.Group({
        // A layer must have a title to appear in the layerswitcher
        title: 'Base maps',
        layers: [
          new ol.layer.Group({
            // A layer must have a title to appear in the layerswitcher
            title: 'Water color with labels',
            // Setting the layers type to 'base' results
            // in it having a radio button and only one
            // base layer being visibile at a time
            type: 'base',
            // Setting combine to true causes sub-layers to be hidden
            // in the layerswitcher, only the parent is shown
            combine: true,
            visible: false,
            layers: [
              new ol.layer.Tile({
                source: new ol.source.Stamen({
                  layer: 'watercolor'
                })
              }),
              new ol.layer.Tile({
                source: new ol.source.Stamen({
                  layer: 'terrain-labels'
                })
              })
            ]
          }),
          new ol.layer.Tile({
            // A layer must have a title to appear in the layerswitcher
            title: 'Water color',
            // Again set this layer as a base layer
            type: 'base',
            visible: false,
            source: new ol.source.Stamen({
              layer: 'watercolor'
            })
          }),
          new ol.layer.Tile({
            // A layer must have a title to appear in the layerswitcher
            title: 'OSM',
            // Again set this layer as a base layer
            type: 'base',
            visible: true,
            source: new ol.source.OSM()
          })
        ]
      })
    ],
    view: new ol.View({
      center: ol.proj.fromLonLat([0, 0], 'EPSG:3857'),
      zoom: 3,
      minZoom: 3,
      projection: 'EPSG:3857'
    })
  });

  var layerSwitcher = new ol.control.LayerSwitcher({
    tipLabel: 'Légende', // Optional label for button
    groupSelectStyle: 'children' // Can be 'children' [default], 'group' or 'none'
  });
  map.addControl(layerSwitcher);
})();
