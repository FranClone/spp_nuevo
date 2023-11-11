function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}
function getCookie(name) {
    const cookieName = `${name}=`;
    const decodedCookie = decodeURIComponent(document.cookie);
    const cookieArray = decodedCookie.split(';');

    for (let i = 0; i < cookieArray.length; i++) {
        let cookie = cookieArray[i];
        while (cookie.charAt(0) === ' ') {
            cookie = cookie.substring(1);
        }
        if (cookie.indexOf(cookieName) === 0) {
            return cookie.substring(cookieName.length, cookie.length);
        }
    }
    return null;
}

// Obtener los IDs previamente vistos de la cookie
const idsPreviosVistos = getCookie('ids_vistos') ? getCookie('ids_vistos').split(',') : [];

// Realizar solicitud AJAX para obtener los IDs de pedidos desde el servidor
function showWelcomePopup() {
    // Obtener los IDs previamente vistos de la cookie
    const idsPreviosVistos = getCookie('ids_vistos') ? getCookie('ids_vistos').split(',') : [];

    // Realizar solicitud AJAX para obtener los IDs de pedidos desde el servidor
    fetch('/obtener-ids-pedidos/')
        .then(response => response.json())
        .then(data => {
            const idsNuevosDesdeBackend = data.ids_pedidos;

            // Encontrar los IDs nuevos
            const nuevosIDs = idsNuevosDesdeBackend.filter(id => !idsPreviosVistos.includes(id.toString()));

            let hayNuevosPedidos = false;

            if (nuevosIDs.length > 0) {
                // Mostrar mensaje para los nuevos IDs
                console.log(`¡Nuevos IDs encontrados! ${nuevosIDs.join(', ')}`);

                // Agregar los nuevos IDs a la lista de IDs vistos
                const idsVistosActualizados = idsPreviosVistos.concat(nuevosIDs);

                // Actualizar la cookie con los IDs vistos
                setCookie('ids_vistos', idsVistosActualizados.join(','), 365); // Guardar por 1 año

                hayNuevosPedidos = true;
            }

            console.log(`¿Hay nuevos pedidos? ${hayNuevosPedidos}`);

            const popupOverlay = document.getElementById('welcome-popup');
            const popupContent = document.querySelector('.popup-content-pedidos');

            if (hayNuevosPedidos) {
                popupContent.innerHTML = `
                    <h3>¡Bienvenido!</h3>
                    <h4>¿Quieres subir nuevos pedidos?</h4>
                    <button type="button" class="carga-button" onclick="showPopupimport(), hideWelcomePopup()">Cargar Pedido</button>
                    <button class="popup-close-pedidos" onclick="hideWelcomePopup()">x</button>
                `;
            } else {
                popupContent.innerHTML = `
                <h3>¡Bienvenido!</h3>
                <h4>¿Quieres subir nuevos pedidos?</h4>
                <button type="button" class="carga-button" onclick="showPopupimport(), hideWelcomePopup()">Cargar Pedido</button>
                <button class="popup-close-pedidos" onclick="hideWelcomePopup()">x</button>
                `;
            }

            popupOverlay.style.display = 'block';
        })
        .catch(error => {
            console.error("Error al obtener los IDs de pedidos:", error);
        });
}

function hideWelcomePopup() {
    const popupOverlay = document.getElementById('welcome-popup');
    popupOverlay.style.display = 'none';
}

window.onload = function () {
    showWelcomePopup();
};



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


