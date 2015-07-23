///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///关于快速zoom bug可用计时器，在zoom之后设定计时器，同时设定地图的minzoom和maxzoom，既禁止缩放，过期后再恢复正常
///关于不用eventsource的方案：gettiles时请求tilesinfo，服务端收到请求即计算，然后将照片缓存到stringio
var map;
///用于记录后退历史
var isNeedHistory = true;
///记录已请求过的
///当前点击将触发的图片信息
var nowPhoto = null;
///弹出框，全局只有一个
var infowindow = null;
///接收推送,并按层-》tile-》rect方式组织
var allLayer = [];
///右侧图片
var rightPhotos = [];
///info是否打开
var isInfoWindow = false;
///用于确认infowindow由map还是右侧发起打开
var isInfoRightClick = false;


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

function getInfoWindowContent(pid, pfile) {
    ///初始化like以及favorite
    var imgscr = '/static/photos/' + pfile + '.jpg';

    $.get(parms.genurl, {'reqType': 'isLike', 'pid': pid}, function (ret) {
        if (ret == '0') {
            $("#likeCount").attr('isLike', '0');
            $("#imgLike").attr('src', '/static/icons/heart_grey_16.png');
        } else {
            $("#likeCount").attr('isLike', '1');
            $("#imgLike").attr('src', '/static/icons/heart_red_16.png');
        }
    });
    $.get(parms.genurl, {'reqType': 'isFavorite', 'pid': pid}, function (ret) {
        if (ret == '0') {
            $("#favoriteCount").attr('isFavorite', '0');
            $("#imgFavorite").attr('src', '/static/icons/star_grey_16.png');
        } else {
            $("#favoriteCount").attr('isFavorite', '1');
            $("#imgFavorite").attr('src', '/static/icons/star_red_16.png');
        }
    });
    $.get(parms.genurl, {'reqType': 'likeCount', 'pid': pid}, function (ret) {
        $("#likeCount").html(ret);
    });
    $.get(parms.genurl, {'reqType': 'favoriteCount', 'pid': pid}, function (ret) {
        $("#favoriteCount").html(ret);
    });

    var content = '<div style="width: 192px">' +
        '<img class="img-rounded" src="' + imgscr + '" style="height: 192px;width: 192px">' +
        '<div style="height: 30px;margin-top: 20px">' +
        '<div id="likediv" style="float: left;margin-left: 1px"><span>喜欢 </span>' +
        '<img src="" id="imgLike" style="cursor: pointer;"> ' +
        '<span id="likeCount" isLike="0" pid="' + pid + '"></span></div>' +
        '<div id="favoritediv" style="float: right;margin-right: 1px"><span>收藏 </span>' +
        '<img src="" id="imgFavorite" style="cursor: pointer;"> ' +
        '<span id="favoriteCount" isFavorite="0" pid="' + pid + '"></span></div>' +
        '</div></div>';

    return content;
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
    div.style.borderStyle = 'hidden';

    ///如果alllayer里没有这个tile
    var isInAllLayer = false;
    if (allLayer[zoom] != undefined) {
        var theLayer = allLayer[zoom];
        for (var i1 = 0; i1 < theLayer.length; i1++) {
            if (theLayer[i1]["x"] == normalizedCoord.x && theLayer[i1]["y"] == normalizedCoord.y) {
                isInAllLayer = true;
                break;
            }
        }
    }
    if (!isInAllLayer) {
        ///请求tile内容信息：
        $.getJSON(parms.jsonurl, {
            'x': normalizedCoord.x,
            'y': normalizedCoord.y,
            'zoom': zoom
        }, function (ret) {
            if (allLayer[Number(ret["zoom"])] === undefined) {
                allLayer[Number(ret["zoom"])] = [];
            }
            var theLayer = allLayer[Number(ret["zoom"])];
            var theTile = [];
            theTile["x"] = Number(ret["x"]);
            theTile["y"] = Number(ret["y"]);
            var nepoint1 = new google.maps.LatLng(Number(ret["nelt"]), Number(ret["neln"]));
            var swpoint1 = new google.maps.LatLng(Number(ret["swlt"]), Number(ret["swln"]));
            theTile["rect"] = new google.maps.LatLngBounds(swpoint1, nepoint1);
            var elements = ret["elements"];
            for (var i = 0; i < elements.length; i++) {
                var theElement = [];
                theElement["pfile"] = elements[i][0];
                theElement["pid"] = elements[i][7];
                var nepoint = new google.maps.LatLng(Number(elements[i][1]), Number(elements[i][2]));
                var swpoint = new google.maps.LatLng(Number(elements[i][3]), Number(elements[i][4]));
                theElement["rect"] = new google.maps.LatLngBounds(swpoint, nepoint);
                theElement["point"] = new google.maps.LatLng(Number(elements[i][5]), Number(elements[i][6]));
                theTile.push(theElement);
            }
            theLayer.push(theTile);
        });
    }

    return div;
};

