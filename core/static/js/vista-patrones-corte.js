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

        var filterCodigo = $filterInputs.filter("[name='filter-value']").val();
        //var filterNombre = $filterInputs.filter("[name='filter-value']").val().toLowerCase();
        var filterProducto = $("#filter-diametrica").val();
        var filterClase = $("#filter-longitud").val();
        //var advancedSearch = $advancedSearch.is(":checked");
        $tableRows.each(function() {
            var rowDataCodigo = $(this).find("td:nth-child(1)").text().toLowerCase();
            var rowDataNombre = $(this).find("td:nth-child(2)").text().toLowerCase();
            var rowDataProducto = $(this).find("td:nth-child(3)").text().toLowerCase();
            var rowDataClase = $(this).find("td:nth-child(4)").text().toLowerCase();

            var matchesCodigo = filterCodigo === '' || rowDataCodigo === filterCodigo;
            //var matchesNombre = filterNombre === '' || rowDataNombre.includes(filterNombre);
            var matchesProducto = filterProducto === '' || rowDataProducto.includes(filterProducto);
            var matchesClase = filterClase === '' || rowDataClase === filterClase;

            if (matchesCodigo  && matchesProducto && matchesClase) {
                $(this).show();
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

//Esta función permite abrir el popup que muestra los detalles, obteniendo los valores traspasados por el botón de detalle. 
//Para ser mostrados en los elementos del popup determinados por su id
function openPopup(codigo, nombre, producto_asociado,rollizo, descripcion,rendimiento,velocidad_linea,setup_time,lead_time,utilizado) {
    document.getElementById('popupCodigo').innerText = codigo;
    document.getElementById('popupNombre').innerText = nombre;
    document.getElementById('popupProductoAsociado').innerText = producto_asociado;
    document.getElementById('popupRollizo').innerText = rollizo;
    document.getElementById('popupPCorteDescripcion').innerText = descripcion;
    document.getElementById('popupPCorteRendimiento').innerText = rendimiento;
    document.getElementById('popupPCorteVelocidadLinea').innerText = velocidad_linea;
    document.getElementById('popupPCorteSetupTime').innerText = setup_time;
    document.getElementById('popupPCorteLeadTime').innerText = lead_time;
    document.getElementById('popupPCorteUtilizado').innerText = utilizado;
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
//Esta función permite abrir y cerrar el popup de carga manual al presionar el botón "Carga manual"
function toggleFormVisibility() {
    const cargaForm = document.querySelector(".form-container-productos form");
    
    if (cargaForm.style.display === "none") {
        cargaForm.style.display = "block";
    } else {
        cargaForm.style.display = "none";
    }
}
// function toggleFormVisibility() {
//     const toggleButton = document.getElementById("toggle-carga-button");
//     const cargaForm = document.querySelector(".form-container-productos form");

//     let isFormVisible = false;

//     toggleButton.addEventListener("click", function() {
//         if (!isFormVisible) {
//             const buttonRect = toggleButton.getBoundingClientRect();
//             const buttonBottom = buttonRect.bottom;
//             cargaForm.style.display = "block";
//             isFormVisible = true;
//         } else {
//             cargaForm.style.display = "none";
//             isFormVisible = false;
//         }
//     });
// }
