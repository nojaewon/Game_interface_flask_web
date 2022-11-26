const character_group = document.body.querySelectorAll(".character-container");

character_group.forEach((character, index) => (
    character.addEventListener("click", ()=>{
        window.location = `/pick/${index}`
    })
));