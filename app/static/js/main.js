function deleteContact(cid) {
    if (window.confirm("<strong>Portfolio deletion</strong>You can't undo this action. Are you sure?")) {
        window.location.href = "/delete/" + cid;
    }
}