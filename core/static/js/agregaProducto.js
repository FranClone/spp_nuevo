// Get the add button and table
const addButton = document.getElementById("add-button");
const table = document.getElementById("product-table");

// Get the first product form
let productForm = document.getElementById("product-form");

// Clone the first product form and add it to the table
addButton.addEventListener("click", function() {
  let newProductForm = productForm.cloneNode(true);
  table.appendChild(newProductForm);
});

// Remove the product form
table.addEventListener("click", function(event) {
  if (event.target.id === "remove-button") {
    event.target.parentNode.parentNode.remove();
  }
});