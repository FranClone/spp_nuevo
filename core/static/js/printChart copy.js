// Variable global para almacenar el gráfico anterior
var chartAnterior = null;

function mostrarGrafico(tipo) {
    // Obtener el canvas y el contexto
    var canvas = document.getElementById("myChart");
    var ctx = canvas.getContext("2d");

    // Realizar una solicitud HTTP GET a la API de Rick y Morty
    fetch("https://rickandmortyapi.com/api/character")
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            // Crear un array de nombres a partir de los objetos JSON de la respuesta
            var nombres = data.results.map(function (personaje) {
                return personaje.name;
            });

            // Crear un objeto para almacenar el recuento de los diferentes estados de los personajes
            var estados = {
                "Alive": 0,
                "Dead": 0,
                "unknown": 0
            };

            // Iterar a través de los objetos JSON de la respuesta y contar el número de personajes en cada estado
            data.results.forEach(function (personaje) {
                estados[personaje.status] += 1;
            });

            // Calcular el porcentaje de cada estado en función del número total de personajes
            var totalPersonajes = data.results.length;
            var porcentajeAlive = (estados["Alive"] / totalPersonajes * 100).toFixed(0);
            var porcentajeDead = (estados["Dead"] / totalPersonajes * 100).toFixed(0);
            var porcentajeUnknown = (estados["unknown"] / totalPersonajes * 100).toFixed(0);

            // Eliminar el gráfico anterior si lo hay
            if (chartAnterior != null) {
                chartAnterior.destroy();
            }

            // Crear el gráfico correspondiente al tipo seleccionado y usar los porcentajes como datos y etiquetas
            if (tipo == "pie") {
                chartAnterior = new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: ["Alive (" + porcentajeAlive + "%)", "Dead (" + porcentajeDead + "%)", "Unknown (" + porcentajeUnknown + "%)"],
                        datasets: [{
                            label: 'Status',
                            data: [estados["Alive"], estados["Dead"], estados["unknown"]],
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
                } else if (tipo == "radar") {
                    chartAnterior = new Chart(ctx, {
                        type: 'radar',
                        data: {
                            labels: nombres,
                            datasets: [{
                                label: 'Estado',
                                data: [estados["Alive"], estados["Dead"], estados["unknown"]],
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
        })
}