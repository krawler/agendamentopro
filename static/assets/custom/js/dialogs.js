
function showDialogModalDeactivate(id){
    $('.btn-delete').on('click', function(){
        $("#dialog-confirm-deactivate").dialog({
            resizable: false,
            height: "auto",
            width: 400,
            modal: true,
            buttons: {
                    "Desativar": function() {
                        $.ajax({
                            type: "POST",
                            dataType: "json",
                            url: "{% url 'pedido:desativar' %}",
                            data: {
                                "pedidoid" : id,
                                "csrfmiddlewaretoken": $('meta[name="csrf-token"]').attr('content')
                            },
                            success: function(jsonData) { 
                                if(jsonData=="True")
                                    return console.log("returned: " + jsonData);
                            }
                        });
                    window.location.reload()    
                    $( this ).dialog( "close" );
                },
                Cancel: function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    });
}
