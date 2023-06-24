$(document).ready(function() {
    $(".filter-button").click(function() {
        $(".filter-form-fields").toggle();
        $(".filter-button").toggleClass("show-filter");
    });

    $("#advanced-search").change(function() {
        if ($(this).is(":checked")) {
            $("#advanced-search-options").show();
        } else {
            $("#advanced-search-options").hide();
        }
    });

    $(".filter-form").submit(function(e) {
        e.preventDefault();
        applyFilter();
    });

    $(".clear-filter-button").click(function() {
        $(".filter-form")[0].reset();
        applyFilter();
    });
    $(".details-button").click(function() {
        var codigo = $(this).data("codigo");
        var nombre = $(this).data("nombre");
        var producto = $(this).data("producto");
        var clase = $(this).data("clase");

        openPopup(codigo, nombre, producto, clase);
    });

    $(".close-button").click(function() {
        closePopup();
    });

    function applyFilter() {
        var filterCodigo = $(".filter-input[name='filter-codigo']").val().toLowerCase();
        var filterNombre = $(".filter-input[name='filter-nombre']").val().toLowerCase();
        var filterProducto = $(".filter-input[name='filter-producto']").val().toLowerCase();
        var filterClase = $(".filter-select[name='filter-clase']").val().toLowerCase();


        $("#patrones-table tbody tr").hide().each(function() {
            var rowDataCodigo = $(this).find("td:nth-child(1)").text().toLowerCase();
            var rowDataNombre = $(this).find("td:nth-child(2)").text().toLowerCase();
            var rowDataProducto = $(this).find("td:nth-child(3)").text().toLowerCase();
            var rowDataClase = $(this).find("td:nth-child(4)").text().toLowerCase();

            var matchesCodigo = filterCodigo === '' || rowDataCodigo === filterCodigo;
            var matchesNombre = filterNombre === '' || rowDataNombre.includes(filterNombre);
            var matchesProducto = filterProducto === '' || rowDataProducto.includes(filterProducto);
            var matchesClase = filterClase === '' || rowDataClase === filterClase;

            if (matchesCodigo && matchesNombre && matchesProducto && matchesClase) {
                $(this).show();
            }
        });

        if ($("#patrones-table tbody tr:visible").length === 0) {
            $(".no-data-message").show();
        } else {
            $(".no-data-message").hide();
        }
    }
    function openPopup(codigo, nombre, producto, clase) {
        $("#popupOverlay").fadeIn();
        $("#popup").fadeIn();
        $("#popup .popup-item:nth-child(1) span").text(codigo);
        $("#popup .popup-item:nth-child(2) span").text(nombre);
        $("#popup .popup-item:nth-child(3) span").text(producto);
        $("#popup .popup-item:nth-child(4) span").text(clase);
    }

    function closePopup() {
        $("#popupOverlay").fadeOut();
        $("#popup").fadeOut();
    }
    // Configuración de DataTables
    $("#patrones-table").DataTable({


    });

});
