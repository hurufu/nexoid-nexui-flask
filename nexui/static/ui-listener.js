if (!!window.EventSource) {
    var source = new EventSource('/pay/display-updates');

    var dp = new DOMParser();
    var xp = new XSLTProcessor();

    var xmlReq = new XMLHttpRequest();
    xmlReq.open("GET", "scap-request.xsl", false);
    xmlReq.send(null);
    xp.importStylesheet(xmlReq.responseXML);

    source.onmessage = function(e) {
        const newElement = document.createElement("li");
        const eventList = document.getElementById("list");

        var xmlDoc = dp.parseFromString(e.data, "text/xml");
        var xml = xmlDoc.getElementsByTagName("ScapiRequest")[0]

        const now = new Date(Date.now());
        xp.setParameter("", "current-time", now.toLocaleString());

        var fragment = xp.transformToFragment(xml, document);

        eventList.prepend(fragment);
    }
}
