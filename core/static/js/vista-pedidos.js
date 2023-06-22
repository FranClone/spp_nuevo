function openPopup(id, nombreBodega, nombreEmpresa, descripcion) {
    document.getElementById('popupId').innerText = id;
    document.getElementById('popupNombreBodega').innerText = nombreBodega;
    document.getElementById('popupNombreEmpresa').innerText = nombreEmpresa;
    document.getElementById('popupDescripcion').innerText = descripcion;
    document.getElementById('popupOverlay').style.display = 'block';
    document.getElementById('popup').style.display = 'block';
}

function closePopup() {
    document.getElementById('popupOverlay').style.display = 'none';
    document.getElementById('popup').style.display = 'none';
}