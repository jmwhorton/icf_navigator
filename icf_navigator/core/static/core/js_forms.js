var question_load_once = false;
window.addEventListener("load", function(){
  if(question_load_once) return;
  function sendData(form){
    const XHR = new XMLHttpRequest();

    const FORM_DATA = new FormData(form);

    // success
    XHR.addEventListener("load", function(event){
      //alert(event.target.responseText);
      if(event.target.status == 200){
        location.reload();
      } else {
        alert(event.target.responseText);
      }
    });

    // error
    XHR.addEventListener("error", function(event){
      alert("save failed");
    });

    XHR.open("POST", form.action);

    XHR.send(FORM_DATA);
  }

  for(let form of document.getElementsByClassName("question_form")){
    form.addEventListener("submit", function(event){
      event.preventDefault();
      sendData(form);
    });
    question_load_once = true;
  }
});
