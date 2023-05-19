$(document).ready(function() {

  // Clone the first product form and add it to the table
  $("#add-button").on("click", function() {
    $("#product-table").append($("#product-form").clone(true));
  });

  // Remove the product form
  $("#product-table").on("click", function(event) {
    if ($(event.target).attr("id") === "remove-button") {
      if ($("#product-table tr").length > 1) { // Verificar si hay más de un producto
        $(event.target).parent().parent().remove();
      } else {
        alert("No puedes eliminar el único producto"); // Mostrar un mensaje de advertencia si solo hay un producto
      }
    } 
  });

});