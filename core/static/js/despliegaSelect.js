
const select = document.querySelector('#select');
const opciones = document.querySelector('#opciones');
const contenidoSelect = document.querySelector('#select .contenido-select');
const hiddenInput = document.querySelector('#inputSelect');

document.querySelectorAll('#opciones > #opcion').forEach((opcion) => {
  opcion.addEventListener('click', (e) => {
    e.preventDefault();
    contenidoSelect.innerHTML = e.currentTarget.innerHTML;
    select.classList.toggle('active');
    opciones.classList.toggle('active');
    hiddenInput.value = e.currentTarget.querySelector('.titulo').innerText;
  });
});

select.addEventListener('click',() => {
  select.classList.toggle('active');
  opciones.classList.toggle('active');
});
/*
// Selecciona el elemento HTML con el identificador "select" y lo almacena en la variable "select"
const select = document.querySelector('#select');

// Selecciona el elemento HTML con el identificador "opciones" y lo almacena en la variable "opciones"
const opciones = document.querySelector('#opciones');

// Selecciona el elemento HTML con el identificador "select" y la clase "contenido-select", y lo almacena en la variable "contenidoSelect"
const contenidoSelect = document.querySelector('#select .contenido-select');

// Selecciona el elemento HTML con el identificador "inputSelect" y lo almacena en la variable "hiddenInput"
const hiddenInput = document.querySelector('#inputSelect');

// Itera sobre cada elemento HTML que tenga el identificador "opcion" dentro de "opciones"
document.querySelectorAll('#opciones > #opcion').forEach((opcion) => {

  // Añade un evento "click" a cada opción
  opcion.addEventListener('click', (e) => {

    // Evita el comportamiento predeterminado del evento "click" (navegación a otra página)
    e.preventDefault();

    // Actualiza el contenido del elemento "contenido-select" con el contenido de la opción seleccionada
    contenidoSelect.innerHTML = e.currentTarget.innerHTML;

    // Alterna la clase "active" en los elementos "select" y "opciones"
    select.classList.toggle('active');
    opciones.classList.toggle('active');

    // Actualiza el valor del campo de entrada oculto con el texto del título de la opción seleccionada
    hiddenInput.value = e.currentTarget.querySelector('.titulo').innerText;
  });
});

// Añade un evento "click" al elemento "select"
select.addEventListener('click',() => {

  // Alterna la clase "active" en los elementos "select" y "opciones"
  select.classList.toggle('active');
  opciones.classList.toggle('active');
});
*/