var StationList = []; // 储存所有站点（已经去除换乘站）
var VirtualTransfers = [];
var Transfers = [];
var VirtualTransfersRemind;
var lineColors;

function buildTipsList(inputString) {
    var tipStations = []; // 所有符合搜索条件的站点
    StationList.forEach(
        function(Station) {
            text = Station.text()
            if (text.indexOf(inputString) >= 0) {
                tipStations.push(Station); // 如果车站名里面有该汉字，加入提示列表
            }
        }
    );
    return tipStations;
}

function find(Mode) {
    From = $('#fromInput').val();
    To = $('#toInput').val();
    $.post('Route/' + From + "/" + To + "/",
        function(data) {
            $("#paths").html("");
            Routes = data["Routes"];
            Modes = data["Modes"];
            for (var i = 0; i < Routes.length; i++) {
                ListElement = $("<div>", {
                    class: "panel panel-default"
                });
                a = $("<div>", {
                    "id": "heading" + i,
                    "role": "tab",
                    "class": "panel-heading"
                });
                b = $("<h4>", {
                    "class": "panel-title"
                });
                c = $("<a>", {
                    "href": "#collapse" + i,
                    "role": "button",
                    "data-toggle": "collapse",
                    "data-parent": "#path" + i,
                    "aria-expanded": (i === 0) ? "true" : "false",
                    "aria-controls": "collapse" + i
                }).html("路线 " + (i + 1).toString() + "：");
                correspondence = {
                    "站数少": "success",
                    "换乘少": "primary",
                    "不出站": "warning",
                    "一票到底": "info"
                }
                for (var mode = 0; mode < Modes[i].length; mode++) {
                    var xxxxx = 'default';
                    if (correspondence.hasOwnProperty(Modes[i][mode])) {
                        xxxxx = correspondence[Modes[i][mode]];
                    }
                    p = $("<span>", {
                        "class": "routetype label label-" + xxxxx
                    }).html(Modes[i][mode]);
                    p.appendTo(c);
                }
                ListElement.append(a.html(b.html(c)));
                d = $("<div>", {
                    "id": "collapse" + i,
                    "class": "panel-collapse collapse in",
                    "role": "tabpanel",
                    "aria-labelledby": "heading" + i
                })
                e = $("<ul>", {
                    "class": "list-group"
                })
                Route = Routes[i];
                for (var j = 0; j < Route["Stations"].length + Route["Lines"].length; j++) {
                    if (j % 2 == 0) {
                        var Station = Route["Stations"][j / 2];
                        var Element = $("<li>", {
                            class: 'StationName list-group-item',
                            id: 'Route' + i + 'Station' + j
                        }).html(Station);
                        e.append(Element);
                    } else {
                        var Line = Route["Lines"][(j - 1) / 2];
                        var Choice = Line[0];
                        Element = $("<li>", {
                            class: 'list-group-item'
                        });
                        for (var k = 0; k < Line.length; k++) {
                            if (k > 0) {
                                Element.append("，或：<br />");
                            }
                            Choice = Line[k];
                            Element.append($("<span>", {
                                class: 'LineName',
                                id: 'Route' + i + 'Line' + j,
                                style: 'background-color:' + lineColors[Choice["Line"]]["Color"]
                            }).html(Choice["Line"]));
                            Element.append("往");
                            Element.append($("<span>", {
                                class: 'Direction',
                                id: 'Route' + i + 'Direction' + j
                            }).html(Choice["Direction"]));
                            Element.append("方向， 坐 ");
                            Element.append($("<span>", {
                                class: 'Distance',
                                id: 'Route' + i + 'Distance' + j
                            }).html(Choice["Distance"]));
                            Element.append(" 站");
                        }
                        e.append(Element);
                    }
                }
                ListElement.append(d.append(e));
                var aa = $("<div>", {
                    class: "panel-group col-xs-12 col-sm-6 col-md-4",
                    id: "path" + i,
                    role: "tablist",
                    "aria-multiselectable": "true"
                }).html(ListElement);
                $("#paths").append(aa);
                for (var j = 2; j < Route["Stations"].length + Route["Lines"].length - 2; j = j + 2) {
                    StationName = Route["Stations"][j / 2];
                    PreviousLine = Route["Lines"][(j - 2) / 2];
                    NextLine = Route["Lines"][j / 2];
                    for (var routea in PreviousLine) {
                        for (var routeb in NextLine) {
                            var a = [StationName, PreviousLine[routea]["Line"], NextLine[routeb]["Line"]];
                            var b = [StationName, NextLine[routeb]["Line"], PreviousLine[routea]["Line"]];
                            for (var list in VirtualTransfers) {
                                var c = VirtualTransfers[list];
                                if (c.toString() == a.toString() || c.toString() == b.toString()) {
                                    $("#Route" + i + "Station" + j).html(StationName + " ");
                                    $("#Route" + i + "Station" + j).append($("<span>", {class:"label label-warning"}).html("出站换乘"));
                                }
                            }
                        }
                    }
                    for (var routea in PreviousLine) {
                        for (var routeb in NextLine) {
                            var a = [StationName, PreviousLine[routea]["System"], NextLine[routeb]["System"]];
                            var b = [StationName, NextLine[routeb]["System"], PreviousLine[routea]["System"]];
                            // console.log(a, b);
                            for (var list in Transfers) {
                                var c = Transfers[list];
                                if (c.toString() == a.toString() || c.toString() == b.toString()) {
                                    $("#Route" + i + "Station" + j).html(StationName + " ");
                                    $("#Route" + i + "Station" + j).append($("<span>", {class:"label label-danger"}).html("转乘"));
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
    $.post('?Mode=allStations', function(data) {
        Stations = data.Stations;
        $.post('?Mode=lineColors', function(data) {
            lineColors = data;
            Stations.forEach(
                function(Station) {
                    var string = $("<div>").html($("<span>", {
                        class: "StationName"
                    }).html(Station["Name"]))
                    Station.Lines.forEach(function(Line) {
                        string.append($("<span>").html(" "));
                        string.append($("<span>", {
                            class: "LineName",
                            style: 'background-color:' + lineColors[Line]["Color"]
                        }).html(lineColors[Line]["ShortName"]));
                    });
                    StationList.push(string);
                }
            );
        });
    });
    $.post('?Mode=VirtualTransfers', function(data) {
        VirtualTransfers = data["VirtualTransfers"];
        Transfers = data["Transfers"];
        VirtualTransfersRemind = data["VirtualTransfersRemind"];
    });
}

function showTips(Element, tipCount = 10) {
    inputElement = $('#' + Element + 'Input');
    inputString = inputElement.val();
    if (inputString === "" || tipCount === 0) {
        tipStations = []; // 如果输入的字符为空，留空
    } else {
        tipStations = buildTipsList(inputString); // 否则，存储输入的站点名称字符串
    }
    var List = $('#' + Element + 'List');
    List.html(''); // 清空用来载入提示的元素
    if (tipStations.length > 0) {
        for (var i = 0; i < Math.min(tipCount, tipStations.length); ++i) {
            k = $('<li>').html(
                $('<a>', {
                    href: "#",
                    style: "cursor:pointer",
                    click: function() {
                        inputElement.val($(this).find(".StationName").html());
                        showTips(Element, 0);
                    }
                }).html(tipStations[i])
            );
            k.appendTo(List);
        }
    } else {
        List.html('<li><a>暂无提示</a></li>');
    }

    if (inputString === "" || tipCount === 0) {
        $('#' + Element + 'Button').attr("aria-expanded", "false");
        $('#' + Element + 'Group').attr("class", "input-group-btn");
    } else {
        $('#' + Element + 'Button').attr("aria-expanded", "true");
        $('#' + Element + 'Group').attr("class", "input-group-btn open");
    }
}