document.addEventListener("DOMContentLoaded", function () {
  // var nome = document.getElementById("container_dados_user").getAttribute("data-nome");
  var nome = document.getElementById("container_dados_user").dataset.nome;
  var email = document.getElementById("container_dados_user").dataset.email;
  var telefone = document.getElementById("container_dados_user").dataset
    .telefone;

  // var primeiro_nome = nome.split(" ", 1);
  varLink = document.getElementById("foto_perfil").src =
    "/static/imagens/pag/perfil_vazio.jpg";
  document.getElementById("nome").innerHTML = nome.toUpperCase();
  document.getElementById("email").innerHTML = "Email: " + email;
  document.getElementById("telefone").innerHTML = "Telefone: " + telefone;
});
