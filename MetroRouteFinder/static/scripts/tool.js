function getURLParam(key) {
    var reg=new RegExp("(^|&)"+key+"=([^&]*)(&|$)");
    var r=window.location.search.substr(1).match(reg);
    if (r!=null)
    {
        return decodeURI(r[2]);
    } else {
        return "Guangzhou";
    }
}