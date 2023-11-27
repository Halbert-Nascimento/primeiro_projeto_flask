//Script para pagina INDEX faz alteração do dom para interatividade com usuario logado

// função para esperar todo o documento html carregar para setar as configurações
document.addEventListener("DOMContentLoaded", function () {
  //pega o nome de usuario do documento html pelo conteiner de datas
  var nome_usuario = document
    .getElementById("container_dados_user")
    .getAttribute("data-nome-usuario");

  if (nome_usuario) {
    nome_usuario = nome_usuario.split(" ", 1); //Quebra o nome composto e salva so o primeiro nome
    document.getElementById("logado").innerText = nome_usuario; //troca texto da tela
    document.getElementById("link_menu").innerText = "Menu";
    document.getElementById("logado").href = "/perfil"; // troca o link
    document.getElementById("link_menu").href = "/perfil";
  } else {
    document.getElementById("link_menu").innerText = "Registrar";

    var menu = document.getElementById("container-logoutID"); // seleciona id do index do menu
    menu.classList.remove("menu-container"); //remove a class que seta as configuraçoes do menu
    menu.classList.add("container-logout"); //adc outra class, para não quebra layout
  }
});
