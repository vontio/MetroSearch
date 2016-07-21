var nearestStation = [],
    earthLatLon,
    marsLonLat, currentCity, map;

function showLocation(position) {
    eWJ = [position.coords.latitude, position.coords.longitude];
    $("#earth").html(eWJ[0] + " " + eWJ[1]);
    toMars(eWJ);
}

function showPicture() {
    $("#walkMap").html("");
    map = new AMap.Map('walkMap', {
        resizeEnable: true,
        keyboardEnable: true
    });
    search("Walking");
}

function search(Mode) {
    transOptions = {
        map: map,
        city: currentCity,
        cityd: currentCity
    };
    start = marsLonLat;
    end = nearestStation[1];
    if (Mode === "Transfer") {
        AMap.service('AMap.Transfer', function() {
            var t = new AMap.Transfer(transOptions);
            t.search(start, end);
        });
    } else {
        if (Mode === "Driving") {
            AMap.service('AMap.Driving', function() {
                var t = new AMap.Driving(transOptions);
                t.search(start, end);
            });
        } else {
            AMap.service('AMap.Walking', function() {
                var t = new AMap.Walking(transOptions);
                t.search(start, end);
            });
        }
    }
}

function obtainNeighbor() {
    currentCity = $("#CurrentCity").text();
    url = "https://restapi.amap.com/v3/place/around";
    dict = {
        key: GaodeKey,
        location: marsLonLat[0] + "," + marsLonLat[1],
        keywords: "地铁站",
        radius: 50000
    };
    if (currentCity != "") {
        dict["city"] = currentCity;
    }
    $.get(url, dict, function(data) {
        pois = data["pois"]
        sN = pois[0]["name"].split("(")[0];
        currentCity = pois[0]["cityname"].replace("市", "");
        $("#demo").html("您当前位于");
        $("#demo").append($("<a>", {
            href: currentCity,
            "class": "btn btn-info CityList"
        }).html(currentCity));
        $("#demo").append("，最近的地铁站是" + sN);
        $("#fromInput").val(sN);
        nearestStation.push(sN);
        nearestStation.push(pois[0]["location"].split(","));
        showPicture();
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
        obtainNeighbor();
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