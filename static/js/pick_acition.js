const deleteQuery = document.body.querySelectorAll(".character-delete");
const deleteQueryWindow = document.body.querySelector(".query-delete");
const NO_delete = document.body.querySelector(".query-delete-no");
const YES_delete = document.body.querySelector(".query-delete-yes");

const createQueryContainer = document.body.querySelectorAll(".character-add");

let cache_delete_index = 0;


createQueryContainer.forEach((el)=>{
    el.addEventListener("click", ()=>{
        window.location = "/create-character";
    })
})

deleteQuery.forEach((btn, idx)=>{
    btn.addEventListener("click", (e)=>{
        e.preventDefault();
        deleteQueryWindow.style.display = 'block';
        cache_delete_index = e.target.dataset.index;
    })
});

NO_delete.addEventListener("click", (e)=>{
    e.preventDefault();
    deleteQueryWindow.style.display = 'none';
});

YES_delete.addEventListener("click", (e)=>{
    e.preventDefault();
    window.location = `/delete/${cache_delete_index}`;
    deleteQueryWindow.style.display = 'none';
    cache_delete_index = 0;
});