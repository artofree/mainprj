var map;
var isNeedHistory = true;
function initialize() {
    var mapOptions = {
        zoom: parms.zoom,
        center: new google.maps.LatLng(parms.lt, parms.ln)
    };
    map = new google.maps.Map(document.getElementById('map-canvas'),
        mapOptions);

    google.maps.event.addListener(map, 'idle', function () {
        var mapBounds = map.getBounds();
        var ne = mapBounds.getNorthEast();
        var sw = mapBounds.getSouthWest();
        ///请求该区域当前zoom下的图片内容：
        $.getJSON(parms.jsonurl, {
            'nelt': ne.lat(),
            'neln': ne.lng(),
            'swlt': sw.lat(),
            'swln': sw.lng(),
            'zoom': map.getZoom()
        }, function (ret) {
            //返回值 ret 在这里是一个列表
            //for(var index =0 ;index <ret.length ;index ++) {
            for (var index in ret) {
                var photoArr = ret[index];
                var lt = photoArr[1];
                var ln = photoArr[2];
                var myLatLng = new google.maps.LatLng(Number(lt), Number(ln));
                var beachMarker = new google.maps.Marker({
                    position: myLatLng,
                    map: map,
                    icon: photoArr[0]
                });
            }
        })
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
        else{
            isNeedHistory =true;
        }
    });
    ///
    google.maps.event.addListener(map, 'dragstart', function () {
        var mapBounds = map.getBounds();
    });
    ///要先隐藏或删除已有的marker
    google.maps.event.addListener(map, 'zoom_changed', function () {
        var mapBounds = map.getBounds();
    });
}
google.maps.event.addDomListener(window, 'load', initialize);
///支持后退：
window.addEventListener('popstate', function (e) {
    if (history.state) {
        var state = e.state;
        var myLatLng = new google.maps.LatLng(Number(state.clt), Number(state.cln));
        map.setCenter(myLatLng);
        map.setZoom(Number(state.zoom));
        isNeedHistory =false;
    }
}, false);

