function getURLParam(key) {
    var reg = new RegExp("(^|&)" + key + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
    var r = window.location.search.substr(1).match(reg); //匹配目标参数
    if (r != null) {
        return decodeURI(r[2]);
    } else {
        return "Guangzhou";
    } //返回参数值
}