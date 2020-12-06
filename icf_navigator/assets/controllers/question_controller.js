import { Controller } from "stimulus"

export default class extends Controller {
  static targets = ["form"];
  static values = { url: String }

  sendData(url){
    const XHR = new XMLHttpRequest();

    const FORM_DATA = new FormData(this.formTarget);

    // success
    XHR.addEventListener("load", function(event){
      //alert(event.target.responseText);
      if(event.target.status == 200){
        fetch(url)
        .then(response => response.text())
        .then(html => document.getElementById("small_preview").innerHTML = html);
      } else {
        alert(event.target.responseText);
      }
    });

    // error
    XHR.addEventListener("error", function(event){
      alert("save failed");
    });

    XHR.open("POST", this.formTarget.action);

    XHR.send(FORM_DATA);
  }

  submit(event){
    event.preventDefault();
    this.sendData(this.urlValue);
  }
}
