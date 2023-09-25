// Get references to the elements
const menuIcon = document.querySelector('.header__menu-icon');
const logoWrap = document.querySelector('.header__logo--wrap');
const navbar = document.querySelector('.header__navbar');
const search = document.querySelector('.header__search');

// Add a click event listener to the menu icon button
menuIcon.addEventListener('click', () => {
  // Toggle the visibility of the elements
  if (menuIcon.style.display !== 'none') {
    menuIcon.style.display = 'none';
    logoWrap.style.display = 'none';
    search.style.display = 'none';
    navbar.style.display = 'block';
  }
});

const headerNavItemLink = document.querySelector(".header-nav-item__link");
const headerNavChild = document.querySelector(".header-nav-child");

headerNavItemLink.addEventListener('click', (e) => {
    // if(headerNavChild.style.display == 'none') {
        e.preventDefault();
        e.stopPropagation();
        headerNavChild.style.display == 'block';
    // }
})

// const deleteIcon = document.querySelector('.delete-icon');
// deleteIcon.addEventListener('click', () => {
//   // Delete the input tag
//   const input = document.querySelector('.searchTerm');
// });

