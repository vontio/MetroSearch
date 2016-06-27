var StationList = []; // 储存所有站点（已经去除换乘站）
function buildTipsList(inputString) {
    var tipStations = []; // 所有符合搜索条件的站点
    StationList.forEach(
        function(Station) {
            if (Station.indexOf(inputString) >= 0) {
                tipStations.push(Station); // 如果车站名里面有该汉字，加入提示列表
            }
        }
    );
    return tipStations;
}

function init(City) {
    $.post('?Mode=allStations&City=' + City,
        function(data) {
            Stations = data.Stations;
            $.post('?Mode=lineColors&City=' + City,
                function(data) {
                    lineColors = data;
                    Stations.forEach(
                        function(Station) {
                            var string = '<span class="StationName">' + Station["Name"] + '</span>'
                            Station.Lines.forEach(
                                function(Line) {
                                    string += ' <span class="LineName" style="background-color:' + lineColors[Line] + '"><font color="white">' + Line + '</font></span>';
                                }
                            );
                            StationList.push(string);
                        }
                    );
                }
            );
        }
    );
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
        var tipEntries = document.createDocumentFragment();
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