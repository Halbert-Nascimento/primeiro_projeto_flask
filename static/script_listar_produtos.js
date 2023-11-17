// Seleciona todos os containers com a classe 'sua-classe'
var containers = document.querySelectorAll(".containner_item");

// Adiciona um ouvinte de eventos de clique a cada container
containers.forEach(function (container, indice) {
  container.addEventListener("click", function () {
    // Quando clicado, faça algo com o container específico
    console.log("Clicou no container " + indice);

    // Ou, se você quiser se referir ao container específico no evento, use 'this':
    // console.log("Clicou no container " + containers.indexOf(this));
    var slide = this.querySelector('[data-js="carrossel"]');
    const nextButton = document.querySelector('[data-js="button_next"]');
    const previusButton = document.querySelector('[data-js="button_previus"]');
    let currentSlideIndex = 0;

    nextButton.addEventListener("click", () => {
      currentSlideIndex++;
      slides.forEach((slides) => {
        slides.classList.remove(".visivel");
      });
      slides[currentSlideIndex].classList.add(".visivel");
    });
  });
});

// var slides = this.querySelectorAll(".containner_img");
// const nextButton = document.querySelector('[data-js="button_next"]');
// const previusButton = document.querySelector('[data-js="button_previus"]');
// let currentSlideIndex = 0;

// nextButton.addEventListener("click", () => {
//   currentSlideIndex++;
//   slides.forEach((slides) => {
//     slides.classList.remove(".visivel");
//   });
//   slides[currentSlideIndex].classList.add(".visivel");
// });
