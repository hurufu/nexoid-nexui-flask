function xf_getInstance(modelId, instanceId) {
    var model = window.document.getElementById(modelId);
    var doc = model.getInstanceDocument(instanceId);
    return doc;
}

function xf_getNode(context, path) {
    return XsltForms_browser.selectSingleNode(path, context);
}

function xf_changeNode(node, value) {
    XsltForms_globals.openAction("XsltForms_change");
    XsltForms_browser.setValue(node, value || "");
    document.getElementById(XsltForms_browser.getMeta(node.ownerDocument.documentElement, "model")).xfElement.addChange(node);
    XsltForms_browser.debugConsole.write("Setvalue " + node.nodeName + " = " + value);
    XsltForms_globals.closeAction("XsltForms_change");
}

function xf_fireEvent(targetId, eventName, payload) {
    XsltForms_globals.openAction("XsltForms_dispatch");
    XsltForms_xmlevents.dispatch(document.getElementById(targetId), eventName, null, null, null, null, payload);
    XsltForms_globals.closeAction("XsltForms_dispatch");
}
