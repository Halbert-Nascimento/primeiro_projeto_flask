//########################## FIM e
// document.addEventListener("DOMContentLoaded", function () {
//   // essa função espera a pagina html ser carregada primeiro
// });
//################################# inicio de outr seção ######################

//seleciona todas as div com classe data-js="containner_produto
const container_produtos = document.querySelectorAll(
  '[data-js="containner_produto"]'
);

//adc ouvinte para os conteudos da div
container_produtos.forEach((container_produto) => {
  //captura botoes dentro do container
  const prevButton = container_produto.querySelector('[data-js="button_prev"]');
  const nextButton = container_produto.querySelector('[data-js="button_next"]');

  //captura as imagens dentro do container
  const slides = container_produto.querySelectorAll(
    '[data-js="carrossel_img"]'
  );

  // indice controle de slide
  let currentIndex = 0;

  //Adiciona um ouvinte de click
  nextButton.addEventListener("click", () => {
    if (currentIndex === slides.length - 1) {
      currentIndex = 0;
    } else {
      currentIndex++;
    }

    //percorre removendo a class que deixa visivel para posterior adicionar visivel no slide corrente
    slides.forEach((slide) => {
      slide.classList.remove("visivel");
    });

    //adc classe visivel novamente no slide currenteIndex
    slides[currentIndex].classList.add("visivel");
    // console.log(currentIndex);
  });

  //Adiciona um ouvinte de click
  prevButton.addEventListener("click", () => {
    if (currentIndex === 0) {
      currentIndex = slides.length - 1;
    } else {
      currentIndex--;
    }

    //percorre removendo a class que deixa visivel para posterior adicionar visivel no slide corrente
    slides.forEach((slide) => {
      slide.classList.remove("visivel");
    });

    //adc classe visivel novamente no slide currenteIndex
    slides[currentIndex].classList.add("visivel");
    // console.log(currentIndex);
  });
});
