
class Gantt {
    constructor(tasks) {
        this.tasks = tasks;
        this.dateWidth = 178;
        this.filteredTasks = tasks;
        this.setMinAndMaxDate();
        this.attachEventListeners();
    }

    setMinAndMaxDate() {
        var maxDates = [];
        var minDates = [];

        for (let i = 0; i < this.tasks.length; i++) {
            minDates.push(new Date(this.tasks[i][1]));
            maxDates.push(new Date(this.tasks[i][2]));
        }
        this.minDate = new Date(Math.min.apply(null, minDates));
        this.maxDate = new Date(Math.max.apply(null, maxDates));
    }
    //Revisar Filtros semana, meses
    diffInMonths(max, min) {
        return (max.getFullYear() - min.getFullYear()) * 12 + max.getMonth() - min.getMonth();
    }

    diffInWeeks(max, min) {
        const oneWeek = 7 * 24 * 60 * 60 * 1000;
        const diffTime = Math.abs(max - min);
        return Math.ceil(diffTime / oneWeek);
    }


// Plan2Table() {
//     var html = '<table class="event-table second-table"><thead><tr>';
//     html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Id Demanda</th>';
//     html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Producto</th>';
//     html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Alto</th>';
//     html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Ancho</th>';
//     html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Largo</th>';
//     html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Medida_Producto</th>';
//     html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Dias Produccion</th>';
//     html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Pqtes Solicitados</th>';
//     html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Pqtes dia</th>';
//     html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">M3</th>';
//     // Añade los encabezados de las otras columnas aquí
//     html += '</tr></thead><tbody>';

//     // Utiliza un conjunto para mantener un registro de los valores únicos de task[66]
//     var uniqueDemandValues = new Set();

//     for (let i = 0; i < this.filteredTasks.length; i++) {
//         var task = this.filteredTasks[i];
//         var demanda = task[66]; // Obtén el valor de la demanda

//         // Verifica si el valor de la demanda ya se ha agregado a la tabla
//         if (!uniqueDemandValues.has(demanda)) {
//             uniqueDemandValues.add(demanda);

//             // Crea una fila para la demanda actual
//             html += '<tr>';
//             html += `<td class="right-align">${demanda}</td>`; // Columna de la demanda
//             html += `<td class="right-align">${task[7]}</td>`; // Columna de la demanda
//             html += `<td class="right-align">${task[17]}</td>`; // Columna de la demanda
//             html += `<td class="right-align">${task[18]}</td>`; // Columna de la demanda
//             html += `<td class="right-align">${task[19]}</td>`; // Columna de la demanda
//             html += `<td class="right-align">${task[64]}</td>`; // Columna de la demanda
//             html += `<td class="right-align">${task[65]}</td>`; // Columna de la demanda
//             html += `<td class="right-align">${task[61]}</td>`; // Columna de la demanda
//             html += `<td class="right-align">${task[62]}</td>`; // Columna de la demanda
//             html += `<td class="right-align">${task[63]}</td>`; // Columna de la demanda
//             // Añade el resto de los valores de task en las celdas de la fila

//             html += '</tr>';
//         }
//     }

//     html += '</tbody></table>';
//     return html;
// }


    //     const groupedRows = {};

    //     // Iterar sobre cada producto y crear una fila por producto
    //     for (let i = 0; i < this.filteredTasks.length; i++) {
    //         var task = this.filteredTasks[i];
    //         // Agrega un mensaje para rastrear el progreso


    //         // El pedido aún no ha vencido, procesa el pedido y agrégalo a la tabla
    //         for (let j = 0; j < task[64].length; j++) {
    //             var m = task[64][j];
    //             bodyHtml += `<td class="right-align">${m}</td>`;/*OP Orden Interna*/
    //             bodyHtml += `<td class="right-align">${task[61]}</td>`;/*OP Orden Interna*/
    //             bodyHtml += `<td class="right-align">${task[62]}</td>`;/*OP Orden Interna*/
    //             bodyHtml += `<td class="right-align">${task[63]}</td>`;/*OP Orden Interna*/
    //             bodyHtml += '</tr>';

    //         }



    //     }

    //     html += bodyHtml;
    //     html += '</tbody></table>';
    //     return html;
    // }

