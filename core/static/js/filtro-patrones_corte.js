const filterForm = document.getElementById('filter-form');
const toggleFilterButton = document.getElementById('toggle-filter-button');
const advancedFilterCheckbox = document.getElementById('advanced-filter-checkbox');
const advancedFilter = document.getElementById('advanced-filter');
const filterButton = document.getElementById('filter-button');
const cancelFilterButton = document.getElementById('cancel-filter-button');
const filterBuzonInput = document.getElementById('filter-buzon');
const filterMaderaInput = document.getElementById('filter-madera');
const filterDiametricaInput = document.getElementById('filter-diametrica');
const filterLongitudInput = document.getElementById('filter-longitud');
const filterCantidadInput = document.getElementById('filter-cantidad');
const table = $('#materia-prima-table').DataTable({


});

toggleFilterButton.addEventListener('click', () => {
    filterForm.style.display = filterForm.style.display === 'none' ? 'block' : 'none';
    advancedFilter.style.display = 'none';
    clearAdvancedFilterInputs();
});

advancedFilterCheckbox.addEventListener('change', () => {
    advancedFilter.style.display = advancedFilterCheckbox.checked ? 'block' : 'none';
});

filterButton.addEventListener('click', () => {
    applyFilters();
});

cancelFilterButton.addEventListener('click', () => {
    filterBuzonInput.value = '';
    clearAdvancedFilterInputs();
    applyFilters();
});

function applyFilters() {
    const buzonFilter = filterBuzonInput.value.toLowerCase();
    const maderaFilter = filterMaderaInput.value.toLowerCase();
    const diametricaFilter = filterDiametricaInput.value.toLowerCase();
    const longitudFilter = filterLongitudInput.value.toLowerCase();
    const cantidadFilter = filterCantidadInput.value.toLowerCase();

    table.columns(0).search(buzonFilter).draw();
    table.columns(1).search(maderaFilter).draw();
    table.columns(2).search(diametricaFilter).draw();
    table.columns(3).search(longitudFilter).draw();
    table.columns(4).search(cantidadFilter).draw();
}

function clearAdvancedFilterInputs() {
    filterMaderaInput.value = '';
    filterDiametricaInput.value = '';
    filterLongitudInput.value = '';
    filterCantidadInput.value = '';
}

function openPopup(codigoPatron, nombrePatron, productoAsociado, claseDiametrica) {
    document.getElementById('popupCodigoPatron').textContent = codigoPatron;
    document.getElementById('popupNombrePatron').textContent = nombrePatron;
    document.getElementById('popupProductoAsociado').textContent = productoAsociado;
    document.getElementById('popupClaseDiametrica').textContent = claseDiametrica;
}

function closePopup() {
    document.getElementById('popupOverlay').style.display = 'none';
    document.getElementById('popup').style.display = 'none';
}