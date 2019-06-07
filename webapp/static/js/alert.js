function alertTriggeret(text, type) {
    type = type || 'info'

    var htmlAlert = `<div class="alert alert-` + type + ` alert-dismissible fade show" role="alert" id="alert">
                    <strong>`+ text +`</strong>
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                        </button>
                    </div>`;

    $('#alert_placeholder').stop(true, true);
    $('#alert_placeholder').html(htmlAlert);
    $('#alert_placeholder').show();
    $('#alert_placeholder').hide(5000);
}