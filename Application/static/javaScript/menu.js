
window.addEventListener('scroll', function(){
    let header = document.querySelector('#header')
    header.classList.toggle('rolagem', window.scrollY > 0)
})

function voltarPaginaAnterior() {
    history.back();
}

function toggleSubMenu(subMenuId) {
    const subMenu = document.getElementById(subMenuId);
    if (subMenu.style.display === 'block') {
      subMenu.style.display = 'none';
    } else {
      subMenu.style.display = 'block';
    }
  }

function previousRound() {
    var currentRound = parseInt(document.getElementById('roundNumber').innerText);
    if (currentRound > 1) {
        currentRound -= 1;
        window.location.href = "/partidas?rodada=" + currentRound;
    }
}

function nextRound() {
    var currentRound = parseInt(document.getElementById('roundNumber').innerText);
    // Suponho que você tenha o número total de rodadas armazenado em uma variável chamada 'totalRounds'
    // Substitua 'totalRounds' pelo valor correto
    var totalRounds = 20; // Exemplo

    if (currentRound < totalRounds) {
        currentRound += 1;
        window.location.href = "/partidas?rodada=" + currentRound;
    }
}
    