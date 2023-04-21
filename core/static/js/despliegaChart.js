function mostrarRecuadro() {
    var tipoGrafico = document.getElementById("tipoGrafico").value;
    var recuadro = document.getElementById("recuadro");
    switch (tipoGrafico) {
      case "pastelChart":
        recuadro.innerHTML = "Has seleccionado un Pastel Chart";
        break;
      case "radarChart":
        recuadro.innerHTML = "Has seleccionado un Radar Chart";
        break;
      case "barraChart":
        recuadro.innerHTML = "Has seleccionado un Barra Chart";
        break;
      default:
        recuadro.innerHTML = "";
    }
  }