    PlanPedidoTable() {
        var html = '<table  class="event-table second-table"><thead><tr>';

        // Agregar dos columnas adicionales a la izquierda
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Fecha Carga</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">OP</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Mercado</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">ETA</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Destino</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Programa</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Detalles</th>';


        // Obtén la fecha actual
        const currentDate = new Date();

        // Calcula la fecha 10 días después
        const tenDaysLater = new Date(currentDate);
        tenDaysLater.setDate(currentDate.getDate() + 10);

        // Agrega las fechas al encabezado
        for (let date = new Date(currentDate); date <= tenDaysLater; date.setDate(date.getDate() + 1)) {
            const formattedDate = this.formatDate(date, "diario");
            html += '<th style="color: white; width: 70vh; font-size: 13px;">' + formattedDate + '</th>';
        }

        html += '</tr></thead><tbody>';

        // Utiliza una variable diferente para el cuerpo de la tabla
        var bodyHtml = '';

        var uniqueOrdenPedido = [];

        this.filteredTasks.sort((task1, task2) => {
            const fechaETA1 = new Date(task1[2]);
            const fechaETA2 = new Date(task2[2]);
            return fechaETA1 - fechaETA2;
        });

        for (let i = 0; i < this.filteredTasks.length; i++) {
            var task = this.filteredTasks[i];

            if (!uniqueOrdenPedido.includes(task[0])) {

                const fechaETA = new Date(task[2]);
                const currentDate = new Date();

                if (fechaETA >= currentDate) {


                    const dMin = new Date(task[3]);
                    const dMax = new Date(task[2]);

                    // Calcular la diferencia en días entre dMin y dMax
                    var dateDiff = this.diffInDays(dMax, dMin);

                    var daysBefore = this.diffInDays(this.minDate, dMin);
                    var daysAfter = this.diffInDays(dMax, this.maxDate);

                    // Ensure that daysBefore is at least 0 (minimum start date constraint)
                    daysBefore = Math.max(daysBefore, 0);

                    // Ensure that daysAfter is at least 0 (maximum end date constraint)
                    daysAfter = Math.max(daysAfter, 0);

                    // Restar la fecha actual para ver cuántos días quedan
                    const fechaActual = new Date(); // Obtener la fecha actual
                    var diasRestantes = this.diffInDays(dMax, fechaActual);



                    bodyHtml += '<tr>';
                    const fechaISO = task[1];/*Fecha de carga*/
                    const fechaISO2 = task[2];/*ETA*/
                    const fechaFormateada = new Date(fechaISO).toLocaleDateString('es-ES');/*Fecha de carga*/
                    const fechaFormateada2 = new Date(fechaISO2).toLocaleDateString('es-ES');/*ETA*/


                    // Agregar el valor de task[7] en la primera columna
                    bodyHtml += `<td style="text-align: center;">${fechaFormateada}</td>`; /*Fecha de carga*/
                    bodyHtml += `<td class="right-align">${task[0]}</td>`;/*OP Orden Interna*/
                    bodyHtml += `<td class="left-align">${task[38]}</td>`; /*Mercado*/
                    bodyHtml += `<td style="text-align: center;">${fechaFormateada2}</td>`; /*ETA*/
                    bodyHtml += `<td class="left-align">${task[39]}</td>`; /*Destino*/
                    bodyHtml += `<td class="left-align">${task[54]}</td>`; /*Programa*/
                    bodyHtml += `<td  style="text-align: center;"><a class="popup-link" data-pedido-id="${i}" data-popup-type="pedido">Ver...</a></td>`; /*Detalle*/

                    for (let day = 0; day < 11; day++) {
                        bodyHtml += '<td class="event-cell';
                        if (day < diasRestantes) {
                            bodyHtml += ' has-paquetes">';
                        } else {
                            bodyHtml += '"></td>';
                        }

                        bodyHtml += '</td>';
                    }

                    bodyHtml += '</tr>';
                    uniqueOrdenPedido.push(task[0]);
                }
            }
        }

        html += bodyHtml;

        html += '</tbody></table>';
        return html;
    }



