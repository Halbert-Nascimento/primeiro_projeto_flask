// script para pagina de PERFIL

document.addEventListener("DOMContentLoaded", function () {
  // var nome = document.getElementById("container_dados_user").getAttribute("data-nome");
  var nome = document.getElementById("container_dados_user").dataset.nome;
  var email = document.getElementById("container_dados_user").dataset.email;
  var telefone = document.getElementById("container_dados_user").dataset
    .telefone;
  var total_produtos = document.getElementById("container_dados_user").dataset
    .total_produtos;
  var foto_perfil = document.getElementById("container_dados_user").dataset
    .f_perfil;

  var primeiro_nome = nome.split(" ", 1);
  if (!foto_perfil) {
    varLink = document.getElementById("foto_perfil").src =
      "/static/imagens/pag/perfil_vazio.png";
  } else {
    varLink = document.getElementById("foto_perfil").src = foto_perfil;
  }

  document.getElementById("nome_nav").innerHTML = primeiro_nome;
  document.getElementById("nome").innerHTML = nome.toUpperCase();
  // document.getElementById("email").innerHTML = "Email: " + email;
  document.getElementById("telefone").innerHTML = telefone;
  document.getElementById("total_publicações").innerHTML = total_produtos;
});
