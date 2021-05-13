import { Controller } from "stimulus"

 function yesnoTotruefalse(yesno, truefalse){
  if(yesno == 'Y' && truefalse == 'True'){
    return false
  } else if (yesno == 'N' && truefalse == 'False') {
    return false
  } else if (yesno == 'B'){
    return false
  }
  return true
}

export default class extends Controller {
  static targets = ["explain", "yesno"];
  static values = {required: String};


  initialize(){
    let current = 'None';
    this.yesnoTargets.forEach((element) => {
      if(element.checked) current = element.value
    });
    this.explainTargets.forEach((element) => {
      element.hidden = yesnoTotruefalse(this.requiredValue, current);
    });
  }


  toggled(event){
    this.explainTargets.forEach((element) => {
      element.hidden = yesnoTotruefalse(this.requiredValue, event.target.value);
    });
  }

}
