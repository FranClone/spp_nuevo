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

function openPopup(orden_pedido, cliente, nombre, fecha_produccion,fecha_entrega, productos, cantidad, prioridad, linea_produccion, comentario) {
    document.getElementById('popupCodigo').innerText = orden_pedido;
    document.getElementById('popupCliente').innerText = cliente;
    document.getElementById('popupNombre').innerText = nombre;
    document.getElementById('popupFecha').innerText = fecha_entrega;
    document.getElementById('popupFechainicio').innerText = fecha_produccion;
    document.getElementById('popupProducto').innerText = productos;
    document.getElementById('popupCantidad').innerText = cantidad;
    document.getElementById('popupPrioridad').innerText = prioridad;
    document.getElementById('popupLinea').innerText = linea_produccion;
    document.getElementById('popupComentario').innerText = comentario;
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

//Validacion Fechas

$(document).ready(function () {
    // Add an event listener to both fecha_produccion and fecha_entrega fields
    $("#id_fecha_produccion, #id_fecha_entrega").on("change", function () {
        var selectedDate = new Date($(this).val());
        var today = new Date();
        var errorSpan = $(this).siblings(".error-message"); // Find the error message element

        if (selectedDate < today) {
            errorSpan.text("Date cannot be in the past.");
            $(this).val(""); // Clear the date field
        } else {
            errorSpan.text(""); // Clear the validation message
        }
    });

    // Add an event listener to the form submission
    $("form").on("submit", function () {
        var selectedDateProduc = new Date($("#id_fecha_produccion").val());
        var selectedDateEntrega = new Date($("#id_fecha_entrega").val());
        var today = new Date();
        var errorSpanProduc = $("#id_fecha_produccion").siblings(".error-message");
        var errorSpanEntrega = $("#id_fecha_entrega").siblings(".error-message");

        // Validate fecha_produccion
        if (selectedDateProduc < today) {
            errorSpanProduc.text("Date cannot be in the past.");
            return false; // Prevent the form from submitting
        } else {
            errorSpanProduc.text(""); // Clear the validation message
        }

        // Validate fecha_entrega
        if (selectedDateEntrega < today) {
            errorSpanEntrega.text("Date cannot be in the past.");
            return false; // Prevent the form from submitting
        } else {
            errorSpanEntrega.text(""); // Clear the validation message
        }
    });
});
