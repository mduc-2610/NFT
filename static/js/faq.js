const faqButton = document.querySelectorAll(".faq__feature-1")
faqButton.forEach(function (button) {
    const faqPlus = button.children[0];
    const faqMinus = button.children[1];
    const faqAnswer = button.nextElementSibling.children[1];
    const faqItem = button.parentElement;
    console.log(faqItem);
    button.addEventListener("click", function () {
        faqAnswer.classList.toggle("show");
        faqMinus.classList.toggle("show-minus");
        faqPlus.classList.toggle("show-plus");
        faqItem.classList.toggle("change-border-color");
        button.style.transition = "max-height 0.4s ease;";
        console.log("asdasddasdsd")
    });
});