    PlanTable() {

        var html = '<table class="event-table second-table"><thead><tr>';
        html += '<tr>'
        html += '<th style="color: white; width: 45vh; font-size: 15px; text-align: center; height:3vh;"></th>';
        html += '<th style="color: white; width: 45vh; font-size: 15px; text-align: center; height:3vh;" colspan="3">Escuadrias</th>';
        html += '<th style="color: white; width: 45vh; font-size: 15px; text-align: center; height:3vh;" colspan="4"></th>';
        html += '<th style="color: white; width: 45vh; font-size: 15px; text-align: center; height:3vh;" colspan="11">Paquetes a Producir</th>';
        html += '</tr>'
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Producto</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Largo <br> (cm)</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Ancho <br> (cm)</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Alto <br> (cm)</th>';

        // Continuar con los demás encabezados
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Pqtes.Solicitados</th>';
       // html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Pqtes.Saldo</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">M3 <br> (cm)</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Detalles</th>';

        // Obtén la fecha actual
        const currentDate = new Date();

        // Calcula la fecha 10 días después
        const tenDaysLater = new Date(currentDate);
        tenDaysLater.setDate(currentDate.getDate() + 10);
        // Agrega las fechas al encabezado
        for (let date = new Date(currentDate); date <= tenDaysLater; date.setDate(date.getDate() + 1)) {
            const formattedDate = this.formatDate(date, "diario");
            html += '<th style="color: white; width: 70vh; font-size: 13px;">' + formattedDate + '</th>';
        }

        html += '</tr></thead><tbody>';

        // Utiliza una variable diferente para el cuerpo de la tabla
        var bodyHtml = '';

        const groupedRows = {};

        // Iterar sobre cada producto y crear una fila por producto
        for (let i = 0; i < this.filteredTasks.length; i++) {
            var task = this.filteredTasks[i];
            // Agrega un mensaje para rastrear el progreso

            // Obtén la fecha de ETA del pedido
            const fechaETA = new Date(task[2]); // Suponiendo que task[2] representa la fecha de ETA
            // Obtén la fecha actual
            const currentDate = new Date();
            // Verifica si la fecha de ETA ya ha pasado
            if (fechaETA >= currentDate) {
                // El pedido aún no ha vencido, procesa el pedido y agrégalo a la tabla
                for (let j = 0; j < task[7].length; j++) {
                    var product = task[7][j];

                    var key = `${product}_${task[19]}_${task[18]}_${task[17]}`; // Crear una clave única para agrupar
                    if (!groupedRows[key]) {
                        groupedRows[key] = {
                            product: product,
                            largo: task[19],
                            ancho: task[18],
                            alto: task[17],
                            cantidad: 0,
                            cantidadm3: 0,
                            detalles: [],
                            fechaInicio: new Date(task[3]),
                            fechaFin: new Date(task[2]),
                            ids: []

                        };
                    }
                    let target = task[45];
                    let sum = 0;
                    let randomNumbers = [];

                    while (sum < target) {
                        let randomNumber = Math.floor(Math.random() * (target - sum)) + 1;
                        sum += randomNumber;
                        randomNumbers.push(randomNumber);
                        if (sum >= target) {
                            break;
                        }
                    }

                    groupedRows[key].cantidad += parseInt(task[45], 10);
                    groupedRows[key].cantidadm3 += parseFloat(task[20]);
                    groupedRows[key].detalles.push({
                        color: task[15],
                        randomNumbers: randomNumbers,
                        i: i,
                    });

                    groupedRows[key].ids.push(i);
                }


            }
        }

        let maxFechaLejanaPorFila = new Date(0); // Inicializar con una fecha muy antigua

        for (let key in groupedRows) {
            let row = groupedRows[key];
            const ids = row.ids;

            for (let id of ids) {
                const fechaTask2 = new Date(this.filteredTasks[id][2]); // Obtén la fecha de task[2] con el ID
                const currentDate = new Date(); // Obtén la fecha actual

                // Calcula la diferencia de días entre la fecha de task[2] y la fecha actual
                const dateDiff = Math.floor((fechaTask2 - currentDate) / (1000 * 60 * 60 * 24));

                if (dateDiff > maxFechaLejanaPorFila) {
                    maxFechaLejanaPorFila = dateDiff;
                }

            }

        }



        const sortedRows = Object.values(groupedRows).sort((a, b) => {
            const productNameA = a.product.toLowerCase();
            const productNameB = b.product.toLowerCase();
            return productNameA.localeCompare(productNameB);
        });
        // Check if the date is today


        const botonReplanificar = document.getElementById('ejecutarBoton');
        botonReplanificar.addEventListener('click', replanificar);

        function replanificar() {
            // Limpiar los valores almacenados en localStorage
            for (let i = 0; i < sortedRows.length; i++) {
                localStorage.removeItem(`paquetesGenerados_${i}`);
            }

            // Recargar la página o actualizar los valores directamente si es posible sin recargar
            location.reload(); // Esto recargará la página para que los números aleatorios se regeneren
        }

        for (let index = 0; index < sortedRows.length; index++) {
            const sortedRow = sortedRows[index];
            const ids = sortedRow.ids.join(', ');
            var dateDiff = this.diffInDays(sortedRow.fechaFin, sortedRow.fechaInicio);
            maxFechaLejanaPorFila = Math.min(maxFechaLejanaPorFila, 11);
        
            function roundToThreeDecimals(number) {
                const roundedNumber = Math.round(number * 1000) / 1000;
                return roundedNumber;
            }
        
            bodyHtml = '<tr>';
            bodyHtml += `<td>${sortedRow.product}</td>`;
            bodyHtml += `<td class="right-align">${sortedRow.largo.toLocaleString()}</td>`;
            bodyHtml += `<td class="right-align">${sortedRow.ancho.toLocaleString()}</td>`;
            bodyHtml += `<td class="right-align">${sortedRow.alto.toLocaleString()}</td>`;
            bodyHtml += `<td class="right-align">${sortedRow.cantidad}</td>`;
            bodyHtml += `<td class="right-align">${roundToThreeDecimals(sortedRow.cantidadm3).toString().replace('.', ',')}</td>`;
            bodyHtml += `<td class="left-align"><a class="popup-link" data-popup-type="producto" data-pedido-id="${ids}">Ver detalles</a></td>`;
            let paquetesPorDia = new Array(maxFechaLejanaPorFila).fill(0);
            let paquetesGuardados = localStorage.getItem(`paquetesGenerados_${index}`); // Usamos el índice como parte del identificador
        

        
            if (paquetesGuardados) {
                paquetesPorDia = JSON.parse(paquetesGuardados);
            } else {
                paquetesPorDia = new Array(maxFechaLejanaPorFila).fill(0);
        
                for (let i = 0; i < sortedRow.detalles.length; i++) {
                    let detalle = sortedRow.detalles[i];
                    for (let l = 0; l < detalle.randomNumbers.length; l++) {
                        let diaAleatorio = Math.floor(Math.random() * maxFechaLejanaPorFila);
                        paquetesPorDia[diaAleatorio] += detalle.randomNumbers[l];
                    }
                }
        
                localStorage.setItem(`paquetesGenerados_${index}`, JSON.stringify(paquetesPorDia));
            }
        
            for (let k = 0; k < paquetesPorDia.length; k++) {
                bodyHtml += '<td class="event-cell';
                if (paquetesPorDia[k] > 0) {
                    bodyHtml += ' has-paquetes">';
                    bodyHtml += `<div style="text-align: center; font-size:1vh;"> ${paquetesPorDia[k]}</div>`;
                } else {
                    bodyHtml += '"></td>';
                }
                bodyHtml += '</td>';
            }
            bodyHtml += '</tr>';
        
            html += bodyHtml;
        }
        
        html = `<table>${html}</table>`;
        return html;

     
    }


    PedidoTable() {
        var html = '<table id="miTabla" class="event-table" style="margin-left: auto; margin-right: auto;" class="second-table"><thead><tr>';

        // Agregar dos columnas adicionales a la izquierda
        html += '<th style="color: white; width: 20vh; font-size: 15px; text-align: center; height:3vh;">Fecha carga</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">OP</th>';
        html += '<th style="color: white; width: 50vh; font-size: 15px; text-align: center; height:3vh;">Cliente</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Mercado</th>';
        html += '<th style="color: white; width: 10vh; font-size: 15px; text-align: center; height:3vh;">ETA</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Destino</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Programa</th>';
        html += '<th style="color: white; width: 20vh; font-size: 15px; text-align: center; height:3vh;">Detalle</th>';



        html += '</tr></thead><tbody>';

        // Utiliza una variable diferente para el cuerpo de la tabla
        var bodyHtml = '';

        // Maintain a list of unique orden_pedido values
        var uniqueOrdenPedido = [];
        for (let i = 0; i < this.filteredTasks.length; i++) {
            var task = this.filteredTasks[i];
            // Agrega un mensaje para rastrear el progreso

            // Obtén la fecha de ETA del pedido
            const fechaETA = new Date(task[2]); // Suponiendo que task[2] representa la fecha de ETA
            // Obtén la fecha actual
            const currentDate = new Date();
            // Verifica si la fecha de ETA ya ha pasado
            if (fechaETA >= currentDate) {
                // El pedido aún no ha vencido, procesa el pedido y agrégalo a la tabla
                for (let j = 0; j < task[7].length; j++) {
                    var product = task[7][j];

                    // Check if orden_pedido already exists in the uniqueOrdenPedido list
                    if (!uniqueOrdenPedido.includes(task[0])) {

                        const fechaISO = task[1];/*Fecha de carga*/
                        const fechaISO2 = task[2];/*ETA*/
                        const fechaFormateada = new Date(fechaISO).toLocaleDateString('es-ES');/*Fecha de carga*/
                        const fechaFormateada2 = new Date(fechaISO2).toLocaleDateString('es-ES');/*ETA*/

                        bodyHtml += `<td style="text-align: center;">${fechaFormateada}</td>`; /*Fecha de carga*/
                        bodyHtml += `<td class="right-align">${task[0]}</td>`;/*OP Orden Interna*/
                        bodyHtml += `<td class="left-align">${task[5]}</td>`; /*Cliente*/
                        bodyHtml += `<td class="left-align">${task[38]}</td>`; /*Mercado*/
                        bodyHtml += `<td style="text-align: center;">${fechaFormateada2}</td>`; /*ETA*/
                        bodyHtml += `<td class="left-align">${task[39]}</td>`; /*Destino*/
                        bodyHtml += `<td class="left-align">${task[54]}</td>`; /*Programa*/
                        bodyHtml += `<td  style="text-align: center;"><a class="popup-link" data-pedido-id="${i}" data-popup-type="pedido">Ver...</a></td>`; /*Detalle*/

                        bodyHtml += '</tr>';

                        // Add the orden_pedido to the uniqueOrdenPedido list
                        uniqueOrdenPedido.push(task[0]);
                    }
                }
            }
        }

        // Agrega el cuerpo de la tabla al encabezado
        html += bodyHtml;

        html += '</tbody></table>';

        return html;
    }

