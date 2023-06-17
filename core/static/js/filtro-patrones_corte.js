function applyFilter() {
        var filterCodigo = $(".filter-input[name='filter-codigo']").val().toLowerCase();
        var filterNombre = $(".filter-input[name='filter-nombre']").val().toLowerCase();
        var filterProducto = $(".filter-input[name='filter-producto']").val().toLowerCase();
        var filterClase = $(".filter-select[name='filter-clase']").val().toLowerCase();

        $("#patrones-table tbody tr").hide().each(function () {
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
