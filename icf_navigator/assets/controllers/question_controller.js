import { Controller } from "stimulus"

export default class extends Controller {
  static targets = ["form", "save"];
  static values = { url: String, id: String }

  connect() {
    this.saveTarget.disabled = true;
  }

  dirty() {
    this.saveTarget.disabled = false;
    // quick fix for custom questions potentially lacking a trix wrapper
    if(document.getElementById(`${this.idValue}_trix_wrapper`)){
      document.getElementById(`${this.idValue}_trix_wrapper`).style.display = 'none';
    }
  }

  trixDirty(){
    this.saveTarget.disabled = false;
  }

  clean() {
    this.saveTarget.disabled = true;
  }

  sendData(){
    const XHR = new XMLHttpRequest();

    const FORM_DATA = new FormData(this.formTarget);

    const url = this.urlValue;
    const c = this.saveTarget;
    const id = this.idValue;

    // success
    XHR.addEventListener("load", function(event){
      if(event.target.status == 200){
        let el = document.getElementById(`question_wrapper_${id}`);
        if(el !== null){
          el.innerHTML = event.target.responseText;
        }
        fetch(url)
          .then(response => response.text())
          .then(html => document.getElementById("small_wrapper").innerHTML = html);
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
    this.sendData();
  }
}
