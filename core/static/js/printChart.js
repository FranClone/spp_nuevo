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
            // Crear dos arrays vacíos para los nombres y especies de los personajes
            var nombres = [];
            var especies = [];
            var estado = [];
            var genero = [];

            // Iterar a través de los objetos JSON de la respuesta y añadir los nombres y especies a los arrays
            data.results.forEach(function (personaje) {
                nombres.push(personaje.name);
                estado.push(personaje.status);
                especies.push(personaje.species);
                genero.push(personaje.gender);
            });

            // Eliminar el gráfico anterior si lo hay
            if (chartAnterior != null) {
                chartAnterior.destroy();
            }

            // Crear el gráfico correspondiente al tipo seleccionado y usar los arrays de nombres y especies como datos y etiquetas
            if (tipo == "pie") {
                chartAnterior = new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: estado,
                        datasets: [{
                            label: 'Species',
                            data: nombres  ,
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
                        labels: nombres,
                        datasets: [{
                            label: 'Species',
                            data: especies,
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
        })
}