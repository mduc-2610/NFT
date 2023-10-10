// Get references to the elements
console.log("hello worlsdffsdfdsfd");
const menuIcon = document.querySelector('.header__menu-icon');
const logoWrap = document.querySelector('.header__logo--wrap');
const navbar = document.querySelector('.header__navbar');
const search = document.querySelector('.header__search');

// menuIcon.addEventListener('click', () => {
  //   // Toggle the visibility of the elements
  //   if (menuIcon.style.display !== 'none') {
    //     menuIcon.style.display = 'none';
    //     logoWrap.style.display = 'none';
    //     search.style.display = 'none';
    //     navbar.style.display = 'block';
    //   }
    // });
    
    // const headerNavItemLink = document.querySelector(".header-nav-item__link");
    // const headerNavChild = document.querySelector(".header-nav-child");
    
    // headerNavItemLink.addEventListener('click', (e) => {
//     // if(headerNavChild.style.display == 'none') {
//         e.preventDefault();
//         e.stopPropagation();
//         headerNavChild.style.display == 'block';
//     // }
// })

headerNavItemChild =  document.querySelectorAll(".header-nav-item-child");
// console.log("1")
// for (var element of headerNavItemChild){
  
  //   console.log(element.textContent.trim());
  // }
  headerNavItemChild[1].addEventListener('click', (e) =>{
    e.preventDefault();
    const url = document.querySelector('.header-nav-item-child__link').getAttribute('href');
    // window.location.href = "{% url 'home' %}";
    // window.location.href = "/home2/";
    // console.log("Hello");
  })
  
  // const deleteIcon = document.querySelector('.delete-icon');
  // deleteIcon.addEventListener('click', () => {
    //   // Delete the input tag
    //   const input = document.querySelector('.searchTerm');
    // });
    
    
    console.log("asfsdfsdffsdfsdf")
    const connectButton = document.querySelector(".header-login__button");
    connectButton.addEventListener('click', () => {
      console.log("abc");
      document.querySelector(".connect").style.display = 'flex';
    })

    const connect = document.querySelector(".connect");
    connect.addEventListener('click', (e) => {
      e.stopPropagation();
      document.querySelector(".connect").style.display = 'none';
    })