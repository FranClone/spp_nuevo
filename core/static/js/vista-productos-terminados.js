$(document).ready(function() {
    $("#patrones-table").DataTable({
        paging: true,
    });
});

function openPopup(id, nombreBodega, nombreEmpresa, descripcion) {

}

function closePopup() {

}


document.querySelector('.filter-form').addEventListener('submit', function(event) {
    event.preventDefault();
    filtrar();
});


function filtrar() {

    const codigo = document.querySelector('input[name="filter-codigo"]').value;
    const nombre = document.querySelector('input[name="filter-nombre"]').value;
    const claseDiametrica = document.querySelector('select[name="filter-clase"]').value;
    const patronCorte = document.querySelector('input[name="filter-patron"]').value;
    const cantidad = document.querySelector('input[name="filter-amount"]').value;

    // Obtener todas las filas de la tabla
    const table = document.getElementById('patrones-table');
    const rows = table.getElementsByTagName('tr');

    // Recorrer las filas y mostrar/ocultar según los filtros
    for (let i = 1; i < rows.length; i++) { // Comenzamos desde 1 para omitir la fila de encabezado
        const row = rows[i];
        const codigoColumn = row.cells[0].innerText;
        const nombreColumn = row.cells[1].innerText;
        const claseDiametricaColumn = row.cells[5].innerText;
        const patronCorteColumn = row.cells[6].innerText;
        const cantidadColumn = row.cells[7].innerText;

        // Verificar si alguna columna no coincide con los filtros
        if (
            (codigo !== '' && codigoColumn !== codigo) ||
            (nombre !== '' && nombreColumn !== nombre) ||
            (claseDiametrica !== '' && claseDiametricaColumn !== claseDiametrica) ||
            (patronCorte !== '' && patronCorteColumn !== patronCorte) ||
            (cantidad !== '' && cantidadColumn !== cantidad)
        ) {
            // Ocultar la fila
            row.style.display = 'none';
        } else {
            // Mostrar la fila
            row.style.display = '';
        }
    }
}

// Evento que se activa al enviar el formulario de filtro
document.querySelector('.filter-form').addEventListener('submit', function(e) {
    e.preventDefault(); // Evitar que se recargue la página al enviar el formulario
    filtrar(); // Ejecutar la función de filtrado
});
// Función para limpiar los campos de filtro
// Agregar el evento de click al botón de cancelar
document.querySelector('.clear-filter-button').addEventListener('click', function(event) {
    event.preventDefault();
    limpiarFiltros();
});

// Función para limpiar los campos de filtro
function limpiarFiltros() {
    // Limpiar los valores de los campos de filtro
    document.querySelector('input[name="filter-codigo"]').value = '';
    document.querySelector('input[name="filter-nombre"]').value = '';
    document.querySelector('select[name="filter-clase"]').value = '';
    document.querySelector('input[name="filter-patron"]').value = '';
    document.querySelector('input[name="filter-amount"]').value = '';

    // Mostrar todas las filas de la tabla
    const table = document.getElementById('patrones-table');
    const rows = table.getElementsByTagName('tr');
    for (let i = 1; i < rows.length; i++) {
        rows[i].style.display = '';
    }
}

// Mostrar u ocultar opciones de búsqueda avanzada
document.getElementById('advanced-search').addEventListener('change', function() {
    const advancedSearchOptions = document.getElementById('advanced-search-options');
    advancedSearchOptions.style.display = this.checked ? 'block' : 'none';
});