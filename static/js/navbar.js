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

    // const ownerCloseButton = document.querySelector(".owner__close");
    // const ownerBlock = document.querySelector(".owner");
    // const ownerContainer = document.querySelector(".container-owner");
    // ownerCloseButton.onclick = (e) => {
    //     ownerContainer.style.display = "none";
    // }
    
    // ownerContainer.onclick =  (e) => {
    //     if (e.target !== ownerBlock) {
    //         ownerContainer.style.display = "none";
    //     }
    // };
    
    // ownerBlock.onclick = (e) => {
    //     e.stopPropagation();
    // }

    const connectButton = document.querySelectorAll('.header-login__button');
    const connect = document.querySelector('.connect');
    const connectContainer = document.querySelector('.container-connect');
    connectButton.forEach((button) => {
        button.onclick = (e) => {
          connect.style.display = 'flex';
        };
    });
    console.log( document.querySelector('.connect'));
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



    // const connect = document.querySelector(".connect");
    // connect.addEventListener('click', (e) => {
    //   e.stopPropagation();
    //   document.querySelector(".connect").style.display = 'none';
    // })