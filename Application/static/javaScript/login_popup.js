//function abrirPopup() {
//  document.getElementById("loginPopup").style.display = "block"; /* Altura da barra de cabeçalho */
//}

//function fecharPopup() {
//  document.getElementById("loginPopup").style.display = "none";
//}

//document.getElementById("loginBtn").addEventListener("click", abrirPopup);

function abrirPopup() {
    document.getElementById("loginPopup").classList.add("mostrar-popup");
}

function fecharPopup() {
    document.getElementById("loginPopup").classList.remove("mostrar-popup");
}

document.getElementById("loginBtn").addEventListener("click", abrirPopup);
  