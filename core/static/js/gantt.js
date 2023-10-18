
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



    PlanTable() {
        var html = '<table class="event-table second-table"><thead><tr>';

        // Agregar dos columnas adicionales a la izquierda
        html += '<th style="color: white; width: 30vh; font-size: 15px; text-align: center; height:3vh;">Producto</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Largo <br> (cm)</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Ancho <br> (cm)</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Alto <br> (cm)</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Pqtes.Solicitados</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">IDS</th>';
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
        for (let i = 0; i < this.filteredTasks.length; i++ ) {
            var task = this.filteredTasks[i];
        
            for (let j = 0; j < task[7].length; j++) {
                var product = task[7][j]; // Obtener el nombre del producto
                var key = `${product}_${task[19]}_${task[18]}_${task[17]}`; // Crear una clave única para agrupar
                console.log("task después del bucle:", i);
            
                if (!groupedRows[key]) {
                    groupedRows[key] = {
                        product: product,
                        largo: task[19],
                        ancho: task[18],
                        alto: task[17],
                        cantidad: 0,
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

                groupedRows[key].cantidad += parseInt(task[45], 10); // Convierte la cantidad en número y suma
                groupedRows[key].detalles.push({
                    color: task[15],
                    randomNumbers: randomNumbers,
                    i: i,
                });

                groupedRows[key].ids.push(i);
            }
        }


        

        // Ahora, puedes iterar sobre las filas agrupadas y construir la tabla final
        for (let key in groupedRows) {
            let row = groupedRows[key];
            const ids = row.ids.join(', ');
            var dateDiff = this.diffInDays(row.fechaFin, row.fechaInicio);
            dateDiff = Math.min(dateDiff, 11);
            console.log("dateDiff:", dateDiff);
            

        
            bodyHtml += '<tr>';
            bodyHtml += `<td>${row.product}</td>`;
            bodyHtml += `<td class="right-align">${row.largo.toLocaleString()}</td>`;
            bodyHtml += `<td class="right-align">${row.ancho.toLocaleString()}</td>`;
            bodyHtml += `<td class="right-align">${row.alto.toLocaleString()}</td>`;
            bodyHtml += `<td class="right-align">${row.cantidad}</td>`; // Muestra la cantidad acumulada como número
            bodyHtml += `<td class="right-align">${ids}</td>`; // Muestra los valores de i
            bodyHtml += `<td class="left-align"><a class="popup-link" data-popup-type="producto" data-pedido-id="${ids}">Ver detalles</a></td>`;
            let paquetesPorDia = new Array(dateDiff).fill(0);

            
            // Distribuir los paquetes en los días
            for (let i = 0; i < row.detalles.length; i++) {
                let detalle = row.detalles[i];
                for (let l = 0; l < detalle.randomNumbers.length; l++) {
                    let diaAleatorio = Math.floor(Math.random() * dateDiff);
                    paquetesPorDia[diaAleatorio] += detalle.randomNumbers[l];
                }
            }
        
            // Agregar las celdas para los paquetes solicitados por día
            for (let k = 0; k < paquetesPorDia.length; k++) {

                bodyHtml += '<td class="event-cell';
            
                if (paquetesPorDia[k] > 0) {
                    bodyHtml += ' has-paquetes';
        
                }
            
                bodyHtml += '">';
                
                if (paquetesPorDia[k] > 0) {
                    bodyHtml += `<a>Pqtes. solicitados: ${paquetesPorDia[k]}</a>`;
                }
                
                bodyHtml += '</td>';
            }
            
            bodyHtml += '</tr>';
            
        }
        
        // Agrega el cuerpo de la tabla al encabezado
        html += bodyHtml;
        
        html += '</tbody></table>';
        return html;}
        


    PedidoTable() {
        var html = '<table id="miTabla" style="margin-left: auto; margin-right: auto;" class="second-table"><thead><tr>';

        // Agregar dos columnas adicionales a la izquierda
        html += '<th style="color: white; width: 20vh; font-size: 15px; text-align: center; height:3vh;">Fecha carga</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">OP</th>';
        html += '<th style="color: white; width: 50vh; font-size: 15px; text-align: center; height:3vh;">Cliente</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Mercado</th>';
        html += '<th style="color: white; width: 10vh; font-size: 15px; text-align: center; height:3vh;">Fecha Creacion</th>';
        html += '<th style="color: white; width: 10vh; font-size: 15px; text-align: center; height:3vh;">ETA</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Destino</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Programa</th>';
        html += '<th style="color: white; width: 20vh; font-size: 15px; text-align: center; height:3vh;">Detalle</th>';



        html += '</tr></thead><tbody>';

        // Utiliza una variable diferente para el cuerpo de la tabla
        var bodyHtml = '';

    // Maintain a list of unique orden_pedido values
        var uniqueOrdenPedido = [];

        // Itera sobre cada producto y crea una fila por producto
        for (let i = 0; i < this.filteredTasks.length; i++) {
            var task = this.filteredTasks[i];

            
            // Check if orden_pedido already exists in the uniqueOrdenPedido list
            if (!uniqueOrdenPedido.includes(task[0])) {

                const fechaISO = task[1];/*Fecha de carga*/
                const fechaISO2 = task[2];/*ETA*/
                const fechaISO3 = task[3];/*Fecha Creacion*/
                const fechaFormateada = new Date(fechaISO).toLocaleDateString('es-ES');/*Fecha de carga*/
                const fechaFormateada2 = new Date(fechaISO2).toLocaleDateString('es-ES');/*ETA*/
                const fechaFormateada3 = new Date(fechaISO3).toLocaleDateString('es-ES');/*Fecha Creacion*/

                bodyHtml += `<td style="text-align: center;">${fechaFormateada}</td>`; /*Fecha de carga*/
                bodyHtml += `<td class="right-align">${task[0]}</td>`;/*OP Orden Interna*/
                bodyHtml += `<td class="left-align">${task[5]}</td>`; /*Cliente*/
                bodyHtml += `<td class="left-align">${task[38]}</td>`; /*Mercado*/
                bodyHtml += `<td style="text-align: center;">${fechaFormateada3}</td>`; /*Fecha Creacion*/
                bodyHtml += `<td style="text-align: center;">${fechaFormateada2}</td>`; /*ETA*/
                bodyHtml += `<td class="left-align">${task[39]}</td>`; /*Destino*/
                bodyHtml += `<td class="left-align">${task[54]}</td>`; /*Programa*/
                bodyHtml += `<td  style="text-align: center;"><a class="popup-link" data-pedido-id="${i}" data-popup-type="pedido">Ver...</a></td>`; /*Detalle*/

                bodyHtml += '</tr>';
                
                // Add the orden_pedido to the uniqueOrdenPedido list
                uniqueOrdenPedido.push(task[0]);
            }
        }

        // Agrega el cuerpo de la tabla al encabezado
        html += bodyHtml;

        html += '</tbody></table>';
        
        return html;
    }

    ProductosTable() {
        var html = '<table style="margin-left: auto; margin-right: auto;"class="second-table"><thead><tr>';



        // Agregar dos columnas adicionales a la izquierda


        html += '<th style="color: white; width: 30vh; font-size: 15px; text-align: center; height:3vh;">Producto</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Largo <br> (cm)</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Ancho <br> (cm)</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Alto <br> (cm)</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Pqtes Solicitados</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">M3</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">ETA</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Detalle</th>';

        html += '</tr></thead><tbody>';

        // Utiliza una variable diferente para el cuerpo de la tabla
        var bodyHtml = '';

        // Itera sobre cada producto y crea una fila por producto
        for (let i = 0; i < this.filteredTasks.length; i++) {
            var task = this.filteredTasks[i];
            for (let j = 0; j < task[7].length; j++) { // Itera sobre la lista de productos en task[11]
                var product = task[7][j]; // Obtiene el nombre del producto
                const fechaISO = task[2];/*ETA*/
                const fechaFormateada4 = new Date(fechaISO).toLocaleDateString('es-ES');/*ETA*/
                bodyHtml += `<td class="left-align">${task[7]}</td>`;/*Nombre del Producto*/
                bodyHtml += `<td class="right-align">${task[19].toLocaleString()}</td>`;/*Largo*/
                bodyHtml += `<td class="right-align">${task[18].toLocaleString()}</td>`;/*Ancho*/
                bodyHtml += `<td class="right-align">${task[17].toLocaleString()}</td>`;/*Alto*/
                bodyHtml += `<td class="right-align">${task[45].toLocaleString()}</td>`;/*pqtes solicitados*/
                bodyHtml += `<td class="right-align">${task[20]}</td>`;/*M3*/
                bodyHtml += `<td style="text-align: center;">${fechaFormateada4}</td>`;/*ETA*/
                bodyHtml += `<td  style="text-align: center;"><a class="popup-link" data-pedido-id="${i}" data-popup-type="producto">Ver...</a></td>`;/*Detalle*/


            }

                bodyHtml += '</tr>';
            
        }
     
        // Agrega el cuerpo de la tabla al encabezado
        html += bodyHtml;
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
        console.log('Attaching event listeners');
        const popupLinks = document.querySelectorAll('.popup-link');
        console.log('Popup links found:', popupLinks.length);

        const self = this; // Store a reference to the current instance

        document.getElementById('gantt').addEventListener('click', function (event) {
            const target = event.target;
            if (target.classList.contains('popup-link')) {
                self.handlePopupClick(event);
            }
        });
    }


    handlePopupClick(event) {
        console.log('Popup link clicked');
        event.stopPropagation();// Evita que el evento se propague al contenedor principal
        const pedidoId = parseInt(event.target.dataset.pedidoId); // Obtenemos el ID del pedido desde el atributo data-pedido-id
        const pedidoIds = event.target.dataset.pedidoId.split(',').map(id => parseInt(id));
        const popupType = event.target.dataset.popupType; // Obtenemos el tipo de popup
        const popup = document.createElement('div');
        popup.className = 'popup-overlay';
        console.log('Pedido ID:', pedidoId);
        console.log('Pedido IDs:', pedidoIds);
        let pedidoData = this.tasks[pedidoId]; // Cambio a let
        let productoData = this.tasks[pedidoIds]; // Cambio a let
        const self = this; // Store a reference to the current instance

        
        if (popupType === 'producto') {
            productoData = this.tasks[pedidoIds];
        
            var html = '<table class="second-table"><thead><tr>';
            //html += '<th class="detalle-pedido-t">Folio</th>';
            html += '<th class="detalle-pedido-t">Op</th>';
            html += '<th class="detalle-pedido-t">item</th>';
            html += '<th class="detalle-pedido-t">Producto</th>';
            html += '<th class="detalle-pedido-t">Alto <br> (cm)</th>';
            html += '<th class="detalle-pedido-t">Ancho <br> (cm)</th>';
            html += '<th class="detalle-pedido-t">Largo <br> (cm)</th>';
            html += `<td class="detalle-pedido-t">Pqte. Solicitados</td>`;
            html += '<th class="detalle-pedido-t">Alto Paquete <br> (cm)</th>';
            html += '<th class="detalle-pedido-t">Ancho Paquete <br> (cm)</th>';
            html += '<th class="detalle-pedido-t">Int.paquete</th>';
            html += '<th class="detalle-pedido-t">Tipo Empaque</th>';
            html += '<th class="detalle-pedido-t">Pzas</th>';
            html += '<th class="detalle-pedido-t">M3</th>';
            html += '<th class="detalle-pedido-t">Mbf</th>';

            html += '</tr></thead><tbody>';
        
            for (let i = 0; i < this.filteredTasks.length; i++) {
                var task = this.filteredTasks[i];
                
                if (task[0] === productoData[0]) { 
                    for (let j = 0; j < task[7].length; j++) {
                        console.log(task[7]);
        
                        html += '<tr>';
                        html += `<tr data-pedido-id="${task[69]}">`; // Asegúrate de establecer el atributo data-producto-nombre aquí
                        // html += '<td class="detalle-pedido"><input type="checkbox" class="producto-checkbox"></td>'; // selecion de folio
                        html += `<td class="detalle-pedido right-align">${task[0]}</td>`; // Op
                        html += `<td class="detalle-pedido right-align">${task[36]}</td>`; // Item
                        html += `<td class="detalle-pedido left-align">${task[7]}</td>`; // Nombre producto
                        html += `<td class="detalle-pedido right-align">${task[17].toLocaleString()}</td>`; // alt.Producc
                        html += `<td class="detalle-pedido right-align">${task[18].toLocaleString()}</td>`; // Anc.Producc
                        html += `<td class="detalle-pedido right-align">${task[19].toLocaleString()}</td>`; // Lar.Producc
                        html += `<td class="detalle-pedido right-align">${task[45].toLocaleString()}</td>`; // Pqte
                        html += `<td class="detalle-pedido right-align">${task[47].toLocaleString()}</td>`; // Alto.Paquete
                        html += `<td class="detalle-pedido right-align">${task[58].toLocaleString()}</td>`; // Anc.paquete
                        html += `<td class="detalle-pedido right-align">${task[48].toLocaleString()}</td>`; // Int.paquete
                        html += `<td class="detalle-pedido right-align">${task[46]}</td>`; // Tipo Empaque
                        html += `<td class="detalle-pedido right-align">${task[55].toLocaleString()}</td>`; // Pzas
                        html += `<td class="detalle-pedido right-align">${task[20]}</td>`; // M3
                        html += `<td class="detalle-pedido right-align">${task[51]}</td>`; // Mbf
        
                        html += '</tr>';
                    }
                }
            }
        
            // Close the table structure
            html += '</tbody></table>';
        
            // Set the innerHTML of the popup element
            popup.innerHTML = `
                <div class="popup-content" id="popup">
                    <h2 style="margin-bottom: 2vh; text-align: center;">Detalles de Producto </h2>
                    ${html} <!-- Insert the generated table here -->
                    <button style="margin-top: 2vh; float:right; background-color: red; color: white; width:6%; border: 1px solid white;" class="close-button">Cerrar</button>
                </div>
            `;
             // boton para el agregar folio
            //<button style="margin-top: 2vh; margin-left: 47%; background-color: red; color: white; width:6%; border: 1px solid white;" class="close-button abrir-folio-button">Agregar Folio</button>
            
        }else if (popupType === 'pedido') {
            productoData = this.tasks[pedidoId];
        
            var html = '<table class="second-table"><thead><tr>';
     
            html += '<th class="detalle-pedido-t">Item</th>';
            html += '<th class="detalle-pedido-t">Nombre producto</th>';
            html += '<th class="detalle-pedido-t">Est</th>';
            html += '<th class="detalle-pedido-t">term</th>';
            html += '<th class="detalle-pedido-t">Calidad</th>';
            html += '<th class="detalle-pedido-t" style="width:20vh;" >FSC</th>';
            html += '<th class="detalle-pedido-t a">Esp.Fact <br> (cm)</th>';
            html += '<th class="detalle-pedido-t a">Anc.Fact <br> (cm)</th>';
            html += '<th class="detalle-pedido-t a">Lar.Fact <br> (cm)</th>';
            html += '<th class="detalle-pedido-t a">Esp. Producc <br> (cm)</th>';
            html += '<th class="detalle-pedido-t a">Anc. Producc <br> (cm)</th>';
            html += '<th class="detalle-pedido-t a">Lar. Producc <br> (cm)</th>';
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
                        console.log(task[7]);
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
                        html += `<td class="detalle-pedido right-align">${task[20]}</td>`; // M3
                        html += `<td class="detalle-pedido right-align">${task[51]}</td>`; // Mbf
                        html += `<td class="detalle-pedido left-align">${task[53]}</td>`; // Marca
                        html += '</tr>';
                    }
            }}
            
            // Close the table structure
            html += '</tbody></table>';
      
        
            // Set the innerHTML of the popup element
            popup.innerHTML = `
                <div class="popup-content" id="popup">
                    <h2 style="margin-bottom: 2vh; text-align: center;">Detalles de Pedido ${productoData[0]}</h2>
                    ${html} <!-- Insert the generated table here -->
                    <button style="margin-top: 2vh; float:right; background-color: red; color: white; width:6%; border: 1px solid white;" class="close-button">Cerrar</button>
                </div>
            `;

        
        
        }
        else if (popupType === 'patron') {
        productoData = this.tasks[pedidoId];
        popup.innerHTML = `
            <div class="popup-content" id="popup">
                <h2>Detalles</h2>
                <div class="popup-item">
                    <strong>Codigo pedido:</strong> <span>${productoData[0]}</span>
                </div>
                <div class="popup-item">
                    <strong>Diametro:</strong> <span>${productoData[35]}</span>
                </div>
                <div class="popup-item">
                    <strong>Largo trozo:</strong> <span>${productoData[24]}</span>
                </div>
                <div class="popup-item">
                    <strong>Codigo patrón:</strong> <span>${productoData[36]}</span>
                </div>
                <div class="popup-item">
                    <strong>Nombre patrón:</strong> <span>${productoData[37]}</span>
                </div>
                <div class="popup-item">
                    <strong>Descripción patrón:</strong> <span>${productoData[38]}</span>
                </div>
                <div class="popup-item">
                    <strong>Rendimiento patrón:</strong> <span>${productoData[39]}</span>
                </div>
                <div class="popup-item">
                    <strong>Velocidad línea patrón:</strong> <span>${productoData[40]}</span>
                </div>
                <div class="popup-item">
                    <strong>Setup time patrón:</strong> <span>${productoData[41]}</span>
                </div>
                <div class="popup-item">
                    <strong>Lead time patrón:</strong> <span>${productoData[42]}</span>
                </div>
                <div class="popup-item">
                    <strong>Utilizado patrón:</strong> <span>${productoData[43]}</span>
                </div>
                <div class="popup-item">
                    <strong>Producto asociado patrón:</strong> <span>${productoData[44]}</span>
                </div>
                <button class="close-button" >Cerrar</button>
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
    // Hacer algo con la variable textoGuardado, por ejemplo, imprimirlo en la consola
    console.log("Texto guardado:", textoGuardado);
    // Puedes realizar cualquier acción adicional aquí, como enviar los datos al servidor.


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
        console.log('Valor de i:', iValue);

        // Obtener todos los valores de 'i' almacenados en el array 'iValues' y mostrarlos
        console.log('Valores de i almacenados:', iValues);
    }
});