// Variable global para almacenar el gráfico anterior
let chartAnterior = null;

function mostrarGrafico(tipo) {
    // Obtener el canvas y el contexto
    const canvas = $('#myChart')[0];
    const ctx = canvas.getContext('2d');
    const imgChart = $('#imgChart');

    // Eliminar el gráfico anterior si lo hay
    if (chartAnterior != null) {
        chartAnterior.destroy();
    }

    // Obtener los datos de pedidos
    const pedidos = pedido_cliente;

    // Calcular la cantidad total de pedidos
    const totalPedidos = pedidos.reduce((total, pedido) => total + pedido.cantidad_pedidos, 0);

    // Crear los arrays de etiquetas y datos
    const nomCliente = [];
    const numPedidos = [];
    const porcentajes = [];

    // Iterar sobre los datos de pedidos y agregar los valores correspondientes a los arrays
    pedidos.forEach(pedido => {
        nomCliente.push(pedido.nombre_cliente);

        // Calcular el porcentaje correspondiente a cada valor
        const porcentaje = (pedido.cantidad_pedidos / totalPedidos) * 100;
        porcentajes.push(porcentaje.toFixed(0) + "%");

        // Agregar el valor de cantidad_pedidos como dato
        numPedidos.push(pedido.cantidad_pedidos);
    });

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
                        '#7a6d5795',
                        '#61525c95',
                        '#6F518895',
                        '#9A776995',
                        '#ffffff95'
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
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const porcentaje = porcentajes[context.dataIndex];
                                return label + ': ' + value + ' (' + porcentaje + ')';
                            }
                        }
                    }
                }
            }
        });
        imgChart.remove();
    } else if (tipo == "line") {
        const meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
        chartAnterior = new Chart(ctx, {
            type: 'line',
            data: {
                labels: meses,
                datasets: [{
                    label: 'Ventas',
                    data: ['1', '2', '4', '7', '5', null, null, null, null, null, null, null],
                    fill: true,
                    backgroundColor: '#fb040595',
                    borderColor: '#61525c95',
                    pointBackgroundColor: '#61525c95',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(255, 99, 132)',
                    pointRadius: 5,
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
        imgChart.remove();
    } else if (tipo == "bar") {
        chartAnterior = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: nomCliente,
                datasets: [{
                    label: '',
                    data: numPedidos,
                    backgroundColor: [
                        '#21130e95',
                        '#7a6d5795',
                        '#fb040595',
                        '#61525c95',
                        '#6F518895',
                        '#9A776995',
                        '#ffffff95'
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
            },
            scales: {
                x: {
                    scaleLabel: {
                        display: true,
                        labelString: 'Eje X'
                    }
                },
                y: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Eje Y'
                    },
                    ticks: {
                        beginAtZero: true,
                        stepSize: 1,
                        precision: 0
                    }
                }]
            }
        });
        imgChart.remove();
    }
}