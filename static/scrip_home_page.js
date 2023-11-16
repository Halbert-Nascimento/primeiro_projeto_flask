document.addEventListener("DOMContentLoaded", function () {
  var nome_usuario = document
    .getElementById("container_dados_user")
    .getAttribute("data-nome-usuario");

  if (nome_usuario) {
    document.getElementById("logado").innerText = nome_usuario;
    document.getElementById("link_menu").innerText = "Menu";
    varLink = document.getElementById("logado").href = "/perfil";
    varLink = document.getElementById("link_menu").href = "/perfil";
  } else {
    document.getElementById("link_menu").innerText = "Registrar";
  }
});
