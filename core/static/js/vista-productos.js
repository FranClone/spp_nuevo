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



function openPopup(orden_producto, nombre, descripcion, inventario_inicial, nombre_rollizo, inventario_final,linea,patrones_de_corte) {
    // Set the data in the popup
    console.log( patrones_de_corte);
    document.getElementById('popupOrden_producto').innerText = orden_producto;
    document.getElementById('popupNombre').innerText = nombre;
    document.getElementById('popupDescripcion').innerText = descripcion;
    document.getElementById('popupInventario_inicial').innerText = inventario_inicial;
    document.getElementById('popupNombre_rollizo').innerText = nombre_rollizo;
    document.getElementById('popupInventario_final').innerText = inventario_final;
    document.getElementById('popupLinea').innerText = linea;
    document.getElementById('popupPatron_corte').innerText = patrones_de_corte;
    console.log("IDs de patrones de corte relacionados:", patrones_de_corte);
    document.getElementById('popupOverlay').style.display = 'flex';
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


//Validador de fechas
$(document).ready(function () {
    function validateDateField($field) {
        var selectedDate = new Date($field.val());
        var today = new Date();

        if (selectedDate < today) {
            alert("Date cannot be in the past.");
            $field.val("");
        }
    }

    // Add an event listener to the fecha_produccion field
    $("#id_fecha_produccion").on("change", function () {
        validateDateField($(this));
    });
});








  
