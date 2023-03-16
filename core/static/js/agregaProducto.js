$(document).ready(function() {

  // Clone the first product form and add it to the table
  $("#add-button").on("click", function() {
    $("#product-table").append($("#product-form").clone(true));
  });

  // Remove the product form
  $("#product-table").on("click", function(event) {
    if ($(event.target).attr("id") === "remove-button") {
      $(event.target).parent().parent().remove();
    } 
  });

});