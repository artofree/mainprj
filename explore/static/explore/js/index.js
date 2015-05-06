var map;
///用于记录后退历史
var isNeedHistory = true;
///记录已请求过的

///
function getNormalizedCoord(coord, zoom) {
    var y = coord.y;
    var x = coord.x;

    // tile range in one direction range is dependent on zoom level
    // 0 = 1 tile, 1 = 2 tiles, 2 = 4 tiles, 3 = 8 tiles, etc
    var tileRange = 1 << zoom;

    // don't repeat across y-axis (vertically)
    if (y < 0 || y >= tileRange) {
        return null;
    }

    // repeat across x-axis
    if (x < 0 || x >= tileRange) {
        x = (x % tileRange + tileRange) % tileRange;
    }

    return {
        x: x,
        y: y
    };
}
/////////////////////////////////////////////////////////////////////////////////////////////
function CoordMapType(tileSize) {
    this.tileSize = tileSize;
}
CoordMapType.prototype.getTile = function (coord, zoom, ownerDocument) {
    var normalizedCoord = getNormalizedCoord(coord, zoom);
    var div = ownerDocument.createElement('div');
    var theUrl = '/photolayer/' + zoom + ',' + normalizedCoord.x + ',' + normalizedCoord.y + '.jpg';
    div.innerHTML = '<img src="' + theUrl + '" width="256" height="256" />';
    //div.innerHTML = '<img src="/static/test.png" width="256" height="256" />';
    div.style.borderStyle = 'hidden';
    return div;
};

function initialize() {
    var mapOptions = {
        zoom: parms.zoom,
        center: new google.maps.LatLng(parms.lt, parms.ln),
        streetViewControl: false,
        mapTypeControlOptions: {
            mapTypeIds: ['moon']
        }
    };
    map = new google.maps.Map(document.getElementById('map-canvas'),
        mapOptions);
    map.overlayMapTypes.insertAt(
        0, new CoordMapType(new google.maps.Size(256, 256)));

    ///存储状态
    google.maps.event.addListener(map, 'tilesloaded', function () {
        if (isNeedHistory) {
            var url = '/explore/';
            var state = {
                clt: map.getCenter().lat(),
                cln: map.getCenter().lng(),
                zoom: map.getZoom()
            };
            url = url + String(state.clt) + ',' + String(state.cln) + ',' + String(state.zoom);
            window.history.pushState(state, document.title, url);
        }
        else {
            isNeedHistory = true;
        }
    });
}
google.maps.event.addDomListener(window, 'load', initialize);

///后退：
window.addEventListener('popstate', function (e) {
    if (history.state) {
        var state = e.state;
        var myLatLng = new google.maps.LatLng(Number(state.clt), Number(state.cln));
        map.setCenter(myLatLng);
        map.setZoom(Number(state.zoom));
        isNeedHistory = false;
    }
}, false);

