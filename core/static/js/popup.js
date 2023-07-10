$(document).ready(function () {
    $(".filter-button").click(function () {
        $(".filter-form-fields").toggle();
        $(".filter-button").toggleClass("show-filter");
    });

    $("#advanced-search").change(function () {
        if ($(this).is(":checked")) {
            $("#advanced-search-options").show();
        } else {
            $("#advanced-search-options").hide();
        }
    });

    $(".filter-form").submit(function (e) {
        e.preventDefault();
        applyFilter();
    });

    $(".clear-filter-button").click(function () {
        $(".filter-form")[0].reset();
        applyFilter();
    });
    $(".details-button").click(function () {
        $("#popup").show();
        $("#popupOverlay").show();
    });

    $(".close-button").click(function () {
        $("#popup").hide();
        $("#popupOverlay").hide();
    });
    
    // Configuración de DataTables
    $("#patrones-table").DataTable({

    });
    $("#patrones-table tbody tr").hover(
        function () {
            $(this).css("background-color", "#E3E1E1"); // Reemplaza "darken-color" con el color más oscuro que deseas utilizar
        },
        function () {
            $(this).css("background-color", "white"); // Restablece el color de fondo original al quitar el ratón de la fila
        }
    );
    $("#patrones-table tbody tr").click(function () {
        // Obtén los valores de la fila clicada
        var codigo = $(this).find("td:nth-child(1)").text();
        var nombre = $(this).find("td:nth-child(2)").text();
        var producto = $(this).find("td:nth-child(3)").text();
        var clase = $(this).find("td:nth-child(4)").text();
    
        // Asigna los valores al contenido del popup
        $("#popup span:nth-child(1)").text(codigo);
        $("#popup span:nth-child(2)").text(nombre);
        $("#popup span:nth-child(3)").text(producto);
        $("#popup span:nth-child(4)").text(clase);
    
        // Muestra el popup y el overlay
        $("#popup").show();
        $("#popupOverlay").show();
    });
    
    
    
    
    
    
    
});
