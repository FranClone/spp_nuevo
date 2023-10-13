
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
        var html = '<table class="second-table"><thead><tr>';

        // Agregar dos columnas adicionales a la izquierda
        html += '<th style="color: white; width: 30vh; font-size: 15px; text-align: center; height:3vh;">Producto</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Largo <br> (cm)</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Ancho <br> (cm)</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">Alto <br> (cm)</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center; height:3vh;">M3</th>';



        // Copiar el encabezado de la primera tabla
        const selectedPeriod = document.querySelector('select[name="periodos"]').value;
        const isDiarioSelected = selectedPeriod === "diario";
        const isSemanalSelected = selectedPeriod === "semanal";
        const isMensualSelected = selectedPeriod === "mensual";

        if (isDiarioSelected) {
            var diffDays = this.diffInDays(this.maxDate, this.minDate) + 1;
            const actual = new Date(this.minDate);

            for (let i = 0; i < diffDays; i++) {
                html += '<th style="color: white; width: 70vh; font-size: 13px;">' + this.formatDate(actual, "diario") + '</th>';
                actual.setDate(actual.getDate() + 1);
            }
        } else if (isSemanalSelected) {
            var diffWeeks = this.diffInWeeks(this.maxDate, this.minDate) + 1;
            const actual = new Date(this.minDate);

            for (let i = 0; i < diffWeeks; i++) {
                const startOfWeek = new Date(actual);
                const endOfWeek = new Date(actual);
                endOfWeek.setDate(startOfWeek.getDate() + 6);

                html += '<th>' + this.formatDate(startOfWeek, "semanal", endOfWeek) + '</th>';
                actual.setDate(startOfWeek.getDate() + 7);
            }
        } else if (isMensualSelected) {
            var diffMonths = this.diffInMonths(this.maxDate, this.minDate) + 1;
            const actual = new Date(this.minDate);

            for (let i = 0; i < diffMonths; i++) {
                actual.setMonth(actual.getMonth() + 1);
                html += '<th>' + this.formatDate(actual, "mensual") + '</th>';
            }
        }

        html += '</tr></thead><tbody>';

        // Utiliza una variable diferente para el cuerpo de la tabla
        var bodyHtml = '';

        // Itera sobre cada producto y crea una fila por producto
        for (let i = 0; i < this.filteredTasks.length; i++) {
            var task = this.filteredTasks[i];

            for (let j = 0; j < task[7].length; j++) { // Itera sobre la lista de productos en task[11]
                var product = task[7][j]; // Obtiene el nombre del producto
                var dMin = new Date(task[3]);
                var dMax = new Date(task[2]);

                // Calcular la diferencia en días entre dMin y dMax
                var dateDiff = this.diffInDays(dMax, dMin);

                var daysBefore = this.diffInDays(this.minDate, dMin);
                var daysAfter = this.diffInDays(dMax, this.maxDate);

                // Ensure that daysBefore is at least 0 (minimum start date constraint)
                daysBefore = Math.max(daysBefore, 0);

                // Ensure that daysAfter is at least 0 (maximum end date constraint)
                daysAfter = Math.max(daysAfter, 0);

                console.log('Fecha de inicio (dMin):', dMin);
                console.log('Fecha de finalización (dMax):', dMax);

                bodyHtml += '<tr>';


                bodyHtml += `<td>${product}</td>`;/*Nombre del Producto*/
                bodyHtml += `<td class="right-align">${task[24].toLocaleString()}</td>`;/*Largo*/
                bodyHtml += `<td class="right-align">${task[23].toLocaleString()}</td>`;/*Ancho*/
                bodyHtml += `<td class="right-align">${task[22].toLocaleString()}</td>`;/*Alto*/
                bodyHtml += `<td class="right-align">${task[25]}</td>`;/*M3*/


                for (let k = 0; k < daysBefore; k++) {
                    bodyHtml += '<td ></td>';
                }

                bodyHtml += `<td class="event-cell" colspan="${dateDiff}" style="background-color: ${task[15]}; border: 1px solid #000;">
                    <a class="popup-link" data-pedido-id="${j}" data-popup-type="producto">Pqtes.solicitados ${task[54]}</a>
                </td>`;

                for (let k = 0; k < daysAfter; k++) {
                    bodyHtml += '<td></td>';
                }

                bodyHtml += '</tr>';
                
            }
        }

        // Agrega el cuerpo de la tabla al encabezado
        html += bodyHtml;

        html += '</tbody></table>';
        return html;
    }

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
                const fechaFormateada2 = new Date(fechaISO).toLocaleDateString('es-ES');/*ETA*/
                const fechaFormateada3 = new Date(fechaISO).toLocaleDateString('es-ES');/*Fecha Creacion*/

                bodyHtml += `<td style="text-align: center;">${fechaFormateada}</td>`; /*Fecha de carga*/
                bodyHtml += `<td class="right-align">${task[0]}</td>`;/*OP Orden Interna*/
                bodyHtml += `<td class="left-align">${task[5]}</td>`; /*Cliente*/
                bodyHtml += `<td class="left-align">${task[47]}</td>`; /*Mercado*/
                bodyHtml += `<td style="text-align: center;">${fechaFormateada3}</td>`; /*Fecha Creacion*/
                bodyHtml += `<td style="text-align: center;">${fechaFormateada2}</td>`; /*ETA*/
                bodyHtml += `<td class="left-align">${task[48]}</td>`; /*Destino*/
                bodyHtml += `<td class="left-align">${task[63]}</td>`; /*Programa*/
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
                bodyHtml += `<td class="right-align">${task[24].toLocaleString()}</td>`;/*Largo*/
                bodyHtml += `<td class="right-align">${task[23].toLocaleString()}</td>`;/*Ancho*/
                bodyHtml += `<td class="right-align">${task[22].toLocaleString()}</td>`;/*Alto*/
                bodyHtml += `<td class="right-align">${task[54].toLocaleString()}</td>`;/*pqtes solicitados*/
                bodyHtml += `<td class="right-align">${task[25]}</td>`;/*M3*/
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
        const productoId = event.target.dataset.productoId;
        const popupType = event.target.dataset.popupType; // Obtenemos el tipo de popup
        const popup = document.createElement('div');
        popup.className = 'popup-overlay';
        console.log('Pedido ID:', pedidoId);
        let pedidoData = this.tasks[pedidoId]; // Cambio a let
        let productoData = this.tasks[productoId]; // Cambio a let
        const self = this; // Store a reference to the current instance

        
        if (popupType === 'producto') {
            productoData = this.tasks[pedidoId];
        
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
                        html += `<td class="detalle-pedido right-align">${task[45]}</td>`; // Item
                        html += `<td class="detalle-pedido left-align">${task[7]}</td>`; // Nombre producto
                        html += `<td class="detalle-pedido right-align">${task[22].toLocaleString()}</td>`; // alt.Producc
                        html += `<td class="detalle-pedido right-align">${task[23].toLocaleString()}</td>`; // Anc.Producc
                        html += `<td class="detalle-pedido right-align">${task[24].toLocaleString()}</td>`; // Lar.Producc
                        html += `<td class="detalle-pedido right-align">${task[54].toLocaleString()}</td>`; // Pqte
                        html += `<td class="detalle-pedido right-align">${task[56].toLocaleString()}</td>`; // Alto.Paquete
                        html += `<td class="detalle-pedido right-align">${task[67].toLocaleString()}</td>`; // Anc.paquete
                        html += `<td class="detalle-pedido right-align">${task[57].toLocaleString()}</td>`; // Int.paquete
                        html += `<td class="detalle-pedido right-align">${task[55]}</td>`; // Tipo Empaque
                        html += `<td class="detalle-pedido right-align">${task[64].toLocaleString()}</td>`; // Pzas
                        html += `<td class="detalle-pedido right-align">${task[25]}</td>`; // M3
                        html += `<td class="detalle-pedido right-align">${task[60]}</td>`; // Mbf
        
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
                        html += `<td class="detalle-pedido right-align">${task[45]}</td>`; // Item
                        html += `<td class="detalle-pedido left-align" style="width:100vh;">${task[7]}</td>`; // Nombre producto
                        html += `<td class="detalle-pedido left-align">${task[68]}</td>`; // Est
                        html += `<td class="detalle-pedido left-align">${task[58]}</td>`; // term
                        html += `<td class="detalle-pedido left-align">${task[59]}</td>`; // Calidad
                        html += `<td class="detalle-pedido left-align">${task[50]}</td>`; // FSC
                        html += `<td class="detalle-pedido right-align ">${task[51].toLocaleString()}</td>`; // Esp.Fact
                        html += `<td class="detalle-pedido right-align">${task[52].toLocaleString()}</td>`; // Anc.Fact
                        html += `<td class="detalle-pedido right-align">${task[53].toLocaleString()}</td>`; // Lar.Fact
                        html += `<td class="detalle-pedido right-align">${task[22].toLocaleString()}</td>`; // alt.Producc
                        html += `<td class="detalle-pedido right-align">${task[23].toLocaleString()}</td>`; // Anc.Producc
                        html += `<td class="detalle-pedido right-align">${task[24].toLocaleString()}</td>`; // Lar.Producc
                        html += `<td class="detalle-pedido left-align">${task[55]}</td>`; // Tipo Empaque
                        html += `<td class="detalle-pedido right-align"  style="width:20vh;">${task[56]}</td>`; // Alto.Paquete
                        html += `<td class="detalle-pedido right-align"  style="width:20vh;">${task[67]}</td>`; // Anc.paquete
                        html += `<td class="detalle-pedido right-align"  style="width:20vh;">${task[57]}</td>`; // Int.paquete
                        html += `<td class="detalle-pedido right-align">${task[64].toLocaleString()}</td>`; // Pzas
                        html += `<td class="detalle-pedido right-align">${task[54].toLocaleString()}</td>`; // Pqte
                        html += `<td class="detalle-pedido right-align">${task[25]}</td>`; // M3
                        html += `<td class="detalle-pedido right-align">${task[60]}</td>`; // Mbf
                        html += `<td class="detalle-pedido left-align">${task[62]}</td>`; // Marca
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