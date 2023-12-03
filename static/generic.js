//Script para teste de implementação de novas funções
//Scrip linkado na pagina LISTAR_PRODUTOS.HTML E CADASTRAR_PRODUTOS.HTML
// APOS TESTE MOVER SCRIPT PARA DEVIDOS ARQUIVOS CORRESPONDES A CADA PAGINA

/*
  FUNÇÃO FORMATAR NOME,  
  REMOVER NOME COMPOSTO, SOBRE NOME e
  MOSTRAR SÓ PRIMEIRO NOME
*/

// document.addEventListener("DOMContentLoaded", function () {
//   // var nome = document.getElementById("container_dados_user").getAttribute("data-nome");
//   var nome = document.getElementById("container_dados_user").dataset.nome;

//   var primeiro_nome = nome.split(" ", 1);

//   document.getElementById("nome_nav").innerHTML = primeiro_nome;
// });


//########################## FIM e 
//################################# inicio de outr seção ######################


document.addEventListener("DOMContentLoaded", function () {
  // essa função espera a pagina html ser carregada primeiro
  const produtos = document.querySelectorAll('.containner_item');

  produtos.forEach((produto)) => {
    const carrossel = produto.querySelector('[data-js="carrossel"]');
    const buttonPrev = produto.querySelector('[data-js="button_previus"]');
    const buttonNext = produto.querySelector('[data-js="button_next"]');

    let currentIndex = 0;

    buttonPrev.addEventListener('click', function(){
      currentIndex = (currentIndex -1 + carrossel.children.lenght) % carrossel.children.lenght;
      updateCarousel();
    });

    buttonNext.addEventListener('click', function () {
      currentIndex = (currentIndex + 1) % carrossel.children.length;
      updateCarousel();
    });

    function updateCarousel(){
      const translateValue = -currentIndex * 100 + '%';
      carrossel.style.transform = 'translateX('+ translateValue +')';

    }


  }
});   