    ProductosTable() {
        var html = '<table class="event-table second-table"><thead><tr>';
        html += '<tr>'
        html += '<th style="color: white; font-size: 15px; text-align: center; height:3vh;"></th>';
        html += '<th style="color: white; font-size: 15px; text-align: center; height:3vh;" colspan="3">Escuadrias</th>';
        html += '<th style="color: white; font-size: 15px; text-align: center; height:3vh;" colspan="4"></th>';
        html += '</tr>'
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Producto</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Largo <br> (cm)</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Ancho <br> (cm)</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Alto <br> (cm)</th>';

        // Continuar con los demás encabezados
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Pqtes <br> Solicitados</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">M3 <br> (cm)</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Detalles</th>';

        html += '</tr></thead><tbody>';

        // Utiliza una variable diferente para el cuerpo de la tabla
        var bodyHtml = '';

        const groupedRows = {};

        // Iterar sobre cada producto y crear una fila por producto
        for (let i = 0; i < this.filteredTasks.length; i++) {
            var task = this.filteredTasks[i];
            // Agrega un mensaje para rastrear el progreso

            // Obtén la fecha de ETA del pedido
            const fechaETA = new Date(task[2]); // Suponiendo que task[2] representa la fecha de ETA
            // Obtén la fecha actual
            const currentDate = new Date();
            // Verifica si la fecha de ETA ya ha pasado
            if (fechaETA >= currentDate) {
                // El pedido aún no ha vencido, procesa el pedido y agrégalo a la tabla
                for (let j = 0; j < task[7].length; j++) {
                    var product = task[7][j];

                    var key = `${product}_${task[19]}_${task[18]}_${task[17]}`; // Crear una clave única para agrupar
                    if (!groupedRows[key]) {
                        groupedRows[key] = {
                            product: product,
                            largo: task[19],
                            ancho: task[18],
                            alto: task[17],
                            cantidad: 0,
                            cantidadm3: 0,
                            detalles: [],
                            fechaInicio: new Date(task[3]),
                            fechaFin: new Date(task[2]),
                            ids: []

                        };
                    }
                    let target = task[45];
                    let sum = 0;
                    let randomNumbers = [];

                    while (sum < target) {
                        let randomNumber = Math.floor(Math.random() * (target - sum)) + 1;
                        sum += randomNumber;
                        randomNumbers.push(randomNumber);
                        if (sum >= target) {
                            break;
                        }
                    }

                    groupedRows[key].cantidad += parseInt(task[45], 10);
                    groupedRows[key].cantidadm3 += parseFloat(task[20]);
                    groupedRows[key].detalles.push({
                        color: task[15],
                        randomNumbers: randomNumbers,
                        i: i,
                    });

                    groupedRows[key].ids.push(i);
                }
            }
        }

        let maxFechaLejanaPorFila = new Date(0); // Inicializar con una fecha muy antigua

        for (let key in groupedRows) {
            let row = groupedRows[key];
            const ids = row.ids;

            for (let id of ids) {
                const fechaTask2 = new Date(this.filteredTasks[id][2]); // Obtén la fecha de task[2] con el ID
                const currentDate = new Date(); // Obtén la fecha actual

                // Calcula la diferencia de días entre la fecha de task[2] y la fecha actual
                const dateDiff = Math.floor((fechaTask2 - currentDate) / (1000 * 60 * 60 * 24));

                if (dateDiff > maxFechaLejanaPorFila) {
                    maxFechaLejanaPorFila = dateDiff;
                }
            }
        }


        const sortedRows = Object.values(groupedRows).sort((a, b) => {
            const productNameA = a.product.toLowerCase();
            const productNameB = b.product.toLowerCase();
            return productNameA.localeCompare(productNameB);
        });


        for (let sortedRow of sortedRows) { // Cambia el nombre de la variable a sortedRow
            const ids = sortedRow.ids.join(', ');
            var dateDiff = this.diffInDays(sortedRow.fechaFin, sortedRow.fechaInicio);
            maxFechaLejanaPorFila = Math.min(maxFechaLejanaPorFila, 11);
            function roundToThreeDecimals(number) {
                const roundedNumber = Math.round(number * 1000) / 1000;
                return roundedNumber;
            }

            bodyHtml += '<tr>';
            bodyHtml += `<td>${sortedRow.product}</td>`;
            bodyHtml += `<td class="right-align">${sortedRow.largo.toLocaleString()}</td>`;
            bodyHtml += `<td class="right-align">${sortedRow.ancho.toLocaleString()}</td>`;
            bodyHtml += `<td class="right-align">${sortedRow.alto.toLocaleString()}</td>`;
            bodyHtml += `<td class="right-align">${sortedRow.cantidad}</td>`;
            bodyHtml += `<td class="right-align">${roundToThreeDecimals(sortedRow.cantidadm3).toString().replace('.', ',')}</td>`;
            bodyHtml += `<td class="left-align"><a class="popup-link" data-popup-type="producto" data-pedido-id="${ids}">Ver detalles</a></td>`;

        }

        bodyHtml += '</tr>';


        html += bodyHtml;
        html += '</tbody></table>';
        return html;
    }

