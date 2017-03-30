$(document).on("beforeAjaxSend.ic", setupCsrfHeader);
$.subscribe("selectionChanged", selectionChanged);
$.subscribe("selectAll", selectAll);
$.subscribe("unselectAll", unselectAll);

function setupCsrfHeader(event, ajaxSetup) {
    let csrftoken = $("#csrftoken").val();
    if (!csrfSafeMethod(ajaxSetup.type) && !this.crossDomain) {
        ajaxSetup.headers["X-CSRFToken"] = csrftoken;
    }
}

function selectionChanged() {
    Intercooler.refresh("/buttons");
}

function clipboardChanged() {};

function selectAll() {
    let checkElements = $(".data-check");
    checkElements.prop("checked", true);
    $.publish("selectionChanged")
}

function unselectAll() {
    let checkElements = $(".data-check");
    checkElements.prop("checked", false);
    $.publish("selectionChanged")
}

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
