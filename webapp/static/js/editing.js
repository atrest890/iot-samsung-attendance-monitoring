(function() {

    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });

    var colorPicker = function(idx) {
        switch (idx) {
            case '1':
                return '#1DFE3F'
            case '2':
                return '#FE6264'
            case '3':
                return '#F5FE62'
            default:
                return 'gray'
        }
    }

    var selects = $('.color-attendance > select')

    for (let i = 0; i < selects.length; i++) {
        selects[i].parentNode.style.backgroundColor = colorPicker(selects[i].value);
        selects[i].style.backgroundColor = colorPicker(selects[i].value);

        selects[i].addEventListener('change', function(e) {
            const color = colorPicker(e.target.value)

            e.target.parentNode.style.backgroundColor = color;
            e.target.style.backgroundColor = color;
        });

        selects[i].addEventListener('change', function(e) {
            processEditing([e.target]);
        });
    }
}())

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// totalStatus отвечает за общий статус для каждого селекта переопределяя его
function processEditing(selects, totalStatus) {
    var editing = [];

    for (let i = 0; i < selects.length; i++) {
        const el = $(selects[i]);
        
        status = totalStatus || el.val()

        editing.push({
            'student': parseInt(el.attr('name')),
            'attendance' : parseInt(el.attr('id')),
            'status' : status
        });
    }

    $.ajax({
        type: 'POST',
        data: {
            data: JSON.stringify(editing),
            csrfmiddlewaretoken: getCookie('csrftoken')
        },
        success: function(data, status) {

            alertTriggeret(data, 'success');
            // TODO: фактически костыль, ибо можно изменять селект
            location.reload();
        },
        error : function(jqXHR, status) {

            alertTriggeret('Произошла ошибка[' + jqXHR.status + ']: ' + jqXHR.statusText, 'danger');
            
            console.log('input error status:', status);
        }
    })
}

function groupEdit(idx) {
    processEditing($('.group-edit:checked'), idx);
}

function selectAll() {
    $('.group-edit').each(function(a, tag){ 
        tag.checked = true;
    });
}

function deselectAll(params) {
    $('.group-edit').each(function(a, tag){ 
        tag.checked = false;
    });
}