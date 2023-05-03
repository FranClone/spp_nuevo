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

    // Calcular la cantidad total de pedidos
    var totalPedidos = 0;
    for (var i = 0; i < pedidos.length; i++) {
        totalPedidos += pedidos[i].cantidad_pedidos;
    }

    // Crear los arrays de etiquetas y datos
    var nomCliente = [];
    var numPedidos = [];
    var porcentajes = [];

    // Iterar sobre los datos de pedidos y agregar los valores correspondientes a los arrays
    for (var i = 0; i < pedidos.length; i++) {
        nomCliente.push(pedidos[i].nombre_cliente);

        // Calcular el porcentaje correspondiente a cada valor
        var porcentaje = (pedidos[i].cantidad_pedidos / totalPedidos) * 100;
        porcentajes.push(porcentaje.toFixed(1) + "%");

        // Agregar el valor de cantidad_pedidos como dato
        numPedidos.push(pedidos[i].cantidad_pedidos);
    }


    // Crear el gráfico correspondiente al tipo seleccionado y usar los porcentajes como datos y etiquetas
    if (tipo == "pie") {
        chartAnterior = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: nomCliente,
                datasets: [{
                    label: 'Clientes',
                    data: numPedidos,
                    backgroundColor: [
                        '#fb040595',
                        '#21130e95',
                        '#a0432895',
                        '#7a6d5795',
                        '#61525c95'
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
                    },
                    title: {
                        display: true,
                        text: 'Cantidad de pedidos por clientes',
                        align: 'start', 
                        padding: {
                            top: 20
                        },
                        
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                var label = context.label || '';
                                var value = context.parsed || 0;
                                var porcentaje = porcentajes[context.dataIndex];
                                return label + ': ' + value + ' (' + porcentaje + ')';
                            }
                        }
                    }
                }
            }
        });
    } else if (tipo == "line") {
        chartAnterior = new Chart(ctx, {
            type: 'line',
            data: {
                labels: nomCliente,
                datasets: [{
                    label: '',
                    data: numPedidos,
                    fill: true,
                    backgroundColor: '#ff000080',
                    borderColor: '#61525c95',
                    pointBackgroundColor: '#61525c95',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(255, 99, 132)',
                    beginAtZero: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'left',
                    }
                }
            },
            title: {
                display: true,
                text: 'Cantidad de pedidos por mes (EN CONSTUCCIÓN)',
                align: 'start', 
                padding: {
                    top: 20
                }
            },
            scales: {
                x: {
                    scaleLabel: {
                        display: true,
                        labelString: 'Eje X'
                    },
                    ticks: {
                        beginAtZero: true
                    }
                },
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Eje Y'
                    },
                    ticks: {
                        beginAtZero: true
                    }
                }]
            } 
        });
    } else if (tipo == "bar") {
        chartAnterior = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: nomCliente,
                datasets: [{
                    label: '',
                    data: numPedidos,
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
            title: {
                display: true,
                text: 'pensando que debo mostrar(EN CONSTUCCIÓN)',
                align: 'start', 
                padding: {
                    top: 20
                }
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'left',
                    }
                }
            },
            scales: {
                x: {
                    scaleLabel: {
                        display: true,
                        labelString: 'Eje X'
                    }
                },
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Eje Y'
                    },
                    ticks: {
                        beginAtZero: true
                    }
                }]
            } 
        });
    }

}