//Este jQuery lo que hace es darte la lista de empresas obtenida desde una solicitud GET
$(document).ready(function() {
// Obtener la referencia al campo de RUT y la lista de empresas
    const rutField = $('.rut-body-empresa');
    const empresasSelect = $('#empresas-list');

    // Función que se ejecuta cuando cambia el valor del campo de RUT
    rutField.on('input', function() {
        const parteRut = $(this).val();
        // Enviar una solicitud AJAX a la vista "get_empresas"
        $.get('/get_empresas/', { parte_rut: parteRut }, function(data) {
        // Actualizar el contenido de la lista de empresas con los nuevos datos
            empresasSelect.empty();
            for (let empresa of data.empresas) {
                empresasSelect.append($('<option></option>').val(empresa).text(empresa));
            }
        });
    });
});