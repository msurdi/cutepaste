let csrftoken = getCookie('csrftoken');

$(document).ajaxStart(saveCaretPosition);
$(document).ajaxComplete(restoreCaretPosition);
$(document).on("cp:displayIfMatches", displayIfMatches);
$(document).on("cp:selectAll", selectAll);
$(document).on("cp:selectNone", selectNone);
$(document).on("beforeAjaxSend.ic", setupCsrfHeader);


function setupCsrfHeader(event, ajaxSetup) {
    if (!csrfSafeMethod(ajaxSetup.type) && !this.crossDomain) {
        ajaxSetup.headers["X-CSRFToken"] = csrftoken;
    }
}

function displayIfMatches(event, matchSelector, showSelector, hideSelector) {
    let matchElements = $(matchSelector);
    let showElements = $(showSelector);
    let hideElements = $(hideSelector);
    let matches = matchElements.length > 0;
    if (matches) {
        showElements.show();
        hideElements.hide();
    } else {
        showElements.hide();
        hideElements.show();
    }
}


function selectAll(event, checkboxesSelector) {
    $(checkboxesSelector).prop("checked", true);
}


function selectNone(event, checkboxesSelector) {
    $(checkboxesSelector).prop("checked", false);
}

let focused = null;
let focused_position = -1;

function saveCaretPosition() {
    focused = null;
    let activeElement = document.activeElement;
    if (activeElement && activeElement.id) {
        focused = activeElement.id;
        focused_position = -1;
        if (activeElement.hasAttribute("value") && activeElement.selectionStart != undefined) {
            focused_position = activeElement.value.slice(0, activeElement.selectionStart).length;
        }
    }
}
function restoreCaretPosition() {
    if (!focused) {
        return;
    }
    setTimeout(() => {
        let element = document.getElementById(focused);
        if (element) {
            element.focus();
        }
        if (focused_position > -1 && element.selectionStart != undefined) {
            element.selectionStart = element.selectionEnd = focused_position;
        }
    });

}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
