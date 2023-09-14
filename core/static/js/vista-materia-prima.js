$(document).ready(function() {
    var $filterButton = $(".filter-button");
    var $showFilterForm = $(".filter-form");
    var $advancedSearch = $("#advanced-search");
    var $advancedSearchOptions = $("#advanced-search-options");
    var $filterForm = $(".filter-form");
    var $filterInputs = $(".filter-input");
    var $clearFilterButton = $(".clear-filter-button");
    var $tableRows = $(".table tbody tr");
    var $noDataMessage = $(".no-data-message");
    var $filterSelects = $(".filter-select");

    $filterButton.click(function() {
        $showFilterForm.toggle();
    });

    $advancedSearch.change(function() {
        $advancedSearchOptions.toggle(this.checked);
    });

    $filterForm.submit(function(e) {
        e.preventDefault();
        filterTable();
    });

    $filterInputs.keyup(function() {
        filterTable();
    });

    $clearFilterButton.click(function() {
        $filterForm[0].reset();
        $tableRows.show();
        $noDataMessage.hide();
    });

    function filterTable() {
        $tableRows.hide();

        var filterBy = $filterSelects.filter("[name='filter-by']").val();
        var filterValue = $filterInputs.filter("[name='filter-value']").val().toLowerCase();
        var filterOption = $filterSelects.filter("[name='filter-option']").val();
        var filterLength = parseFloat($("#filter-length").val());
        var filterLengthMax = parseFloat($("#filter-length-max").val());
        var filterWidth = parseFloat($("#filter-width").val());
        var filterWidthMax = parseFloat($("#filter-width-max").val());
        var filterThickness = parseFloat($("#filter-thickness").val());
        var filterThicknessMax = parseFloat($("#filter-thickness-max").val());
        var advancedSearch = $advancedSearch.is(":checked");

        $tableRows.each(function() {
            var $row = $(this);
            var rowData = $row.find("td:nth-child(" + (getFieldIndex(filterBy) + 1) + ")").text().toLowerCase();
            var rowLength = parseFloat($row.find("td:nth-child(5)").text());
            var rowWidth = parseFloat($row.find("td:nth-child(4)").text());
            var rowThickness = parseFloat($row.find("td:nth-child(3)").text());

            if (advancedSearch) {
                if (filterLength && (rowLength < filterLength || rowLength > filterLengthMax)) {
                    return;
                }
                if (filterWidth && (rowWidth < filterWidth || rowWidth > filterWidthMax)) {
                    return;
                }
                if (filterThickness && (rowThickness < filterThickness || rowThickness > filterThicknessMax)) {
                    return;
                }
            }

            if (filterOption === "partial" && rowData.includes(filterValue)) {
                $row.show();
            } else if (filterOption === "exact" && rowData === filterValue) {
                $row.show();
            }
        });

        $noDataMessage.toggle($tableRows.filter(":visible").length === 0);
    }

    function getFieldIndex(fieldName) {
        var index = 0;

        switch (fieldName) {
            case "nombre":
                index = 1;
                break;
            case "codigo":
                index = 0;
                break;
        }

        return index;
    }
});

function openPopup(numero_buzon, nombre, alto, ancho, largo, conicidad, almacenamiento, inventario_inicial, volumen_procesado, inventario_final) {
    document.getElementById('popupCodigo').textContent = numero_buzon;
    document.getElementById('popupNombre').textContent = nombre;
    document.getElementById('popupAlto').textContent = alto;
    document.getElementById('popupAncho').textContent = ancho;
    document.getElementById('popupLargo').textContent = largo;
   // document.getElementById('popupLinea').textContent = linea;
    document.getElementById('popupConicidad').textContent = conicidad;
    document.getElementById('popupAlmacenamiento').textContent = almacenamiento;
    document.getElementById('popupInventario_inicial').textContent = inventario_inicial;
    document.getElementById('popupVolumen_procesado').textContent = volumen_procesado;
    document.getElementById('popupInventario_final').textContent = inventario_final;
    document.getElementById('popupOverlay').style.display = 'block';
    document.getElementById('popup').style.display = 'block';
}

function closePopup() {
    document.getElementById('popupOverlay').style.display = 'none';
    document.getElementById('popup').style.display = 'none';
}
$(document).ready(function() {
    $('.table').DataTable({
        paging: true,

    });
});
toggleFilter();

function toggleFilter() {
var toggleFilterButton = document.querySelector('.filter-section .filter-button');
var filterForm = document.querySelector('.filter-section .filter-form');
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
}

toggleCargaForm();

function toggleCargaForm() {
    
    const toggleButton = document.getElementById("toggle-carga-button");
    const cargaForm = document.querySelector(".form-container-productos form");

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
}



