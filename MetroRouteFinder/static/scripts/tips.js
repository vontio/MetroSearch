var StationList = [],
    VirtualTransfers = [],
    Transfers = [],
    lineColors;

function buildTipsList(c) {
    var a = [];
    StationList.forEach(function(b) {
        text = b.text();
        0 <= text.indexOf(c) && a.push(b)
    });
    return a
}

function find(c) {
    From = $("#fromInput").val();
    To = $("#toInput").val();
    $.post("Route/" + From + "/" + To + "/", function(a) {
        $("#paths").html("");
        Routes = a.Routes;
        Modes = a.Modes;
        for (a = 0; a < Routes.length; a++) {
            ListElement = $("<div>", {
                "class": "panel panel-default"
            });
            f = $("<div>", {
                id: "heading" + a,
                role: "tab",
                "class": "panel-heading"
            });
            h = $("<h4>", {
                "class": "panel-title"
            });
            g = $("<a>", {
                href: "#collapse" + a,
                role: "button",
                "data-toggle": "collapse",
                "data-parent": "#path" + a,
                "aria-expanded": 0 === a ? "true" : "false",
                "aria-controls": "collapse" +
                    a
            }).html("\u8def\u7ebf " + (a + 1).toString() + "\uff1a");
            correspondence = {
                "\u7ad9\u6570\u5c11": "success",
                "\u6362\u4e58\u5c11": "primary",
                "\u4e0d\u51fa\u7ad9": "warning",
                "\u4e00\u7968\u5230\u5e95": "info"
            };
            for (var b = 0; b < Modes[a].length; b++) {
                var c = "default";
                correspondence.hasOwnProperty(Modes[a][b]) && (c = correspondence[Modes[a][b]]);
                p = $("<span>", {
                    "class": "routetype label label-" + c
                }).html(Modes[a][b]);
                p.appendTo(g)
            }
            ListElement.append(f.html(h.html(g)));
            d = $("<div>", {
                id: "collapse" + a,
                "class": "panel-collapse collapse in",
                role: "tabpanel",
                "aria-labelledby": "heading" + a
            });
            e = $("<ul>", {
                "class": "list-group"
            });
            Route = Routes[a];
            for (b = 0; b < Route.Stations.length + Route.Lines.length; b++) {
                if (0 == b % 2) f = Route.Stations[b / 2], f = $("<li>", {
                    "class": "StationName list-group-item",
                    id: "Route" + a + "Station" + b
                }).html(f);
                else
                    for (h = Route.Lines[(b - 1) / 2], f = $("<li>", {
                        "class": "list-group-item"
                    }), c = 0; c < h.length; c++) 0 < c && f.append("\uff0c\u6216\uff1a<br />"), g = h[c], f.append($("<span>", {
                            "class": "LineName",
                            id: "Route" + a + "Line" + b,
                            style: "background-color:" + lineColors[g.Line].Color
                        }).html(g.Line)),
                        f.append("\u5f80"), f.append($("<span>", {
                            "class": "Direction",
                            id: "Route" + a + "Direction" + b
                        }).html(g.Direction)), f.append("\u65b9\u5411\uff0c \u5750 "), f.append($("<span>", {
                            "class": "Distance",
                            id: "Route" + a + "Distance" + b
                        }).html(g.Distance)), f.append(" \u7ad9");
                e.append(f)
            }
            ListElement.append(d.append(e));
            b = $("<div>", {
                "class": "panel-group col-xs-12 col-sm-6 col-md-4",
                id: "path" + a,
                role: "tablist",
                "aria-multiselectable": "true"
            }).html(ListElement);
            $("#paths").append(b);
            for (b = 2; b < Route.Stations.length + Route.Lines.length -
                2; b += 2) {
                StationName = Route.Stations[b / 2];
                PreviousLine = Route.Lines[(b - 2) / 2];
                NextLine = Route.Lines[b / 2];
                for (var l in PreviousLine)
                    for (var m in NextLine) {
                        var f = [StationName, PreviousLine[l].Line, NextLine[m].Line],
                            h = [StationName, NextLine[m].Line, PreviousLine[l].Line],
                            n;
                        for (n in VirtualTransfers) {
                            var g = VirtualTransfers[n];
                            if (g.toString() == f.toString() || g.toString() == h.toString()) $("#Route" + a + "Station" + b).html(StationName + " "), $("#Route" + a + "Station" + b).append($("<span>", {
                                "class": "label label-warning"
                            }).html("\u51fa\u7ad9\u6362\u4e58"))
                        }
                    }
                for (l in PreviousLine) {
                    for (m in NextLine) {
                        for (n in f =
                            [StationName, PreviousLine[l].System, NextLine[m].System], h = [StationName, NextLine[m].System, PreviousLine[l].System], Transfers) {
                            if (g = Transfers[n], g.toString() == f.toString() || g.toString() == h.toString()) {
                                $("#Route" + a + "Station" + b).html(StationName + " "), $("#Route" + a + "Station" + b).append($("<span>", {
                                    "class": "label label-danger"
                                }).html("\u8f6c\u4e58"));
                            }
                        }
                    }
                }
            }
        }
    })
}

function init() {
    $.post("?Mode=allStations", function(c) {
        Stations = c.Stations;
        lineColors = c.Lines;
        Stations.forEach(function(a) {
            var c = $("<div>").html($("<span>", {
                "class": "StationName"
            }).html(a.Name));
            a.Lines.forEach(function(a) {
                c.append($("<span>").html(" "));
                c.append($("<span>", {
                    "class": "LineName",
                    style: "background-color:" + lineColors[a].Color
                }).html(lineColors[a].ShortName))
            });
            StationList.push(c)
        })
    });
    $.post("?Mode=VirtualTransfers", function(c) {
        VirtualTransfers = c.VirtualTransfers;
        Transfers = c.Transfers;
    });
}

function showTips(c, a) {
    a = void 0 === a ? 10 : a;
    inputElement = $("#" + c + "Input");
    inputString = inputElement.val();
    tipStations = "" === inputString || 0 === a ? [] : buildTipsList(inputString);
    var b = $("#" + c + "List");
    b.html("");
    if (0 < tipStations.length)
        for (var q = 0; q < Math.min(a, tipStations.length); ++q) k = $("<li>").html($("<a>", {
            href: "#",
            style: "cursor:pointer",
            click: function() {
                inputElement.val($(this).find(".StationName").html());
                showTips(c, 0)
            }
        }).html(tipStations[q])), k.appendTo(b);
    else b.html("<li><a>\u6682\u65e0\u63d0\u793a</a></li>");
    "" === inputString || 0 === a ? ($("#" + c + "Button").attr("aria-expanded", "false"), $("#" + c + "Group").attr("class", "input-group-btn")) : ($("#" + c + "Button").attr("aria-expanded", "true"), $("#" + c + "Group").attr("class", "input-group-btn open"))
};