var StationList = [],
    VirtualTransfers = [],
    Transfers = [],
    lineColors = [];

function buildTipsList(c) {
    var a = [];
    StationList.forEach(function(b) {
        if (0 <= b.text().indexOf(c)) {
            a.push(b);
        }
    });
    return a;
}

function find() {
    $("#paths").html("");
    $.post("Route/" + $("#fromInput").val() + "/" + $("#toInput").val() + "/",
        function(a) {
            Routes = a.Routes;
            Modes = a.Modes;
            for (a = 0; a < Routes.length; a++) {
                var ListElement = $("<div>", {
                        "class": "panel panel-default"
                    }),
                    f = $("<div>", {
                        id: "heading" + a,
                        role: "tab",
                        "class": "panel-heading"
                    }),
                    h = $("<h4>", {
                        "class": "panel-title"
                    }),
                    g = $("<a>", {
                        href: "#collapse" + a,
                        role: "button",
                        "data-toggle": "collapse",
                        "data-parent": "#path" + a,
                        "aria-expanded": 0 === a ? "true" : "false",
                        "aria-controls": "collapse" + a
                    }).html("路线 " + (a + 1).toString() + " "),
                    correspondence = {
                        "站数少": "success",
                        "换乘少": "primary",
                        "不出站": "warning"
                    };
                for (var b = 0; b < Modes[a].length; b++) {
                    var c = "info";
                    if (correspondence.hasOwnProperty(Modes[a][b])) {
                        c = correspondence[Modes[a][b]];
                    }
                    g.append(
                        $("<span>", {
                            "class": "routetype label label-" + c
                        }).html(Modes[a][b])
                    );
                }
                ListElement.append(f.html(h.html(g)));
                var d = $("<div>", {
                        id: "collapse" + a,
                        "class": "panel-collapse collapse in",
                        role: "tabpanel",
                        "aria-labelledby": "heading" + a
                    }),
                    e = $("<ul>", {
                        "class": "list-group"
                    }),
                    Route = Routes[a],
                    pre = "Route" + a;
                for (var b = 0; b < Route.Stations.length + Route.Lines.length; b++) {
                    if (0 == b % 2) {
                        f = $("<li>", {
                            "class": "StationName list-group-item",
                            id: pre + "Station" + b
                        }).html(Route.Stations[b / 2]);
                    } else {
                        h = Route.Lines[(b - 1) / 2];
                        f = $("<li>", {
                            "class": "list-group-item"
                        });
                        for (var c in h) {
                            if (c > 0) {
                                f.append("，或：<br>");
                            }
                            g = h[c];
                            f.append($("<span>", {
                                "class": "LineName",
                                id: pre + "Line" + b,
                                style: "background-color:" + lineColors[g.Line].Color
                            }).html(g.Line));
                            f.append($("<span>", {
                                "class": "Direction",
                                id: pre + "Direction" + b
                            }).html(g.Direction));
                            f.append("方向，" + g.Distance + " 站");
                        }
                    }
                    e.append(f);
                }
                ListElement.append(d.append(e));
                $("#paths").append(
                    $("<div>", {
                        "class": "panel-group col-xs-12 col-sm-6 col-md-4",
                        id: "path" + a,
                        role: "tablist",
                        "aria-multiselectable": "true"
                    }).html(ListElement));
                for (var b = 2; b < Route.Stations.length + Route.Lines.length - 2; b += 2) {
                    StationName = Route.Stations[b / 2];
                    PreviousLine = Route.Lines[(b - 2) / 2];
                    NextLine = Route.Lines[b / 2];
                    for (var l in PreviousLine) {
                        for (var m in NextLine) {
                            var f = [StationName, PreviousLine[l], NextLine[m]];
                            var VT = []
                            for (var n in VirtualTransfers) {
                                if (VirtualTransfers[n][0] == f[0]) {
                                    VT.push(VirtualTransfers[n]);
                                }
                            }
                            for (var n in Transfers) {
                                if (Transfers[n][0] == f[0]) {
                                    VT.push(Transfers[n]);
                                }
                            }
                            for (var n in VT) {
                                g = VT[n];
                                if ((g[1] == f[1].Line && g[2] == f[2].Line) || (g[1] == f[2].Line && g[2] == f[1].Line)) {
                                    $("#Route" + a + "Station" + b).html(StationName + " ");
                                    $("#Route" + a + "Station" + b).append($("<span>", {
                                        "class": "label label-warning"
                                    }).html("出站换乘"));
                                }
                                if ((g[1] == f[1].System && g[2] == f[2].System) || (g[1] == f[2].System && g[2] == f[1].System)) {
                                    $("#Route" + a + "Station" + b).html(StationName + " ");
                                    $("#Route" + a + "Station" + b).append($("<span>", {
                                        "class": "label label-danger"
                                    }).html("转乘"));
                                }
                            }
                        }
                    }
                }
            }
        }
    );
}

function init() {
    $.post("?Mode=allStations",
        function(c) {
            Stations = c.Stations;
            lineColors = c.Lines;
            VirtualTransfers = c.VirtualTransfers;
            Transfers = c.Transfers;
            console.log(VirtualTransfers)
            console.log(Transfers)
            Stations.forEach(function(a) {
                var c = $("<div>").html($("<span>", {
                    "class": "StationName"
                }).html(a.Name));
                a.Lines.forEach(function(a) {
                    c.append(" ");
                    c.append($("<span>", {
                        "class": "LineName",
                        style: "background-color:" + lineColors[a].Color
                    }).html(lineColors[a].ShortName));
                });
                StationList.push(c);
            })
        });
}

function walkM() {
    if ($("#fromInput").val() != nearestStation[0]) {
        $("#walk").hide();
    } else {
        $("#walk").show();
    }
}

function showTips(c, a) {
    a = void 0 === a ? 10 : a;
    inputElement = $("#" + c + "Input");
    inputString = inputElement.val();
    walkM();
    if ("" === inputString || 0 === a) {
        tipStations = "";
    } else {
        tipStations = buildTipsList(inputString);
    }

    var b = $("#" + c + "List");
    b.html("");
    if (0 < tipStations.length) {
        for (var q = 0; q < Math.min(a, tipStations.length); ++q) {
            k = $("<li>").html($("<a>", {
                href: "#",
                style: "cursor:pointer",
                click: function() {
                    inputElement.val($(this).find(".StationName").html());
                    showTips(c, 0)
                }
            }).html(tipStations[q]));
            k.appendTo(b);
        }
    } else {
        b.html("<li><a>暂无提示</a></li>");
    }; if (inputString === "" || a === 0) {
        $("#" + c + "Button").attr("aria-expanded", "false");
        $("#" + c + "Group").attr("class", "input-group-btn");
    } else {
        $("#" + c + "Button").attr("aria-expanded", "true");
        $("#" + c + "Group").attr("class", "input-group-btn open");
    }
}

function clearInput() {
    $("#toInput").val("");
    $("#fromInput").val("");
    $("#paths").html("");
    $("#walk").hide();
}

function switchInput() {
    var From = $("#toInput").val();
    $("#toInput").val($("#fromInput").val());
    $("#fromInput").val(From);
    $("#paths").html("");
    walkM();
}