CoordMapType.prototype.releaseTile = function (node) {
    //var zoom = map.getZoom();
    //var tilex = node.Aa.x;
    //var tiley = node.Aa.y;
    //var theLayer = allLayer[zoom];
    //if (theLayer != undefined) {
    //    for (var item in theLayer) {
    //        if (theLayer[item]["x"] == tilex && theLayer[item]["y"] == tiley) {
    //            theLayer.splice(item, 1);
    //        }
    //    }
    //}
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
    infowindow = new google.maps.InfoWindow();
    ///关闭infowindow：
    google.maps.event.addListener(infowindow, 'closeclick', function () {
        isInfoRightClick = false;
    });
    allLayer[parms.zoom] = [];
    map = new google.maps.Map(document.getElementById('map-canvas'),
        mapOptions);
    map.overlayMapTypes.insertAt(
        0, new CoordMapType(new google.maps.Size(256, 256)));

    ///zoomchange:
    google.maps.event.addListener(map, 'zoom_changed', function () {

    });
    ///监听鼠标点击，从nowphoto里获得并呈现
    google.maps.event.addListener(map, 'click', function (event) {
        if (nowPhoto) {
            if (isInfoWindow) {
                infowindow.close();
            }
            theContent = getInfoWindowContent(nowPhoto["pid"], nowPhoto["pfile"]);
            infowindow.setContent(theContent);
            infowindow.setPosition(nowPhoto["point"]);
            infowindow.open(map);
            isInfoWindow = true;
            isInfoRightClick = false;
        } else {
            if (isInfoWindow) {
                infowindow.close();
                isInfoWindow = false;
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
                        nowPhoto["pfile"] = theTile[index]["pfile"];
                        nowPhoto["pid"] = theTile[index]["pid"];
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
    ///获得右栏图片列表
    google.maps.event.addListener(map, 'idle', function () {
        var mapBounds = map.getBounds();
        var ne = mapBounds.getNorthEast();
        var sw = mapBounds.getSouthWest();
        ///请求该区域当前zoom下的图片内容：
        rightPhotos = [];
        $.getJSON(parms.plisturl, {
            'nelt': ne.lat(),
            'neln': ne.lng(),
            'swlt': sw.lat(),
            'swln': sw.lng(),
            'zoom': map.getZoom()
        }, function (ret) {
            //返回值 ret 在这里是一个列表
            rightPhotos = ret;
            if (isInfoWindow && isInfoRightClick) {
                var i = 0;
            }
            else {
                initFun();
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

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
var minleftwidth = 5;
var comrightwidth = 500;
var safeblank = 10;
var rightpadding = 20;
var tabheight = 50;
var navheight = 50;
var navtopmargin = 50;

var loop = 0;
var isLastLoop = false;
function loopFun(theLoop) {
    var rightWidth;
    var leftWidth;
    var width = $(window).width();
    var thumbdiv = $("#thumbdiv");
    thumbdiv.empty();
    if (width > comrightwidth + safeblank + minleftwidth) {
        rightWidth = comrightwidth - 2 * rightpadding;
        leftWidth = width - comrightwidth - safeblank;
    }
    if (width <= comrightwidth + safeblank + minleftwidth) {
        leftWidth = minleftwidth;
        rightWidth = width - safeblank - minleftwidth - 2 * rightpadding;
    }
    $("#map-canvas").width(leftWidth);
    var rightdiv = $("#rightdiv");
    rightdiv.width(rightWidth);
    $("#tabdiv").height(tabheight);
    var navdiv = $("#navdiv");
    navdiv.height(navheight);
    thumbdiv.height(rightdiv.height() - tabheight - navheight - navtopmargin);

    ///计算图片元素个数
    var theHeight = thumbdiv.height();
    var theWidth = thumbdiv.width();
    ///可容图片数
    var theCount = Math.floor(theHeight / 110) * Math.floor(theWidth / 110);
    ///实际图片数
    var realCount = theCount;
    ///设置图片
    isLastLoop = false;
    if (rightPhotos.length - theLoop * theCount < theCount) {
        realCount = rightPhotos.length - theLoop * theCount;
        isLastLoop = true;
    }
    for (var index = theLoop * theCount; index < theLoop * theCount + realCount; index++) {
        var imgscr = '/static/photos/' + rightPhotos[index][1] + '.jpg';
        var pid = rightPhotos[index][0];
        var pfile = rightPhotos[index][1];
        var lt = rightPhotos[index][3];
        var ln = rightPhotos[index][4];
        thumbdiv.append('<div style="float: left ;height: 114px ;width: 114px">' +
        '<a href="#" class="thePhoto" pid="' + pid + '" pfile ="' + pfile + '" lt="' + lt + '" ln="' + ln + '">' +
        '<img class="img-thumbnail" src="' + imgscr + '" style="width: 100px ;height: 100px ;background: rgb(255, 255, 255); ">' +
        '</a>' +
        '</div>');
    }
    ///设置翻页
    var backdiv = $("#backdiv");
    backdiv.empty();
    if (isLastLoop) {
        backdiv.append('<h5 style="color: grey">下一页<span class="glyphicon glyphicon-triangle-right" aria-hidden="true"></span></h5>');
    }
    else {
        backdiv.append('<a href="#" id="backloop"><h5>下一页<span class="glyphicon glyphicon-triangle-right" aria-hidden="true"></span></h5></a>');
    }
    var frontdiv = $("#frontdiv");
    frontdiv.empty();
    if (theLoop == 0) {
        frontdiv.append('<h5 style="color: grey"><span class="glyphicon glyphicon-triangle-left" aria-hidden="true"></span>上一页</h5>');
    }
    else {
        frontdiv.append('<a href="#" id="frontloop"><h5><span class="glyphicon glyphicon-triangle-left" aria-hidden="true"></span>上一页</h5></a>');
    }
}

function initFun() {
    loop = 0;
    loopFun(loop);
}


$(document).ready(function () {
    $(window).resize(function () {
        initFun();
    });
});

$(document).ready(function () {
    initFun();
});

///
$(document).ready(function () {
    $(document).on("click", ".thePhoto", function () {
        var pid = $(this).attr("pid");
        var pfile = $(this).attr("pfile");
        var lt = $(this).attr("lt");
        var ln = $(this).attr("ln");

        if (isInfoWindow) {
            infowindow.close();
        }
        theContent = getInfoWindowContent(pid, pfile);
        infowindow.setContent(theContent);
        infowindow.setPosition(new google.maps.LatLng(Number(lt), Number(ln)));
        infowindow.open(map);
        isInfoWindow = true;
        isInfoRightClick = true;
    });
});

///frontloop
$(document).ready(function () {
    $(document).on("click", "#frontloop", function () {
        loop -= 1;
        loopFun(loop);
    });
});
///backloop
$(document).ready(function () {
    $(document).on("click", "#backloop", function () {
        loop += 1;
        loopFun(loop);
    });
});
///
$(document).ready(function () {
    $(document).on("click", "#imgLike", function () {
        var jlikeCount = $("#likeCount");
        if (jlikeCount.attr('isLike') == '1') {
            alert('您已点赞');
        }
        else {
            var likeCount = jlikeCount.html();
            jlikeCount.html(Number(likeCount) + 1);
            jlikeCount.attr('isLike', '1');
            $("#imgLike").attr('src', '/static/icons/heart_red_16.png');
            $.get(parms.genurl, {'reqType': 'addLike', 'pid': jlikeCount.attr('pid')}, function (ret) {
            });
        }
    });
});

$(document).ready(function () {
    $(document).on("click", "#imgFavorite", function () {
        var jfavoriteCount = $("#favoriteCount");
        if (jfavoriteCount.attr('isFavorite') == '1') {
            alert('您已收藏');
        }
        else {
            var favoriteCount = jfavoriteCount.html();
            jfavoriteCount.html(Number(favoriteCount) + 1);
            jfavoriteCount.attr('isFavorite', '1');
            $("#imgFavorite").attr('src', '/static/icons/star_red_16.png');
            $.get(parms.genurl, {'reqType': 'addFavorite', 'pid': jfavoriteCount.attr('pid')}, function (ret) {
            });
        }
    });
});