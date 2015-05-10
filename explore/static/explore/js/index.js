///关于快速zoom bug可用计时器，在zoom之后设定计时器，同时设定地图的minzoom和maxzoom，既禁止缩放，过期后再恢复正常
///关于不用eventsource的方案：gettiles时请求tilesinfo，服务端收到请求即计算，然后将照片缓存到stringio
var map;
///用于记录后退历史
var isNeedHistory = true;
///记录已请求过的
///当前点击将触发的图片信息
var nowPhoto = null;
var infowindow = null;
var rightPhotos = [];
///接收推送,并按层-》tile-》rect方式组织
var allLayer = [];
var source = new EventSource("/getTilesInfo/");
source.onmessage = function (event) {
    if (event.data == "")
        return;
    var data = JSON.parse(event.data);
    for (var i1 = 0; i1 < data.length; i1++) {
        var ret = data[i1];
        if (allLayer[Number(ret["zoom"])] === undefined) {
            allLayer[Number(ret["zoom"])] = [];
        }
        var theLayer = allLayer[Number(ret["zoom"])];
        for (var i2 = 0; i2 < theLayer.length; i2++) {
            if (theLayer[i2]["x"] == Number(ret["x"]) && theLayer[i2]["y"] == Number(ret["y"]))
                return;
        }
        var theTile = [];
        theTile["x"] = Number(ret["x"]);
        theTile["y"] = Number(ret["y"]);
        var nepoint1 = new google.maps.LatLng(Number(ret["nelt"]), Number(ret["neln"]));
        var swpoint1 = new google.maps.LatLng(Number(ret["swlt"]), Number(ret["swln"]));
        theTile["rect"] = new google.maps.LatLngBounds(swpoint1, nepoint1);
        var elements = ret["elements"];
        for (var i = 0; i < elements.length; i++) {
            var theElement = [];
            theElement["photoid"] = elements[i][0];
            var nepoint = new google.maps.LatLng(Number(elements[i][1]), Number(elements[i][2]));
            var swpoint = new google.maps.LatLng(Number(elements[i][3]), Number(elements[i][4]));
            theElement["rect"] = new google.maps.LatLngBounds(swpoint, nepoint);
            theElement["point"] = new google.maps.LatLng(Number(elements[i][5]), Number(elements[i][6]));
            theTile.push(theElement);
        }
        theLayer.push(theTile);
    }
};
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

    ///请求tile信息：
    //$.getJSON(parms.jsonurl, {
    //    'x': normalizedCoord.x,
    //    'y': normalizedCoord.y,
    //    'zoom': map.getZoom()
    //}, function (ret) {
    //    //返回值 ret 在这里是一个列表
    //    //for(var index =0 ;index <ret.length ;index ++) {
    //    var bigPhotos = ret;
    //});

    return div;
};

CoordMapType.prototype.releaseTile = function (node) {
    var zoom = map.getZoom();
    var tilex = node.Aa.x;
    var tiley = node.Aa.y;
    var theLayer = allLayer[zoom];
    if (theLayer != undefined) {
        for (var item in theLayer) {
            if (theLayer[item]["x"] == tilex && theLayer[item]["y"] == tiley) {
                theLayer.splice(item, 1);
            }
        }
    }
};

function initialize() {
    var mapOptions = {
        zoom: parms.zoom,
        minZoom: 3,
        center: new google.maps.LatLng(parms.lt, parms.ln),
        streetViewControl: false,
        draggableCursor: 'default',
        draggingCursor: 'move',
        mapTypeControlOptions: {
            mapTypeIds: ['moon']
        }
    };
    map = new google.maps.Map(document.getElementById('map-canvas'),
        mapOptions);
    map.overlayMapTypes.insertAt(
        0, new CoordMapType(new google.maps.Size(256, 256)));

    ///zoomchange:
    google.maps.event.addListener(map, 'zoom_changed', function () {
        //allLayer = [];
    });
    ///监听鼠标点击，从nowphoto里获得并呈现
    google.maps.event.addListener(map, 'click', function (event) {
        if (nowPhoto) {
            if (infowindow) {
                infowindow.close();
            }
            var imgscr = '/static/photos/' + nowPhoto["photoid"] + '.jpg';
            infowindow = new google.maps.InfoWindow({
                content: '<img src="' + imgscr + '" width="256" height="256" />',
                position: nowPhoto["point"]
            });
            infowindow.open(map);
        } else {
            if (infowindow) {
                infowindow.close();
                infowindow = null;
            }
        }
    });
    ///监听鼠标移动，切换cursor
    google.maps.event.addListener(map, 'mousemove', function (event) {
        var zoom = map.getZoom();
        ///找不到说明层tile信息还没来
        if (allLayer[zoom] === undefined) {
            nowPhoto = null;
            return
        }
        var theLayer = allLayer[zoom];
        var isInTiles = false;
        for (var i = 0; i < theLayer.length; i++) {
            if (isInTiles)
                break;
            var theTile = theLayer[i];
            if (theTile["rect"].contains(event.latLng)) {
                for (var index = 0; index < theTile.length; index++) {
                    if (theTile[index]["rect"].contains(event.latLng)) {
                        nowPhoto = [];
                        nowPhoto["point"] = theTile[index]["point"];
                        nowPhoto["photoid"] = theTile[index]["photoid"];
                        isInTiles = true;
                        break;
                    }
                }
            }
        }
        if (isInTiles) {
            ///换图标
            map.setOptions({draggableCursor: 'pointer'});
        }
        else {
            if (nowPhoto) {
                nowPhoto = null;
                ///换图标
                map.setOptions({draggableCursor: 'default'});
            }
        }
    });

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

