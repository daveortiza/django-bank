$(document).ready(function(){

    $.ajaxSetup({
        headers: {
            'XCSRFToken': $( 'meta[name="csrf-token"]').attr('content')
        }
    });

    $( "#cardModal" ).on( "click", "#requestBtn", function () {
        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: '/banking/create/'
        })
        .done(function(data) {
            var html = 'Card number <b>' + data.card + '</b><br>'
                     + 'Pincode <b>' + data.pincode + '</b>';

            $('#cardModal #requestBtn').hide();
            $("#cardModal #loaded").val(1);
            $("#cardModal .modal-body").html(html);
        })
        .fail(function(data) {
            console.log(data._message)
        })
    });

    $( "#cardModal" ).on( "click", ".close-modal", function () {
        is_loaded = parseInt($("#cardModal #loaded").val());
        if (is_loaded) {
            location.reload();
        }
    });

    $( "#cardModal" ).on( "submit", "#createTransaction", function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data._status == '201') {
                    $("#cardModal").modal("hide");
                } else {
                    $("#cardModal .modal-content").html(data.modal);
                }
            }
        });

        return false;
    });

    /**
     * Call modal window
     */
    $( "#callCardModal" ).click(function () {
        $.ajax({
            url: '/banking/card-modal/',
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#cardModal").modal("show");
            },
            success: function (data) {
                $("#cardModal .modal-content").html(data.modal);
            }
        });
    });

    /**
     * Call modal window
     */
    $( "#callTransactionModal" ).click(function () {
        $.ajax({
            url: '/banking/transaction-form/',
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#cardModal").modal("show");
            },
            success: function (data) {
                $("#cardModal .modal-content").html(data.modal);
            }
        });
    });

});