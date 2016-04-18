function mapMarkerLayer(name, imgSrc, pos, scale) {
    var icon = new ol.Feature({
        geometry: new ol.geom.Point(
            ol.proj.fromLonLat(pos)
        ),
        name: name
    });
    var iconStyle = new ol.style.Style({
        image: new ol.style.Icon({
            scale: scale,
            anchor: [0.5, 1],
            anchorXUnits: 'fraction',
            anchorYUnits: 'fraction',
            src: imgSrc
        }),
    });
    return new ol.layer.Vector({
        source: new ol.source.Vector({
            features: [icon]
        }),
        style: iconStyle
    });
}
