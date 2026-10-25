const menu=document.querySelector('#menu');
menu?.addEventListener('click',()=>{const open=document.body.classList.toggle('menuopen');menu.setAttribute('aria-expanded',String(open));});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){document.body.classList.remove('menuopen');menu?.setAttribute('aria-expanded','false');}});
document.querySelector('#search')?.addEventListener('input',e=>{const term=e.target.value.toLocaleLowerCase().trim();document.querySelectorAll('nav a').forEach(a=>a.hidden=!a.textContent.toLocaleLowerCase().includes(term));});
