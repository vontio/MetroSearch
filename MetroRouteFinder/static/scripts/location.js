function displayNotice(string) {
    $("#demo").html(string);
}

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showLocation, showError);
    } else {
        displayNotice("浏览器不支持定位。");
    }
}

function showLocation(position) {
    EarthLatLon = [position.coords.latitude, position.coords.longitude]
    toMars(EarthLatLon);
}

function obtainNeighbor(MarsLonLat) {
    url = "https://restapi.amap.com/v3/place/around";
    $.get(url, {
        key: GaodeKey,
        location: MarsLonLat[0] + "," + MarsLonLat[1],
        keywords: "地铁站",
    }, function(data) {
        pois = data["pois"]
        StationName = pois[0]["name"].split("(")[0];
        CityName = pois[0]["cityname"].replace("市", "");
        $("#demo").html("您当前位于");
        $("#demo").append($("<a>", {
            href: CityName
        }).html(CityName));
        $("#demo").append("，最近的地铁站是"+StationName+"站");
        $("#fromInput").val(StationName);
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
        obtainNeighbor(MarsLonLat);
    });
}

function showError(error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            displayNotice("您拒绝提供位置信息，因此我们无法为您定位。");
            break;
        case error.POSITION_UNAVAILABLE:
            displayNotice("位置信息暂时不可用。");
            break;
        case error.TIMEOUT:
            displayNotice("暂时无法获得位置信息。");
            break;
        case error.UNKNOWN_ERROR:
            displayNotice("发生了无法处理的意外事件。");
            break;
    }
}