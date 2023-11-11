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

function openPopup(
    
    fecha_produccion, nombre,comentario,version,prioridad
  ) {
   // document.getElementById('popupCodigo').innerText = orden_interna;
    document.getElementById('popupfechap').innerText = fecha_produccion;
    document.getElementById('popupProducto').innerText = nombre;
    document.getElementById('popupComentario').innerText = comentario;
    document.getElementById('popupVersion').innerText = version;
    document.getElementById('popupPrioridad').innerText = prioridad || "N/A";
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

//Validacion Fechas

$(document).ready(function () {
    // Calculate yesterday's date
    var yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);

    // Format yesterday's date in yyyy-mm-dd format
    var formattedYesterday = yesterday.toISOString().split('T')[0];

    // Set the min attribute for fecha_produccion and fecha_entrega to yesterday's date
    $("#id_fecha_produccion, #id_fecha_entrega").attr("min", formattedYesterday);

    // Add an event listener to both fecha_produccion and fecha_entrega fields
    $("#id_fecha_produccion, #id_fecha_entrega").on("change", function () {
        var fechaProduc = new Date($("#id_fecha_produccion").val());
        var fechaEntrega = new Date($("#id_fecha_entrega").val());
        var errorSpanProduc = $("#id_fecha_produccion").siblings(".error-message");
        var errorSpanEntrega = $("#id_fecha_entrega").siblings(".error-message");

        // Validate fecha_produccion
        if (fechaProduc < yesterday) {
            errorSpanProduc.text("Date cannot be earlier than yesterday.");
            $("#id_fecha_produccion").val(""); // Clear the date field
        } else {
            errorSpanProduc.text(""); // Clear the validation message
        }

        // Validate fecha_entrega
        if (fechaEntrega < yesterday) {
            errorSpanEntrega.text("Date cannot be earlier than yesterday.");
            $("#id_fecha_entrega").val(""); // Clear the date field
        } else if (fechaProduc > fechaEntrega) {
            errorSpanProduc.text("Fecha produccion cannot be later than Fecha entrega.");
            errorSpanEntrega.text("Fecha entrega cannot be earlier than Fecha produccion.");
            $("#id_fecha_produccion").val(""); // Clear the date field
            $("#id_fecha_entrega").val(""); // Clear the date field
        } else {
            errorSpanProduc.text(""); // Clear the validation message
            errorSpanEntrega.text(""); // Clear the validation message
        }
    });

    // Add an event listener to the form submission
    $("form").on("submit", function () {
        var fechaProduc = new Date($("#id_fecha_produccion").val());
        var fechaEntrega = new Date($("#id_fecha_entrega").val());
        var errorSpanProduc = $("#id_fecha_produccion").siblings(".error-message");
        var errorSpanEntrega = $("#id_fecha_entrega").siblings(".error-message");

        // Validate fecha_produccion
        if (fechaProduc < yesterday) {
            errorSpanProduc.text("Date cannot be earlier than yesterday.");
            return false; // Prevent the form from submitting
        } else {
            errorSpanProduc.text(""); // Clear the validation message
        }

        // Validate fecha_entrega
        if (fechaEntrega < yesterday) {
            errorSpanEntrega.text("Date cannot be earlier than yesterday.");
            return false; // Prevent the form from submitting
        } else if (fechaProduc > fechaEntrega) {
            errorSpanProduc.text("Fecha produccion cannot be later than Fecha entrega.");
            errorSpanEntrega.text("Fecha entrega cannot be earlier than Fecha produccion.");
            return false; // Prevent the form from submitting
        } else {
            errorSpanProduc.text(""); // Clear the validation message
            errorSpanEntrega.text(""); // Clear the validation message
        }
    });
});
