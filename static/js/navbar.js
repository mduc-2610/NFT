
const connectButton = document.querySelectorAll('.header-login__button');
const connect = document.querySelector('.connect');
const connectContainer = document.querySelector('.container-connect');
connectButton.forEach((button) => {
  button.onclick = (e) => {
      connect.style.display = 'flex';
  };
});
connect.onclick = (e) => {
  console.log(e.target);
  if(e.target !== connectContainer) {
      console.log("OKOKOK");
      connect.style.display = 'none';
  }
}

connectContainer.onclick = (e) => {
  e.stopPropagation();
}

const connectCloseButton = document.querySelector('.connect__close-button');
connectCloseButton.onclick = (e) => {
  connect.style.display = 'none';
};

