function showDetails() {
    // Obtenha o elemento de seleção
    var selectPartidas = document.getElementById("partidas");
    // Obtenha o índice selecionado
    var selectedIndex = selectPartidas.selectedIndex;
    // Obtenha o texto da opção selecionada
    var selectedOption = selectPartidas.options[selectedIndex].text;

    // Div que conterá os detalhes da partida
    var detalhesPartida = document.getElementById("detalhesPartida");

    // Atualize os detalhes da partida com base na opção selecionada
    switch (selectedOption) {
        case "16/04/2023-16:00 Palmeiras x Cuiabá":
            document.getElementById("EquipeMandante").value = "Palmeiras";
            document.getElementById("EquipeVisitante").value = "Cuiabá";
            document.getElementById("EstadioPartida").value = "Allianz Parque";
            document.getElementById("DataTime").value = "2023-04-16T16:00";
            document.getElementById("Placar").value = "0 - 0";
            break;
        case "20/04/2023-18:00 Flamengo x Corinthians":
            document.getElementById("EquipeMandante").value = "Flamengo";
            document.getElementById("EquipeVisitante").value = "Corinthians";
            document.getElementById("EstadioPartida").value = "Maracanã";
            document.getElementById("DataTime").value = "2023-04-20T18:00";
            document.getElementById("Placar").value = "2 - 1";
            break;
        // Adicione mais casos conforme necessário
    }
}
