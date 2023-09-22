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
                    <h4>¡Hay nuevos pedidos!</h4>
                    <button class="popup-close-pedidos" onclick="hideWelcomePopup()">x</button>
                `;
            } else {
                popupContent.innerHTML = `
                    <h3>¡Bienvenido!</h3>
                    <h4>No Existe una planificación Anterior</h4>
                    <h4>¿Quieres subir nuevos pedidos?</h4>
                    <button type="button" class="carga-button" onclick="showPopupimport(), hideWelcomePopup()">Subir Archivo</button>
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




