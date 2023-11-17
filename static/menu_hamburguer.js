document.addEventListener("DOMContentLoaded", function () {
  const menuHamburguer = document.getElementById("menuHamburguer");
  const opcoesMenu = document.getElementById("opcoesMenu");

  menuHamburguer.addEventListener("click", function () {
    opcoesMenu.classList.toggle("mostrar");
  });

  // Fechar o menu de opções se o usuário clicar fora dele
  document.addEventListener("click", function (event) {
    if (
      !event.target.matches("#menuHamburguer") &&
      !event.target.matches("#opcoesMenu")
    ) {
      opcoesMenu.classList.remove("mostrar");
    }
  });
});