    PatronTable() {
        var html = '<table class="second-table"><thead><tr>';

        // Agregar dos columnas adicionales a la izquierda

        html += '<th style="color: white; width: 30vh; font-size: 13px;">Nro Pedido</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">diametro <br> (cm)</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Largo Trozo <br> (cm)</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Cantidad Piezas</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Producto Asociado</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Detalles</th>';


        html += '</tr></thead><tbody>';

        // Utiliza una variable diferente para el cuerpo de la tabla
        var bodyHtml = '';

        // Itera sobre cada producto y crea una fila por producto
        for (let i = 0; i < this.filteredTasks.length; i++) {
            var task = this.filteredTasks[i];
            bodyHtml += `<td class="right-align">${task[0]}</td>`;/*Nro Pedido*/
            bodyHtml += `<td class="right-align">${task[35]}</td>`;/*Diametro*/
            bodyHtml += `<td class="right-align">${task[24].toLocaleString()}</td>`;/*Largo Trozo*/
            bodyHtml += `<td class="right-align">${task[28]}</td>`;/*Cantidad Piezas*/
            bodyHtml += `<td class="left-align">${task[44]}</td>`;/*Producto Asociado*/
            bodyHtml += `<td><a class="popup-link" data-pedido-id="${i}" data-popup-type="patron">Ver...</a></td>`;/*Detalle*/

            bodyHtml += '</tr>';

        }

        // Agrega el cuerpo de la tabla al encabezado
        html += bodyHtml;

        html += '</tbody></table>';
        return html;
    }

    showPedidosTable() {
        this.filteredTasks = this.tasks;
        document.getElementById('gantt').innerHTML = this.PedidoTable();
    }


    showProductosTable() {
        this.filteredTasks = this.tasks;
        document.getElementById('gantt').innerHTML = this.ProductosTable();
    }

    showPatronesTable() {
        this.filteredTasks = this.tasks;
        document.getElementById('gantt').innerHTML = this.PatronTable();
    }


    showPlanTable() {
        this.filteredTasks = this.tasks;
        document.getElementById('gantt').innerHTML = this.PlanTable();
    }

    // showPlan2Table() {
    //     this.filteredTasks = this.tasks;
    //     document.getElementById('gantt').innerHTML = this.Plan2Table();
    // }

    showPlanPedidoTable() {
        this.filteredTasks = this.tasks;
        document.getElementById('gantt').innerHTML = this.PlanPedidoTable();
    }


    diffInDays(max, min) {
        var diffTime = Math.abs(max - min);
        return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    }

    formatDate(date, period, endDate) {
        const day = date.getDate();
        const month = date.getMonth() + 1;
        const year = date.getFullYear();

        // Agrega ceros iniciales si es necesario
        const formattedDay = day < 10 ? '0' + day : day;
        const formattedMonth = month < 10 ? '0' + month : month;

        if (period === "diario") {
            return `${formattedDay}-${formattedMonth}-${year}`;
        } else if (period === "semanal") {
            const weekStart = new Date(date);
            weekStart.setDate(weekStart.getDate() - weekStart.getDay() + 1);
            const weekEnd = new Date(weekStart);
            weekEnd.setDate(weekEnd.getDate() + 6);

            const startDay = weekStart.getDate();
            const endDay = weekEnd.getDate();

            return `${formattedDay}-${formattedMonth}-${year} al ${endDay}-${formattedMonth}-${year}`;
        } else if (period === "mensual") {
            const monthStart = new Date(date);
            monthStart.setDate(1);
            const monthEnd = new Date(date);
            monthEnd.setMonth(monthEnd.getMonth() + 1, 0);

            const endDay = monthEnd.getDate();

            if (formattedMonth === monthEnd.getMonth() + 1) {
                return `${formattedDay}-${formattedMonth}-${year}`;
            } else {
                return `${formattedDay}-${formattedMonth}-${year} al ${endDay}-${monthEnd.getMonth() + 1}-${year}`;
            }
        }
    }


    attachEventListeners() {
        const popupLinks = document.querySelectorAll('.popup-link');

        const self = this; // Store a reference to the current instance

        document.getElementById('gantt').addEventListener('click', function (event) {
            const target = event.target;
            if (target.classList.contains('popup-link')) {
                self.handlePopupClick(event);
            }
        });
    }


