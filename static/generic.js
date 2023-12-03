//Script para teste de implementação de novas funções
//Scrip linkado na pagina LISTAR_PRODUTOS.HTML E CADASTRAR_PRODUTOS.HTML
// APOS TESTE MOVER SCRIPT PARA DEVIDOS ARQUIVOS CORRESPONDES A CADA PAGINA

/*
  FUNÇÃO FORMATAR NOME,  
  REMOVER NOME COMPOSTO, SOBRE NOME e
  MOSTRAR SÓ PRIMEIRO NOME
*/

document.addEventListener("DOMContentLoaded", function () {
  // var nome = document.getElementById("container_dados_user").getAttribute("data-nome");
  var nome = document.getElementById("container_dados_user").dataset.nome;

  var primeiro_nome = nome.split(" ", 1);

  document.getElementById("nome_nav").innerHTML = primeiro_nome;
});
