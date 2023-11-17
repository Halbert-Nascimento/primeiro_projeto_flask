document.addEventListener("DOMContentLoaded", function () {
  // var nome = document.getElementById("container_dados_user").getAttribute("data-nome");
  var nome = document.getElementById("container_dados_user").dataset.nome;

  var primeiro_nome = nome.split(" ", 1);

  document.getElementById("nome_nav").innerHTML = primeiro_nome;
});
