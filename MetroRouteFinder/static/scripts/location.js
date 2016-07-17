function showLocation(position) {
    EarthLatLon = [position.coords.latitude, position.coords.longitude];
    $("#earth").html(EarthLatLon[0] + " " + EarthLatLon[1]);
    toMars(EarthLatLon);
}

function showPicture(start, end, endName) {
    var url = "https://m.amap.com/navi/?";
    url += ("start=" + start);
    url += ("&dest=" + end);
    url += ("&destName=" + endName);
    url += ("&naviby=bus&key=" + DisplayKey);
    $("#walkMap").attr({
        src: url
    });
}

function obtainStationLocation(StationName) {
    city = $("#CurrentCity").text();
    url = "http://restapi.amap.com/v3/geocode/geo"
    dict = {
        key: GaodeKey,
        address: StationName + "地铁站",
        city: city
    }
    $.get("/Station/" + StationName, function(a) {});
}

function obtainNeighbor(MarsLonLat) {
    city = $("#CurrentCity").text();
    url = "https://restapi.amap.com/v3/place/around";
    dict = {
        key: GaodeKey,
        location: MarsLonLat[0] + "," + MarsLonLat[1],
        keywords: "地铁站"
    }
    if (city != "") {
        dict["city"] = city;
        dict["radius"] = 50000;
    }
    $.get(url, dict, function(data) {
        pois = data["pois"]
        StationName = pois[0]["name"].split("(")[0];
        StationLonLat = pois[0]["location"]
        CityName = pois[0]["cityname"].replace("市", "");
        $("#demo").html("您当前位于");
        $("#demo").append($("<a>", {
            href: CityName,
            "class": "btn btn-info CityList"
        }).html(CityName));
        $("#demo").append("，最近的地铁站是" + StationName + "站");
        $("#fromInput").val(StationName);
        showPicture(MarsLonLat[0] + "," + MarsLonLat[1], StationLonLat, StationName + "站");
    });
}

function toMars(EarthLatLon) {
    url = "https://restapi.amap.com/v3/assistant/coordinate/convert";
    $.get(url, {
        key: GaodeKey,
        locations: EarthLatLon[1] + "," + EarthLatLon[0],
        coordsys: "gps"
    }, function(data) {
        MarsLonLat = data["locations"].split(",");
        $("#mars").html(MarsLonLat[1] + " " + MarsLonLat[0]);
        obtainNeighbor(MarsLonLat);
    });
}

function displayNotice(string) {
    $("#status").html(string);
}

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showLocation, showError);
    } else {
        displayNotice("浏览器不支持定位。");
    }
}

function showError(error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            displayNotice("您拒绝提供位置信息，因此我们无法为您定位。");
            break;
        case error.POSITION_UNAVAILABLE:
            displayNotice("我们不知道您在哪儿。");
            break;
        case error.TIMEOUT:
            displayNotice("暂时无法获得位置信息。");
            break;
        case error.UNKNOWN_ERROR:
            displayNotice("发生了无法处理的意外事件。");
            break;
    }
}
$(function() {
    resize();
    getLocation();
});

function resize()
{
    a = $("#navbarcontainer").height() + 20;
    $("body").attr("style", "padding-top: "+ a +"px");
}

$(window).resize(resize);