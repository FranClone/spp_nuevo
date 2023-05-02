// Variable global para almacenar el gráfico anterior
var chartAnterior = null;

function mostrarGrafico(tipo) {
    // Obtener el canvas y el contexto
    var canvas = document.getElementById("myChart");
    var ctx = canvas.getContext("2d");

    // Eliminar el gráfico anterior si lo hay
    if (chartAnterior != null) {
        chartAnterior.destroy();
    }

    // Obtener los datos de pedidos
    var pedidos = pedido_cliente;
    
    // Crear los arrays de etiquetas y datos
    var labels = [];
    var data = [];

    // Iterar sobre los datos de pedidos y agregar los valores correspondientes a los arrays
    for (var i = 0; i < pedidos.length; i++) {
        labels.push(pedidos[i].nombre_cliente);
        data.push(pedidos[i].cantidad_pedidos);
    }

    // Crear el gráfico correspondiente al tipo seleccionado y usar los porcentajes como datos y etiquetas
    if (tipo == "pie") {
        chartAnterior = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Clientes',
                    data: data,
                    backgroundColor: [
                        'rgba(219, 213, 213, 10)',
                        'rgba(131, 131, 131, 10)',
                        'rgba(74, 74, 74, 10)'
                    ],
                    borderColor: [
                        'rgba(0, 0, 0, 8)',
                        'rgba(0, 0, 0, 8)',
                        'rgba(0, 0, 0, 8)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'left',
                    }
                }
            }
        });
    } else if (tipo == "line") {
        chartAnterior = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: '',
                    data: data,
                    fill: true,
                    backgroundColor: 'rgba(255,  99, 132, 0.2)',
                    borderColor: 'rgb(255, 99, 132)',
                    pointBackgroundColor: 'rgb(255, 99, 132)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(255, 99, 132)'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'left',
                    }
                }
            }
        });
    } else if (tipo == "bar") {
        chartAnterior = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: '',
                    data: data,
                    backgroundColor: [
                        'rgba(219, 213, 213, 10)',
                        'rgba(131, 131, 131, 10)',
                        'rgba(74, 74, 74, 10)'
                    ],
                    borderColor: [
                        'rgba(0, 0, 0, 8)',
                        'rgba(0, 0, 0, 8)',
                        'rgba(0, 0, 0, 8)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'left',
                    }
                }
            }
        });
    }

}