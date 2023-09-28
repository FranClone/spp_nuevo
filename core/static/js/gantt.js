
class Gantt {
    constructor(tasks) {
        this.tasks = tasks;
        this.dateWidth = 178;
        this.filteredTasks = tasks;
        this.setMinAndMaxDate();
        document.getElementById('gantt').innerHTML = this.buildTableHeader() + this.buildTableBody();
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
    //Tabla carta gantt
    buildTableHeader() {
        var html = '<table ><thead  style="position: sticky; top: 0; background-color: white; z-index: 1;width: 400px;"><tr>';

            // Agrega las nuevas columnas aquí
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Fecha carga</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Nro Pedido</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Cliente</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Fecha Creación</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">ETA</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Linea</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Detalle</th>';

        const selectedPeriod = document.querySelector('select[name="periodos"]').value;
        const isDiarioSelected = selectedPeriod === "diario";
        const isSemanalSelected = selectedPeriod === "semanal";
        const isMensualSelected = selectedPeriod === "mensual";
        //Encabezado
        if (isDiarioSelected) {
            var diffDays = this.diffInDays(this.maxDate, this.minDate) + 1;
            const actual = new Date(this.minDate);

            for (let i = 0; i < diffDays; i++) {
                html += '<th style="color: white; width: 80vh; ">' + this.formatDate(actual, "diario") + '</th>';
                actual.setDate(actual.getDate() + 1); // Avanza un día
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

        html += '</tr></thead><tbody">';
        return html;
    }



    buildTableBody() {
        var html = '';
    
        for (let i = 0; i < this.filteredTasks.length; i++) {
            var task = this.filteredTasks[i];
    
            var dMin = new Date(task[3]);
            var dMax = new Date(task[2]);

                    // Agregar dos columnas adicionales a la izquierda

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
    
            html += '<tr>';
    
            for (let j = 0; j < daysBefore; j++) {
                html += '<td></td>';
            }
    
            html += `<td class="event-cell" colspan="${dateDiff}" style="background-color: ${task[15]}; border: 1px solid #000;">
                <span>${task[4]}%</span>
                <a class="popup-link" data-pedido-id="${i}" data-popup-type="pedido"${i}">${task[0]}</a>
            </td>`;
    
            for (let j = 0; j < daysAfter; j++) {
                html += '<td></td>';
            }
    
            html += '</tr>';

        }
        return html;
    }



    buildSecondTable() {
        var html = '<table class="second-table"><thead><tr>';

        // Agregar dos columnas adicionales a la izquierda
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Linea Produccion</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Cliente</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Productos</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Escuadrias</th>';

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

            for (let j = 0; j < task[9].length; j++) { // Itera sobre la lista de productos en task[11]
                var product = task[9][j]; // Obtiene el nombre del producto
                var largo = task[10][j];
                var ancho = task[11][j];
                var alto = task[12][j];
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

                // Agregar el valor de task[7] en la primera columna
                bodyHtml += `<td></td>`;

                // Agregar el valor de task[7] en la primera columna
                bodyHtml += `<td>${task[5]}</td>`;

                // Agregar el nombre del producto en la segunda columna
                bodyHtml += `<td>${product}</td>`;


                bodyHtml += `<td>L:${largo} A:${ancho} Al:${alto}</td>`;


                for (let k = 0; k < daysBefore; k++) {
                    bodyHtml += '<td ></td>';
                }

                bodyHtml += `<td class="event-cell" colspan="${dateDiff}" style="background-color: ${task[14]}; border: 1px solid #000;">
                    <span>${task[4]}%</span>
                    <a class="popup-link" data-pedido-id="${i}" data-popup-type="producto">U ${task[7]}</a>
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

    SalidaTable() {
        var html = '<table class="second-table"><thead><tr>';

        // Agregar dos columnas adicionales a la izquierda
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Linea Produccion</th>';/**/
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Cliente</th>';/**/
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Item</th>'; /**/
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Folio</th>'; /**/
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Cliente</th>'; /**/
        html += '<th style="color: white; width: 30vh; font-size: 13px;">OP</th>'; /**/
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Mercado</th>'; /**/
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Productos</th>';/**/
        html += '<th style="color: white; width: 30vh; font-size: 13px;">ETA</th>';/**/
        html += '<th style="color: white; width: 30vh; font-size: 13px;">L/A/AL</th>';/**/
        html += '<th style="color: white; width: 30vh; font-size: 13px;">PQTES.Solicitados</th>';/**/
        html += '<th style="color: white; width: 30vh; font-size: 13px;">PQTES.Saldo</th>';/**/
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Trozos</th>';/**/
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Ø</th>';/**/
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Largo Trozos</th>';/**/
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Grado de Urgencia</th>';/**/
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Lateral</th>';/*por determinar*/
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Nota</th>';/**/
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Cant.desep.de 20MM</th>';/**/
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Largo del Taco</th>';/**/
        html += '<th style="color: white; width: 30vh; font-size: 13px;">OBS</th>';/**/
        html += '<th style="color: white; width: 30vh; font-size: 13px;">M3 Prod.</th>';/**/
        


        html += '</tr></thead><tbody>';

        // Utiliza una variable diferente para el cuerpo de la tabla
        var bodyHtml = '';

        // Itera sobre cada producto y crea una fila por producto
        for (let i = 0; i < this.filteredTasks.length; i++) {
            var task = this.filteredTasks[i];

            for (let j = 0; j < task[7].length; j++) { // Itera sobre la lista de productos en task[11]
                var product = task[7][j]; // Obtiene el nombre del producto
                var largo = task[10][j];
                var ancho = task[11][j];
                var alto = task[12][j];


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

                bodyHtml += `<td></td>`;/*Linea de Produccion*/
                bodyHtml += `<td>${task[5]}</td>`;/*Cliente*/
                bodyHtml += `<td></td>`;/*Item*/
                bodyHtml += `<td></td>`;/*Folio  / pedido id?*/
                bodyHtml += `<td></td>`;/*Cliente*/
                bodyHtml += `<td></td>`;/*OP*  / pedido id?*/
                bodyHtml += `<td></td>`;/*Mercado*/
                bodyHtml += `<td>${product}</td>`;/*Producto*/
                bodyHtml += `<td></td>`;/*ETA*/
                bodyHtml += `<td>L:${largo} A:${ancho} Al:${alto}</td>`;/*Diametros*/
                bodyHtml += `<td></td>`;/*ETA*/
                bodyHtml += `<td></td>`;/*ETA*/
                bodyHtml += `<td></td>`;/*ETA*/
                bodyHtml += `<td></td>`;/*ETA*/
                bodyHtml += `<td></td>`;/*ETA*/
                bodyHtml += `<td></td>`;/*ETA*/
                bodyHtml += `<td></td>`;/*ETA*/
                bodyHtml += `<td></td>`;/*ETA*/
                bodyHtml += `<td></td>`;/*ETA*/
                bodyHtml += `<td></td>`;/*ETA*/
                bodyHtml += `<td></td>`;/*ETA*/
                bodyHtml += `<td></td>`;/*ETA*/
                bodyHtml += '</tr>';
            }
        }

        // Agrega el cuerpo de la tabla al encabezado
        html += bodyHtml;

        html += '</tbody></table>';
        return html;
    }



    PedidoTable() {
        var html = '<table style="margin-left: auto; margin-right: auto;" class="second-table"><thead><tr>';

        // Agregar dos columnas adicionales a la izquierda
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center;">Linea</th>';
        html += '<th style="color: white; width: 20vh; font-size: 15px; text-align: center;">Fecha carga</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center;">OP</th>';
        html += '<th style="color: white; width: 25vh; font-size: 15px; text-align: center;">Cliente</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center;">Mercado</th>';
        html += '<th style="color: white; width: 20vh; font-size: 15px; text-align: center;">Fecha Creacion</th>';
        html += '<th style="color: white; width: 20vh; font-size: 15px; text-align: center;">ETA</th>';
        html += '<th style="color: white; width: 25vh; font-size: 15px; text-align: center;">Destino</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center;">Programa</th>';
        html += '<th style="color: white; width: 20vh; font-size: 15px; text-align: center;">Detalle</th>';



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

                bodyHtml += `<td style="text-align: center;">${task[13]}</td>`; /*Linea*/
                bodyHtml += `<td style="text-align: center;">${fechaFormateada}</td>`; /*Fecha de carga*/
                bodyHtml += `<td style="text-align: center;">${task[0]}</td>`;/*OP Orden Interna*/
                bodyHtml += `<td style="text-align: center;">${task[5]}</td>`; /*Cliente*/
                bodyHtml += `<td style="text-align: center;">${task[47]}</td>`; /*Mercado*/
                bodyHtml += `<td style="text-align: center;">${fechaFormateada3}</td>`; /*Fecha Creacion*/
                bodyHtml += `<td style="text-align: center;">${fechaFormateada2}</td>`; /*ETA*/
                bodyHtml += `<td style="text-align: center;">${task[48]}</td>`; /*Destino*/
                bodyHtml += `<td style="text-align: center;">${task[63]}</td>`; /*Programa*/
                bodyHtml += `<td style="text-align: center;"><a class="popup-link" data-pedido-id="${i}" data-popup-type="pedido">Ver...</a></td>`; /*Detalle*/

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
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center;">Linea</th>';
        html += '<th style="color: white; width: 20vh; font-size: 15px; text-align: center;">Producto</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center;">Largo</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center;">Ancho</th>';
        html += '<th style="color: white; width: 15vh; font-size: 15px; text-align: center;">Alto</th>';
        html += '<th style="color: white; width: 20vh; font-size: 15px; text-align: center;">Pqtes Solicitados</th>';
        html += '<th style="color: white; width: 20vh; font-size: 15px; text-align: center;">M3</th>';
        html += '<th style="color: white; width: 20vh; font-size: 15px; text-align: center;">ETA</th>';
        html += '<th style="color: white; width: 20vh; font-size: 15px; text-align: center;">Detalle</th>';



        html += '</tr></thead><tbody>';

        // Utiliza una variable diferente para el cuerpo de la tabla
        var bodyHtml = '';

        // Itera sobre cada producto y crea una fila por producto
        for (let i = 0; i < this.filteredTasks.length; i++) {
            var task = this.filteredTasks[i];
            for (let j = 0; j < task[7].length; j++) { // Itera sobre la lista de productos en task[11]
                var product = task[7][j]; // Obtiene el nombre del producto
                bodyHtml += `<td style="text-align: center;">${task[13]}</td>`;/*Linea*/
                bodyHtml += `<td style="text-align: center;">${task[7]}</td>`;/*Nombre del Producto*/
                bodyHtml += `<td style="text-align: center;">${task[24]}</td>`;/*Largo*/
                bodyHtml += `<td style="text-align: center;">${task[23]}</td>`;/*Ancho*/
                bodyHtml += `<td style="text-align: center;">${task[22]}</td>`;/*Alto*/
                bodyHtml += `<td style="text-align: center;">${task[54]}</td>`;/*pqtes solicitados*/
                bodyHtml += `<td style="text-align: center;">${task[25]}</td>`;/*M3*/
                bodyHtml += `<td style="text-align: center;">${task[2]}</td>`;/*ETA*/
                bodyHtml += `<td style="text-align: center;"><a class="popup-link" data-pedido-id="${i}" data-popup-type="producto">Ver...</a></td>`;/*Detalle*/

            }

                bodyHtml += '</tr>';
            
        }

        // Agrega el cuerpo de la tabla al encabezado
        html += bodyHtml;

        html += '</tbody></table>';
        return html;
    }
//______________
    PatronTable() {
        var html = '<table class="second-table"><thead><tr>';

        // Agregar dos columnas adicionales a la izquierda

        html += '<th style="color: white; width: 30vh; font-size: 13px;">Nro Pedido</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">diametro</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Largo Trozo</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Cantidad Piezas</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Producto Asociado</th>';
        html += '<th style="color: white; width: 30vh; font-size: 13px;">Detalles</th>';


        html += '</tr></thead><tbody>';

        // Utiliza una variable diferente para el cuerpo de la tabla
        var bodyHtml = '';

        // Itera sobre cada producto y crea una fila por producto
        for (let i = 0; i < this.filteredTasks.length; i++) {
            var task = this.filteredTasks[i];
                bodyHtml += `<td>${task[0]}</td>`;/*Nro Pedido*/
                bodyHtml += `<td>${task[35]}</td>`;/*Diametro*/
                bodyHtml += `<td>${task[24]}</td>`;/*Largo Trozo*/
                bodyHtml += `<td>${task[28]}</td>`;/*Cantidad Piezas*/
                bodyHtml += `<td>${task[44]}</td>`;/*Producto Asociado*/
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

    showProduccionTable() {
        this.filteredTasks = this.tasks;
        document.getElementById('gantt').innerHTML = this.buildSecondTable();

    }

    showSalidaTable() {
        this.filteredTasks = this.tasks;
        document.getElementById('gantt').innerHTML = this.SalidaTable();

    }
    showPatronesTable() {
        this.filteredTasks = this.tasks;
        document.getElementById('gantt').innerHTML = this.PatronTable();
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

    getMonthName(month) {
        return new Date(2020, month - 1, 1).toLocaleString('default', { month: 'long' });
    }

    filterTasksByLine(lineValue) {
        if (lineValue === "lineas") {
            this.filteredTasks = this.tasks;
        } else {
            this.filteredTasks = this.tasks.filter(task => task[5] === lineValue);
        }

        document.getElementById('gantt').innerHTML = this.buildTableHeader() + this.buildTableBody();
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
            html += '<th class="detalle-pedido-t">Op</th>';
            html += '<th class="detalle-pedido-t">item</th>';
            html += '<th class="detalle-pedido-t">Producto</th>';
            html += '<th class="detalle-pedido-t">Alto</th>';
            html += '<th class="detalle-pedido-t">Ancho</th>';
            html += '<th class="detalle-pedido-t">Largo</th>';
            html += `<td class="detalle-pedido-t">Pqte. Solicitados</td>`;
            html += '<th class="detalle-pedido-t">Alto.Paquete</th>';
            html += '<th class="detalle-pedido-t">Anc.paquete</th>';
            html += '<th class="detalle-pedido-t">Int.paquete</th>';
            html += '<th class="detalle-pedido-t">Tipo Empaque</th>';
            html += '<th class="detalle-pedido-t">Pzas</th>';
            html += '<th class="detalle-pedido-t">M3</th>';
            html += '<th class="detalle-pedido-t">Mbf</th>';
            html += '<th class="detalle-pedido-t">Diametro</th>';
            html += '<th class="detalle-pedido-t">Trozos</th>';
            html += `<td class="detalle-pedido-t">Largo Trozo</td>`;
            html += '<th class="detalle-pedido-t">Pzas x Trozos</th>';
            html += '<th class="detalle-pedido-t">Notas</th>';
            html += '<th class="detalle-pedido-t">Pzas x Pqte</th>';
            html += '<th class="detalle-pedido-t">Cant. de Sep. de 20MM</th>';

            html += '</tr></thead><tbody>';
        
            for (let i = 0; i < this.filteredTasks.length; i++) {
                var task = this.filteredTasks[i];
                if (task[0] === productoData[0]) { 
                    for (let j = 0; j < task[7].length; j++) {
                        console.log(task[7]);
        
                        html += '<tr>';
                        html += `<td class="detalle-pedido">${task[0]}</td>`; // Op
                        html += `<td class="detalle-pedido">${task[45]}</td>`; // Item
                        html += `<td class="detalle-pedido">${task[7]}</td>`; // Nombre producto
                        html += `<td class="detalle-pedido">${task[22]}</td>`; // alt.Producc
                        html += `<td class="detalle-pedido">${task[23]}</td>`; // Anc.Producc
                        html += `<td class="detalle-pedido">${task[24]}</td>`; // Lar.Producc
                        html += `<td class="detalle-pedido">${task[54]}</td>`; // Pqte
                        html += `<td class="detalle-pedido">${task[56]}</td>`; // Alto.Paquete
                        html += `<td class="detalle-pedido">${task[67]}</td>`; // Anc.paquete
                        html += `<td class="detalle-pedido">${task[57]}</td>`; // Int.paquete
                        html += `<td class="detalle-pedido">${task[55]}</td>`; // Tipo Empaque
                        html += `<td class="detalle-pedido">${task[64]}</td>`; // Pzas
                        html += `<td class="detalle-pedido">${task[25]}</td>`; // M3
                        html += `<td class="detalle-pedido">${task[60]}</td>`; // Mbf
                        html += `<td class="detalle-pedido"></td>`; //Diametro  (colocar como null)
                        html += `<td class="detalle-pedido"></td>`; //Numero de Trozos (colocar como null)
                        html += `<td class="detalle-pedido"></td>`; //largo trozo (colocar como null)
                        html += `<td class="detalle-pedido"></td>`; //Piezas*Trozo (colocar como null)   ////consular con los profes
                        html += `<td class="detalle-pedido"></td>`; //Notas (colocar como null)   ////consular con los profes
                        html += `<td class="detalle-pedido"></td>`; //Piezas*pqte (colocar como null)
                        html += `<td class="detalle-pedido"></td>`; //Separadores(colocar como null)

        
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
                    <button style="margin-top: 2vh; margin-left: 47%; background-color: red; color: white; width:6%; border: 1px solid white;" class="close-button">Cerrar</button>
                </div>
            `;
            
    



        }else if (popupType === 'pedido') {
            productoData = this.tasks[pedidoId];
            

            var html = '<table class="second-table"><thead><tr>';
            html += '<th class="detalle-pedido-t">Item</th>';
            html += '<th class="detalle-pedido-t">Nombre producto</th>';
            html += '<th class="detalle-pedido-t">Est</th>';
            html += '<th class="detalle-pedido-t">term</th>';
            html += '<th class="detalle-pedido-t">Calidad</th>';
            html += '<th class="detalle-pedido-t">FSC</th>';
            html += '<th class="detalle-pedido-t">Esp.Fact</th>';
            html += '<th class="detalle-pedido-t">Anc.Fact</th>';
            html += '<th class="detalle-pedido-t">Lar.Fact</th>';
            html += '<th class="detalle-pedido-t">Esp.Producc</th>';
            html += '<th class="detalle-pedido-t">Anc.Producc</th>';
            html += '<th class="detalle-pedido-t">Lar.Producc</th>';
            html += '<th class="detalle-pedido-t">Tipo Empaque</th>';
            html += '<th class="detalle-pedido-t">Alto.Paquete</th>';
            html += '<th class="detalle-pedido-t">Anc.paquete</th>';
            html += '<th class="detalle-pedido-t">Int.paquete</th>';
            html += '<th class="detalle-pedido-t">Pzas</th>';
            html += '<th class="detalle-pedido-t">Pqte</th>';
            html += '<th class="detalle-pedido-t">M3</th>';
            html += '<th class="detalle-pedido-t">Mbf</th>';
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
                        html += `<td class="detalle-pedido">${task[45]}</td>`; // Item
                        html += `<td class="detalle-pedido">${task[7]}</td>`; // Nombre producto
                        html += `<td class="detalle-pedido">${task[26]}</td>`; // Est
                        html += `<td class="detalle-pedido">${task[58]}</td>`; // term
                        html += `<td class="detalle-pedido">${task[59]}</td>`; // Calidad
                        html += `<td class="detalle-pedido">${task[50]}</td>`; // FSC
                        html += `<td class="detalle-pedido">${task[51]}</td>`; // Esp.Fact
                        html += `<td class="detalle-pedido">${task[52]}</td>`; // Anc.Fact
                        html += `<td class="detalle-pedido">${task[53]}</td>`; // Lar.Fact
                        html += `<td class="detalle-pedido">${task[22]}</td>`; // alt.Producc
                        html += `<td class="detalle-pedido">${task[23]}</td>`; // Anc.Producc
                        html += `<td class="detalle-pedido">${task[24]}</td>`; // Lar.Producc
                        html += `<td class="detalle-pedido">${task[55]}</td>`; // Tipo Empaque
                        html += `<td class="detalle-pedido">${task[56]}</td>`; // Alto.Paquete
                        html += `<td class="detalle-pedido">${task[67]}</td>`; // Anc.paquete
                        html += `<td class="detalle-pedido">${task[57]}</td>`; // Int.paquete
                        html += `<td class="detalle-pedido">${task[64]}</td>`; // Pzas
                        html += `<td class="detalle-pedido">${task[54]}</td>`; // Pqte
                        html += `<td class="detalle-pedido">${task[25]}</td>`; // M3
                        html += `<td class="detalle-pedido">${task[60]}</td>`; // Mbf
                        html += `<td class="detalle-pedido">${task[62]}</td>`; // Marca
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
                    <button style="margin-top: 2vh; margin-left: 47%; background-color: red; color: white; width:6%; border: 1px solid white;" class="close-button">Cerrar</button>
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
                <button class="close-button">Cerrar</button>
            </div>
        `;
        }
        document.body.appendChild(popup);

        // Add a click event listener to the close button
        const closeButton = popup.querySelector('.close-button');
        closeButton.addEventListener('click', () => {
            self.closePopup(popup);
        });
        
    }

    closePopup(popup) {
        popup.style.display = 'none';
    }
}


const periodosSelect = document.querySelector('select[name="periodos"]');
periodosSelect.value = "diario";
periodosSelect.addEventListener('change', function () {
    gantt.setMinAndMaxDate();
    document.getElementById('gantt').innerHTML = gantt.buildTableHeader() + gantt.buildTableBody();
});

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

// Fisher-Yates shuffle function
function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}
// Add your shuffleButton click event listener here
const shuffleButton = document.getElementById('shuffleButton');
shuffleButton.addEventListener('click', () => {
    shuffle(gantt.tasks);
    gantt.setMinAndMaxDate();
    document.getElementById('gantt').innerHTML = gantt.buildTableHeader() + gantt.buildTableBody();
    gantt.attachEventListeners();
});
//Popup para importar
function showPopupimport() {
    const popupOverlay = document.getElementById('popupContainer');
    popupOverlay.style.display = 'block';
}

function closePopupimport() {
    const popupOverlay = document.getElementById('popupContainer');
    popupOverlay.style.display = 'none';
}

// Función para cerrar el popup
function closePopup() {
    var popup = document.getElementById("carga-form");
    popup.style.display = "none";
}




