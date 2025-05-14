document.addEventListener('DOMContentLoaded', function () {
    setTimeout(() => {
        const nextButton = document.getElementById('next_page');

        if (nextButton) {
            console.log("Boton 'Next' encontrado: " + nextButton)
        } else console.log("Aqui no hay nada macho")
    }, 300);
});