    handlePopupClick(event) {
        event.stopPropagation();// Evita que el evento se propague al contenedor principal
        const pedidoId = parseInt(event.target.dataset.pedidoId); // Obtenemos el ID del pedido desde el atributo data-pedido-id
        const pedidoIds = event.target.dataset.pedidoId.split(',').map(id => parseInt(id));
        const popupType = event.target.dataset.popupType; // Obtenemos el tipo de popup
        const popup = document.createElement('div');
        popup.className = 'popup-overlay';
        let pedidoData = this.tasks[pedidoId]; // Cambio a let
        let productoData = this.tasks[pedidoIds]; // Cambio a let
        const self = this; // Store a reference to the current instance


        if (popupType === 'producto') {
            let product, largo, ancho, alto;
        for (let i = 0; i < pedidoIds.length; i++) {
            productoData = this.tasks[pedidoIds[i]];
            if (productoData) {
                product = productoData[7];
                largo = productoData[19];
                ancho = productoData[18];
                alto = productoData[17];
                break;
                }
            }


            var html = '<div id="scroll">';
            html +='<table class="second-table" ><thead class="scroll-top"><tr>';

            html += '<tr>'
            html += '<th class="detalle-pedido-t" colspan="5" ></th>';
            html += '<th class="detalle-pedido-t" colspan="3" >Paquete</th>';
            html += '<th class="detalle-pedido-t" colspan="4" ></th>';
            html += '</tr>'
            html += '<th class="detalle-pedido-t">Op</th>';
            html += '<th class="detalle-pedido-t">item</th>';
            html += '<th class="detalle-pedido-t">ETA</th>';
            html += `<td class="detalle-pedido-t">Pqte. Solicitados</td>`;
            html += `<td class="detalle-pedido-t">Pqte. Saldo</td>`;
            html += '<th class="detalle-pedido-t">Alto <br> (cm)</th>';
            html += '<th class="detalle-pedido-t">Ancho<br> (cm)</th>';
            html += '<th class="detalle-pedido-t">Int</th>';
            html += '<th class="detalle-pedido-t">Tipo Empaque</th>';
            html += '<th class="detalle-pedido-t">Pzas</th>';
            html += '<th class="detalle-pedido-t">M3</th>';
            html += '<th class="detalle-pedido-t">Mbf</th>';

            html += '</tr></thead><tbody>';

            for (let i = 0; i < this.filteredTasks.length; i++) {
                var task = this.filteredTasks[i];

                for (let j = 0; j < pedidoIds.length; j++) {
                    if (i === pedidoIds[j]) {
                        const fechaISO = task[2];/*ETA*/
                        const fechaFormateada5 = new Date(fechaISO).toLocaleDateString('es-ES');/*ETA*/
                        html += '<tr>';
                        html += `<td class="detalle-pedido right-align">${task[0]}</td>`; // Op
                        html += `<td class="detalle-pedido right-align">${task[36]}</td>`; // Item
                        html += `<td class="detalle-pedido right-align">${fechaFormateada5}</td>`; // Fecha de Entrega
                        html += `<td class="detalle-pedido right-align">${task[45].toLocaleString()}</td>`; // Pqte
                        html += `<td class="detalle-pedido right-align"></td>`; // Pqte.saldo (lo que llevan hecho)
                        html += `<td class="detalle-pedido right-align">${task[47].toLocaleString()}</td>`; // Alto.Paquete
                        html += `<td class="detalle-pedido right-align">${task[58].toLocaleString()}</td>`; // Anc.paquete
                        html += `<td class="detalle-pedido right-align">${task[48].toLocaleString()}</td>`; // Int.paquete
                        html += `<td class="detalle-pedido right-align">${task[46]}</td>`; // Tipo Empaque
                        html += `<td class="detalle-pedido right-align">${task[55].toLocaleString()}</td>`; // Pzas
                        html += `<td class="detalle-pedido right-align">${task[20].toString().replace('.', ',')}</td>`; // M3
                        html += `<td class="detalle-pedido right-align">${task[51].toString().replace('.', ',')}</td>`; // Mbf

                        html += '</tr>';
                    }
                }
            }
            // Calcular los totales
            let totalPqteSolicitados = 0;
            let totalM3 = 0;
            let totalMbf = 0;
            let totalPiezas = 0;
            for (let j = 0; j < pedidoIds.length; j++) {
                let i = pedidoIds[j];
                let task = this.filteredTasks[i];
                totalPqteSolicitados += parseInt(task[45], 10); // Convierte a número
                totalM3 += parseFloat(task[20]); // Convierte a número de punto flotante
                totalMbf += parseFloat(task[51]); // Convierte a número de punto flotante
                totalPiezas += parseFloat(task[55]); // Convierte a número de punto flotante
                
            }


            // Cerrar la estructura de la tabla
            html += '</tbody>';

            html += '<tfoot class="scroll-bot">';
            html += '<tr>';
            html += '<th class="detalle-pedido-t">Total:</th>';
            html += '<th class="detalle-pedido-t"></th>';
            html += '<th class="detalle-pedido-t"></th>';
            html += `<th class="detalle-pedido-t">${totalPqteSolicitados.toLocaleString()}</th>`; // Pqte. Solicitados
            html += '<th class="detalle-pedido-t"></th>';
            html += '<th class="detalle-pedido-t"></th>';
            html += '<th class="detalle-pedido-t"></th>';
            html += '<th class="detalle-pedido-t"></th>';
            html += '<th class="detalle-pedido-t"></th>';
            html += `<th class="detalle-pedido-t">${totalPiezas.toLocaleString()}</th>`; // Pzas
            html += `<th class="detalle-pedido-t">${totalM3.toLocaleString().replace('.', ',')}</th>`; // M3
            html += `<th class="detalle-pedido-t">${totalMbf.toLocaleString().replace('.', ',')}</th>`; // Mbf
            html += '</tr>';
            html += '</tfoot></table></div>';




            // Set the innerHTML of the popup element
            popup.innerHTML = `
            <div class="popup-content" id="popup">
                <h2 style="margin-bottom: 2vh; text-align: center;">Plan de Producción ${product} - ${largo}-${ancho}-${alto} </h2>
                ${html} <!-- Inserta aquí la tabla generada -->
                <button style="float:right;" class="close-button">Cerrar</button>
            </div>
        `;
            // boton para el agregar folio
            //<button style="margin-top: 2vh; margin-left: 47%; background-color: red; color: white; width:6%; border: 1px solid white;" class="close-button abrir-folio-button">Agregar Folio</button>

        }
        else if (popupType === 'pedido') {
            productoData = this.tasks[pedidoId];

            var html = '<div id="scroll">';
            html +='<table class="second-table" ><thead class="scroll-top"><tr>';
            html += '<tr>'
            html += '<th class="detalle-pedido-t" colspan="6" ></th>';
            html += '<th class="detalle-pedido-t" colspan="3" >Facturacion</th>';
            html += '<th class="detalle-pedido-t" colspan="3" >Escuadrias</th>';
            html += '<th class="detalle-pedido-t" colspan="9" ></th>';
            html += '</tr>'
            html += '<th class="detalle-pedido-t">Item</th>';
            html += '<th class="detalle-pedido-t">Nombre producto</th>';
            html += '<th class="detalle-pedido-t">Est</th>';
            html += '<th class="detalle-pedido-t">term</th>';
            html += '<th class="detalle-pedido-t">Calidad</th>';
            html += '<th class="detalle-pedido-t" style="width:20vh;" >FSC</th>';
            html += '<th class="detalle-pedido-t a">Espesor <br> (cm)</th>';
            html += '<th class="detalle-pedido-t a">Ancho <br> (cm)</th>';
            html += '<th class="detalle-pedido-t a">Largo <br> (cm)</th>';
            html += '<th class="detalle-pedido-t a">Espesor  <br> (cm)</th>';
            html += '<th class="detalle-pedido-t a">Ancho  <br> (cm)</th>';
            html += '<th class="detalle-pedido-t a">Largo  <br> (cm)</th>';
            html += '<th class="detalle-pedido-t">Tipo Empaque</th>';
            html += '<th class="detalle-pedido-t">Alto Paquete <br> (cm)</th>';
            html += '<th class="detalle-pedido-t">Ancho Paquete <br> (cm)</th>';
            html += '<th class="detalle-pedido-t">Int.paquete</th>';
            html += '<th class="detalle-pedido-t">Pzas</th>';
            html += '<th class="detalle-pedido-t">Pqte</th>';
            html += '<th class="detalle-pedido-t">M3</th>';
            html += '<th class="detalle-pedido-t ">Mbf</th>';
            html += '<th class="detalle-pedido-t">Marca</th>';
            html += '</tr></thead><tbody>';

            // Iterate through the filtered tasks and products
            for (let i = 0; i < this.filteredTasks.length; i++) {
                var task = this.filteredTasks[i];
                if (task[0] === productoData[0]) {
                    for (let j = 0; j < task[7].length; j++) {
                        // Create a new row for each product
                        html += '<tr>';
                        html += `<td class="detalle-pedido right-align">${task[36]}</td>`; // Item
                        html += `<td class="detalle-pedido left-align" style="width:100vh;">${task[7]}</td>`; // Nombre producto
                        html += `<td class="detalle-pedido left-align">${task[59]}</td>`; // Est
                        html += `<td class="detalle-pedido left-align">${task[49]}</td>`; // term
                        html += `<td class="detalle-pedido left-align">${task[50]}</td>`; // Calidad
                        html += `<td class="detalle-pedido left-align">${task[41]}</td>`; // FSC
                        html += `<td class="detalle-pedido right-align ">${task[42].toLocaleString()}</td>`; // Esp.Fact
                        html += `<td class="detalle-pedido right-align">${task[43].toLocaleString()}</td>`; // Anc.Fact
                        html += `<td class="detalle-pedido right-align">${task[44].toLocaleString()}</td>`; // Lar.Fact
                        html += `<td class="detalle-pedido right-align">${task[17].toLocaleString()}</td>`; // alt.Producc
                        html += `<td class="detalle-pedido right-align">${task[18].toLocaleString()}</td>`; // Anc.Producc
                        html += `<td class="detalle-pedido right-align">${task[19].toLocaleString()}</td>`; // Lar.Producc
                        html += `<td class="detalle-pedido left-align">${task[46]}</td>`; // Tipo Empaque
                        html += `<td class="detalle-pedido right-align"  style="width:20vh;">${task[47]}</td>`; // Alto.Paquete
                        html += `<td class="detalle-pedido right-align"  style="width:20vh;">${task[58]}</td>`; // Anc.paquete
                        html += `<td class="detalle-pedido right-align"  style="width:20vh;">${task[48]}</td>`; // Int.paquete
                        html += `<td class="detalle-pedido right-align">${task[55].toLocaleString()}</td>`; // Pzas
                        html += `<td class="detalle-pedido right-align">${task[45].toLocaleString()}</td>`; // Pqte
                        html += `<td class="detalle-pedido right-align">${task[20].toString().replace('.', ',')}</td>`; // M3
                        html += `<td class="detalle-pedido right-align">${task[51].toString().replace('.', ',')}</td>`; // Mbf
                        html += `<td class="detalle-pedido left-align">${task[53]}</td>`; // Marca
                        html += '</tr>';
                    }
                }
            }
            // Calcular los totales
            let totalM3 = 0;
            let totalMbf = 0;
            let totalPiezas = 0;
            let totalPqtes = 0;
            for (let j = 0; j < pedidoIds.length; j++) {
                let i = pedidoIds[j];
                if (i < this.filteredTasks.length) {
                    let task = this.filteredTasks[i];
                    // Convert to number and add to totals
                    totalM3 += parseFloat(task[20]);
                    totalMbf += parseFloat(task[51]);
                    totalPqtes += parseFloat(task[45]);
                    totalPiezas += parseFloat(task[55]);
                }
            }
            
            // Cerrar la estructura de la tabla
            html += '</tbody>';

            html += '<tfoot class="scroll-bot">';
            html += '<tr>';
            html += '<th class="detalle-pedido-t">Total:</th>';
            html += '<th class="detalle-pedido-t"></th>';
            html += '<th class="detalle-pedido-t"></th>';
            html += '<th class="detalle-pedido-t"></th>';
            html += '<th class="detalle-pedido-t"></th>';
            html += '<th class="detalle-pedido-t"></th>';
            html += '<th class="detalle-pedido-t"></th>';
            html += '<th class="detalle-pedido-t"></th>';
            html += '<th class="detalle-pedido-t"></th>';
            html += '<th class="detalle-pedido-t"></th>';
            html += '<th class="detalle-pedido-t"></th>';
            html += '<th class="detalle-pedido-t"></th>';
            html += '<th class="detalle-pedido-t"></th>';
            html += '<th class="detalle-pedido-t"></th>';
            html += '<th class="detalle-pedido-t"></th>';
            html += '<th class="detalle-pedido-t"></th>';
            html += `<th class="detalle-pedido-t">${totalPiezas.toLocaleString()}</th>`; // Pzas
            html += `<th class="detalle-pedido-t">${totalPqtes.toLocaleString()}</th>`; // Pqte. Solicitados
            html += `<th class="detalle-pedido-t">${totalM3.toLocaleString().replace('.', ',')}</th>`; // M3
            html += `<th class="detalle-pedido-t">${totalMbf.toLocaleString().replace('.', ',')}</th>`; // Mbf
            html += '<th class="detalle-pedido-t"></th>';
            html += '</tr>';
            html += '</tfoot></table></div>';

            
            // Set the innerHTML of the popup element
            popup.innerHTML = `
                <div class="popup-content" id="popup">
                    <h2 style="margin-bottom: 2vh; text-align: center;">Detalles de Pedido ${productoData[0]}</h2>
                    ${html} <!-- Insert the generated table here -->
                    <button style="float:right;" class="close-button">Cerrar</button>
                </div>
            `;



        }
        document.body.appendChild(popup);

        // Add a click event listener to the close button
        const closeButton = popup.querySelector('.close-button');
        closeButton.addEventListener('click', () => {
            self.closePopup(popup);
        });
        $(document).on('click', '.abrir-folio-button', function () {
            // Puedes realizar cualquier acción adicional aquí, como enviar los datos al servidor.
            actualizarProductosSeleccionados();
            self.closePopup(popup);
            mostrarPopup3();
        });
    }

