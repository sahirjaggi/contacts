function deleteContact(cid) {
    if (window.confirm("Are you sure you want to delete this contact?")) {
        window.location.href = "/delete/" + cid;
    }
}

function contactOverlay(cid) {
    var loc = "/list_item/" + cid;
    var del = "javascript:deleteContact('" + cid + "');"
    document.getElementById('contact_frame').setAttribute('src', loc);
    document.getElementById('delete').setAttribute('href', del);
	el = document.getElementById("contact_overlay");
	el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
}

function newOverlay() {
	el = document.getElementById("new_overlay");
	el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
}

function coExpand() {
    el = document.getElementById("content-one");
    el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
}