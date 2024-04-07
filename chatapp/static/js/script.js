const box=document.getElementById("box");

const input_username=document.querySelector("input[name='username']")

const startbutton=document.getElementById("start")

const closebox=document.getElementById("close-box")


let radios = document.querySelectorAll('input[type="radio"][name="choice"]');

let flag=0;
toggle_avatars=()=>{
    if(flag===0){
        flag=1;
    }
    else{
        flag=0;
    }
radios[flag].checked=true;
}

document.addEventListener("keydown",(e)=>{
if(e.key==="Enter"){
    startbutton.click();
}
else if(e.key==="ArrowLeft"){
toggle_avatars();
}
else if(e.key==='ArrowRight'){
toggle_avatars();
}
else if(e.key==='Escape'){
    closebox.click();
}
    
});

startbutton.addEventListener("click",(event)=>{
box.style.display="block";
input_username.focus();
});

closebox.addEventListener("click",(e)=>{
input_username.textContent="";
box.style.display="none";
});

