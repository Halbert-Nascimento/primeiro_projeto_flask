document.addEventListener("DOMContentLoaded", function () {
  var nome_usuario = document
    .getElementById("container_dados_user")
    .getAttribute("data-nome-usuario");

  if (nome_usuario) {
    nome_usuario = nome_usuario.split(" ", 1);
    document.getElementById("logado").innerText = nome_usuario;
    document.getElementById("link_menu").innerText = "Menu";
    document.getElementById("logado").href = "/perfil";
    document.getElementById("link_menu").href = "/perfil";
  } else {
    document.getElementById("link_menu").innerText = "Registrar";
  }
});
