$(document).ready(function() {
  const select = $('#select'); // Selecciona el elemento con el ID "select"
  const opciones = $('#opciones'); // Selecciona el elemento con el ID "opciones"
  const contenidoSelect = $('#select .contenido-select'); // Selecciona el elemento con la clase "contenido-select" dentro de "select"
  const hiddenInput = $('#inputSelect'); // Selecciona el elemento con el ID "inputSelect"

  opciones.on('click', '#opcion', function(e) {
    e.preventDefault();
    contenidoSelect.html($(this).html()); // Actualiza el contenido de "contenidoSelect" con el HTML del elemento clicado
    select.toggleClass('active'); // Alterna la clase "active" en el elemento "select"
    opciones.toggleClass('active'); // Alterna la clase "active" en el elemento "opciones"
    hiddenInput.val($(this).find('.titulo').text()); // Actualiza el valor de "hiddenInput" con el texto del elemento clicado con la clase "titulo"
  });

  select.on('click', function() {
    select.toggleClass('active'); // Alterna la clase "active" en el elemento "select"
    opciones.toggleClass('active'); // Alterna la clase "active" en el elemento "opciones"
  });
});
