var toggleFilterButton = document.getElementById('toggle-filter-button');
var filterForm = document.getElementById('filter-form');
var cancelFilterButton = document.getElementById('cancel-filter-button');
var isFilterVisible = false; // Variable de estado para el filtro

toggleFilterButton.addEventListener('click', function() {
    if (isFilterVisible) {
        filterForm.style.display = 'none';
        toggleFilterButton.innerText = 'Filtrar';
        isFilterVisible = false;
    } else {
        filterForm.style.display = 'block';
        toggleFilterButton.innerText = 'Ocultar filtro';
        isFilterVisible = true;
    }
});

filterForm.addEventListener('submit', function(event) {
    event.preventDefault();
    filtrar();
});

cancelFilterButton.addEventListener('click', function() {
    filterForm.style.display = 'none';
    filterForm.reset();
    toggleFilterButton.innerText = 'Filtrar';
    isFilterVisible = false;
});

function filtrar() {
    const numeroBuzon = document.getElementById('filter-buzon').value;
    const tipoMadera = document.getElementById('filter-madera').value;
    const claseDiametrica = document.getElementById('filter-diametrica').value;
    const longitud = document.getElementById('filter-longitud').value;
    const cantidad = document.getElementById('filter-cantidad').value;

    const table = document.getElementById('materia-prima-table');
    const rows = table.getElementsByTagName('tr');

    for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const numeroBuzonColumn = row.cells[0].innerText;
        const tipoMaderaColumn = row.cells[1].innerText;
        const claseDiametricaColumn = row.cells[2].innerText;
        const longitudColumn = row.cells[3].innerText;
        const cantidadColumn = row.cells[4].innerText;

        if (
            (numeroBuzon !== '' && numeroBuzonColumn !== numeroBuzon) ||
            (tipoMadera !== '' && tipoMaderaColumn !== tipoMadera) ||
            (claseDiametrica !== '' && claseDiametricaColumn !== claseDiametrica) ||
            (longitud !== '' && longitudColumn !== longitud) ||
            (cantidad !== '' && cantidadColumn !== cantidad)
        ) {
            row.style.display = 'none';
        } else {
            row.style.display = '';
        }
    }
}

const toggleButton = document.getElementById("toggle-carga-button");
const cargaForm = document.querySelector(".form-container-materia-prima form");

let isFormVisible = false;

toggleButton.addEventListener("click", function() {
    if (!isFormVisible) {
        const buttonRect = toggleButton.getBoundingClientRect();
        const buttonBottom = buttonRect.bottom;
        cargaForm.style.display = "block";
        isFormVisible = true;
    } else {
        cargaForm.style.display = "none";
        isFormVisible = false;
    }
});
