//Este Código jQuery lo que hace es bloquear las teclas que no sean números, o k o K en el dígito verificador
$(document).ready(function() {
    // Detecta cuando se realiza un input en los campos con clase "rut-body" y "rut-dv"
    $(".input-rut-body, .input-rut-dv").on("input", function(event) {
        // Obtiene el valor del campo y remueve cualquier caracter que no sea un número o la letra 'k' o 'K'    
        if ($(this).hasClass('input-rut-body')) {
            var value = $(this).val().replace(/[^0-9]/g, '');
            // Si el campo es el "rut-body", limita el valor a 8 caracteres
            value = value.substring(0, 8);
        } else {
            var value = $(this).val().replace(/[^0-9kK]/g, '');
            // Si el campo es el "rut-dv", limita el valor a 1 caracter
            value = value.substring(0, 1);
        }
    
        // Actualiza el valor del campo
        $(this).val(value);
    });
    
    // Detecta cuando se pega texto en los campos con clase "rut-body" y "rut-dv"
    $(".input-rut-body, .input-rut-dv").on("paste", function(event) {
        // Obtiene el texto que se está pegando
        var pasteData = event.originalEvent.clipboardData.getData('text');
        
        // Remueve cualquier caracter que no sea un número o la letra 'k' o 'K'

    
        if ($(this).hasClass('input-rut-body')) {
            var value = pasteData.replace(/[^0-9]/g, '');
            // Si el campo es el "rut-body", limita el valor a 8 caracteres
            value = value.substring(0, 8);
        } else {
            var value = pasteData.replace(/[^0-9kK]/g, '');
            // Si el campo es el "rut-dv", limita el valor a 1 caracter
            value = value.substring(0, 1);
        }
    
        // Actualiza el valor del campo
        $(this).val(value);
        // Previene la acción predeterminada de pegar texto
        event.preventDefault();
    });

    // Cuando el RUT Body termina, pasa inmediatamente al RUT dv
    $('.input-rut-body').keyup(function(e) {
        if ($(this).val().length == $(this).attr('maxlength')) {
            $('.input-rut-dv').focus();
        }
    });

    $(".input-rut-dv").keyup(function(e) {
        if( $(this).val().length == $(this).attr("maxlength")) {
            $("#id_password").focus();
        }
    });

    $(".input-rut-dv").keyup(function(e) {
        if( $(this).val().length == ("")){
            $('.input-rut-body').focus();
        }
    });

});