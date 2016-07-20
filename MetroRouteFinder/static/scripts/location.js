var nearestStation = [],
    myPosition = "";

function sL(position) {
    eWJ = [position.coords.latitude, position.coords.longitude];
    $("#earth").html(eWJ[0] + " " + eWJ[1]);
    toMars(eWJ);
}

function showPicture(start, end, endName) {
    $("#walkMap").html("");
    var map = new AMap.Map('walkMap');
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

function obtainNeighbor(mJW) {
    cK = $("#CurrentCity").text();
    url = "https://restapi.amap.com/v3/place/around";
    mP = mJW[0] + "," + mJW[1];
    dict = {
        key: GaodeKey,
        location: mP,
        keywords: "地铁站",
        radius: 50000
    }
    if (cK != "") {
        dict["city"] = cK;
    }
    $.get(url, dict, function(data) {
        pois = data["pois"]
        sN = pois[0]["name"].split("(")[0];
        cN = pois[0]["cityname"].replace("市", "");
        $("#demo").html("您当前位于");
        $("#demo").append($("<a>", {
            href: cN,
            "class": "btn btn-info CityList"
        }).html(cN));
        $("#demo").append("，最近的地铁站是" + sN);
        $("#status").html("获取成功");
        $("#fromInput").val(sN);
        $("#location").html(cN + "市" + sN + "站附近");
        showPicture(mP, pois[0]["location"], sN);
    });
}

function toMars(eWJ) {
    url = "https://restapi.amap.com/v3/assistant/coordinate/convert";
    $.get(url, {
        key: GaodeKey,
        locations: eWJ[1] + "," + eWJ[0],
        coordsys: "gps"
    }, function(data) {
        mJW = data["locations"].split(",");
        $("#mars").html(mJW[1] + " " + mJW[0]);
        obtainNeighbor(mJW);
    });
}

function dN(s) {
    $("#status").html(s);
}

function gL() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(sL, sE);
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