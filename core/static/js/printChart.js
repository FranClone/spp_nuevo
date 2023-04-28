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

    // Crear el gráfico correspondiente al tipo seleccionado
    if (tipo == "pie") {
        chartAnterior = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Red', 'Blue', 'Yellow'],
                datasets: [{
                    label: '# of Votes',
                    data: [12, 19, 3],
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
    } else if (tipo == "radar") {
        chartAnterior = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Eating', 'Drinking', 'Sleeping', 'Designing', 'Coding', 'Cycling', 'Running'],
                datasets: [{
                    label: 'My First Dataset',
                    data: [65, 59, 90, 81, 56, 55, 40],
                    fill: true,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
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
                labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
                datasets: [{
                    label: '# of Votes',
                    data: [12, 19, 3, 5, 2, 3],
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