    closePopup(popup) {
        popup.style.display = 'none';
    }

}
// Declarar la variable fuera de la función
var productosSeleccionados = [];

$(document).on('change', '.producto-checkbox', function () {
    // Obtén el nombre del producto de la fila
    var pedidoId = $(this).closest('tr').data('pedido-id');
    if ($(this).prop('checked')) {
        // El checkbox se ha seleccionado, agrega el nombre del producto a la lista
        productosSeleccionados.push(pedidoId);
    } else {
        // El checkbox se ha deseleccionado, elimina el nombre del producto de la lista
        var index = productosSeleccionados.indexOf(pedidoId);
        if (index !== -1) {
            productosSeleccionados.splice(index, 1);
        }
    }
});
// Función para actualizar la lista de productos seleccionados en el popup
function actualizarProductosSeleccionados() {
    var listaProductos = productosSeleccionados.join(", "); // Convierte la lista en una cadena separada por comas
    $("#productos-seleccionados").text("Productos seleccionados: " + listaProductos);
}

// Evento clic en el botón Cerrar del popup
$(document).on('click', '#cerrar-popup-button', function () {
    ocultarPopup3();
});

// Evento clic en el botón Agregar Folio 
$(document).on('click', '.agregar-folio-button', function () {
    var textoIngresado = $("#texto-input").val();

    // Guardar el texto en una variable
    var textoGuardado = textoIngresado;



});


