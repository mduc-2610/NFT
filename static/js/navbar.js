const headerMenuIcon = document.querySelector('.header__menu-icon');
    headerMenuIcon.onclick = (e) => {
        document.querySelector('.navbar').style.display = 'block';
    }
    const navbarBack = document.querySelector('.navbar-back');
    navbarBack.onclick = (e) => {
        document.querySelector('.navbar').style.display = 'none';
    }
    const headerBackIcon = document.querySelector('.header-back');
    const navbarLinkDefault = document.querySelectorAll('.navbar__link--default');
    navbarLinkDefault.forEach((link) => {
        link.onclick = (e) => {
            e.preventDefault();
        }
    });
    const navbarItem = document.querySelectorAll('.navbar__item');
    navbarItem.forEach((link) => {
        link.onclick = (e) => {
            const navbarChild = link.querySelector(".navbar-child__list");
            if (navbarChild) {
                navbarChild.classList.toggle('show');
                link.querySelector('.navbar__link svg').classList.toggle('rotate');
                navbarItem2 = navbarChild.querySelectorAll(".navbar-child__item");
                console.log(navbarItem2);
                navbarItem2.forEach((link2) => {
                    link2.onclick = (e) => {
                        e.stopPropagation();
                        const navbarChild2 = link2.querySelector(".navbar-child-2__list");
                        if (navbarChild2) {
                            navbarChild2.classList.toggle('show');
                            link2.querySelector('.navbar__link svg:nth-child(2)').classList.toggle('rotate');
                        }
                    }
                });     
            }
        }
    });

const headerSearchButton = document.querySelector('.header__search-button');
const headerSearchInput = document.querySelector('.header__search-input');
const navbarList = document.querySelector('.navbar__list');
const headerMenuBack = document.querySelector('.header__menu-back');

function getWindowWidth() {
    var width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
        console.log("Window width: " + width + " pixels");
}
var prevSize = "";
headerSearchInput.addEventListener('click', (e) => {
    prevSize = window.getComputedStyle(headerSearchInput.parentElement).getPropertyValue('width');
    headerSearchInput.parentElement.style.width = "70%";
    navbarList.style.display = 'none';
    headerMenuBack.style.display = 'block';
});
console.log("Previous size" + prevSize + "*********" + window.getComputedStyle(headerSearchInput.parentElement).getPropertyValue('width'));
window.addEventListener("resize", (e) => {
    var width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    headerMenuBack.addEventListener('click', (e) => {
        headerSearchInput.parentElement.style.width = prevSize;
        navbarList.style.display = 'flex';
        headerMenuBack.style.display = 'none';
    });
});

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


    // const connect = document.querySelector(".connect");
    // connect.addEventListener('click', (e) => {
    //   e.stopPropagation();
    //   document.querySelector(".connect").style.display = 'none';
    // })