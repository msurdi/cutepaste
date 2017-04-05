let $document = $(document);
$document.on("selection-change", selectionChange);
Turbolinks.start();

function selectionChange() {
    let filesCheckboxes = $("#filelist").find("input[type='checkbox']");
    let selectedCheckboxes = filesCheckboxes.filter(":checked");
    let $selectionStatus = $("#selection-status");

    if (filesCheckboxes.length === selectedCheckboxes.length) {
        $selectionStatus.val("all");
    } else if (selectedCheckboxes.length === 0) {
        $selectionStatus.val("none");
    } else {
        $selectionStatus.val("some");
    }
}

$.ajaxSetup({
    beforeSend: function (xhr) {
        let csrftoken = $("#csrftoken").val();
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
});