// Función para mostrar el popup y el fondo semitransparente
function mostrarPopup3() {
    $("#popup3").show();
}

// Función para ocultar el popup y el fondo semitransparente
function ocultarPopup3() {
    $("#popup3").hide();

}


const toggleLineasButton = document.getElementById('toggle-lineas-button');
toggleLineasButton.addEventListener('change', function () {
    const selectedLine = this.value;
    gantt.filterTasksByLine(selectedLine);
});

function toggleCargaForm() {
    const cargaForm = document.getElementById('carga-form');
    if (cargaForm.style.display === 'none') {
        cargaForm.style.display = 'block';
    } else {
        cargaForm.style.display = 'none';
    }
}

function showPopup() {
    const popupOverlay = document.getElementById('popup-ejecutar');
    popupOverlay.style.display = 'block';
}

function hidePopup() {
    /* const popupOverlay = document.getElementById('popup-ejecutar');
    popupOverlay.style.display = 'none'; */
    window.location.href = '/pantalla-carga/';
}

//Popup para importar
function showPopupimport() {
    const popupOverlay = document.getElementById('popupContainer');
    popupOverlay.style.display = 'block';
}

function closePopupimport() {
    const popupOverlay = document.getElementById('popupContainer');
    popupOverlay.style.display = 'none';
}
//Popup para Actualizar materia prima
function showPopupmateria() {
    const popupOverlay = document.getElementById('popupContainermateria');
    if (popupContainermateria.style.display === 'none') {
        popupContainermateria.style.display = 'block';
    } else {
        popupContainermateria.style.display = 'none';
    }
}

function closePopupmateria() {
    var popup = document.getElementById("popupContainermateria");
    popup.style.display = "none";
}
//Popup para Actualizar stock producto terminado
function showPopupproduccion() {
    const popupOverlay = document.getElementById('popupContainerproduccion');
    if (popupContainerproduccion.style.display === 'none') {
        popupContainerproduccion.style.display = 'block';
    } else {
        popupContainerproduccion.style.display = 'none';
    }
}

function closePopupproduccion() {
    var popup = document.getElementById("popupContainerproduccion");
    popup.style.display = "none";
}
// Función para cerrar el popup
function closePopup() {
    var popup = document.getElementById("carga-form");
    popup.style.display = "none";
}


document.addEventListener('click', function (event) {
    if (event.target && event.target.classList.contains('popup-link')) {
        // Obtener el valor de 'i' desde el atributo de datos personalizado
        const iValue = event.target.getAttribute('data-i');

    }
});

function calcularDiasRestantes(fechaFinalizacion) {
    // Obtén la fecha actual
    const fechaActual = new Date();

    // Convierte la fecha de finalización del pedido a un objeto de fecha
    const fechaFinalizacionPedido = new Date(fechaFinalizacion);

    // Calcula la diferencia en milisegundos entre las dos fechas
    const diferenciaEnMs = fechaFinalizacionPedido - fechaActual;

    // Convierte la diferencia de milisegundos a días
    const diasRestantes = Math.ceil(diferenciaEnMs / (1000 * 60 * 60 * 24));

    // Retorna la cantidad de días restantes
    return diasRestantes;
}