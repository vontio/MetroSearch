var nearestStation = [],
    earthLatLon,
    marsLonLat, currentCity = $("#CurrentCity").text(),
    map, t;

function showLocation(position) {
    eWJ = [position.coords.latitude, position.coords.longitude];
    $("#earth").html(eWJ[0] + " " + eWJ[1]);
    initMap();
    toMars(eWJ);
}

function initMap() {
    $("#walkMap").html("");
    map = new AMap.Map('walkMap', {
        resizeEnable: true,
        keyboardEnable: true
    });
}

function showPicture() {
    search("Walking");
}

function search(Mode) {
    if (t) t.clear();

    transOptions = {
        map: map,
        city: currentCity,
        cityd: currentCity
    };
    if (Mode === "Transfer") {
        t = new AMap.Transfer(transOptions);
    } else if (Mode === "Driving") {
        t = new AMap.Driving(transOptions);
    } else {
        t = new AMap.Walking(transOptions);
    }
    t.search(marsLonLat, nearestStation[1]);
}

function obtainNeighbor() {
    dict = {
        type: '150500',
    };
    if (currentCity != "") {
        dict["city"] = currentCity;
    }
    var placeSearch = new AMap.PlaceSearch(dict);
    var cpoint = [marsLonLat[0], marsLonLat[1]];
    placeSearch.searchNearBy("地铁站", cpoint, 50000, function(status, result) {
        pois = result["poiList"]["pois"];
        sN = pois[0]["name"].split("(")[0];
        $("#fromInput").val(sN);
        nearestStation.push(sN);
        nearestStation.push([pois[0]["location"]["lng"], pois[0]["location"]["lat"]]);
        showPicture();
    });
}

function obtainLocation() {
    var placeSearch = new AMap.Geocoder();
    var cpoint = [marsLonLat[0], marsLonLat[1]];
    placeSearch.getAddress(cpoint, function(status, result) {
        console.log(result["regeocode"]["addressComponent"]["city"]);
        a = result["regeocode"]["addressComponent"]["city"].replace("市", "")
        $("#demo").html("您当前位于");
        $("#demo").append($("<a>", {
            href: a,
            "class": "btn btn-info CityList"
        }).html(result["regeocode"]["formattedAddress"]));
    });
}

function toMars(eWJ) {
    url = "https://restapi.amap.com/v3/assistant/coordinate/convert";
    $.get(url, {
        key: GaodeKey,
        locations: eWJ[1] + "," + eWJ[0],
        coordsys: "gps"
    }, function(data) {
        marsLonLat = data["locations"].split(",");
        $("#mars").html(marsLonLat[1] + " " + marsLonLat[0]);
        if (currentCity != "") {
            obtainNeighbor();
        } else {
            obtainLocation();
        }
    });
}

function dN(s) {
    $("#demo").html(s);
}

function gL() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showLocation, sE);
    } else {
        dN("浏览器不支持定位。");
    }
}

function sE(error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            dN("您拒绝提供位置信息，因此我们无法为您定位。");
            break;
        case error.POSITION_UNAVAILABLE:
            dN("我们不知道您在哪儿。");
            break;
        case error.TIMEOUT:
            dN("暂时无法获得位置信息。");
            break;
        case error.UNKNOWN_ERROR:
            dN("发生了无法处理的意外事件。");
            break;
    }
}

function rS() {
    a = $("#navbarcontainer").height() + 20;
    $("body").attr("style", "padding-top: " + a + "px");
}
$(window).resize(rS);
$(function() {
    rS();
    if ($("#CurrentCity").text() != "") {
        init();
    }
    gL();
});