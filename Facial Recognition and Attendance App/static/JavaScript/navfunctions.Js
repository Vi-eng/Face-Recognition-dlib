document.getElementById('hmbgr').onclick =  function() {
    dropit();
};


//Functions
function dropit(){
    var dropitems = document.getElementById('nav');
    dropitems.classList.toggle('active');
    var content = document.getElementById('content');
    content.classList.toggle('navactive');
}

var title = document.getElementsByTagName('title');
var navs = document.getElementsByClassName('nav');

Array.prototype.forEach.call(navs, (value) => {
    if (title[0].innerHTML == value.innerHTML){
        value.classList.add('acti');
    }else{
        value.classList.remove('acti');
    };    
});
