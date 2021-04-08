import { Controller } from "stimulus"

export default class extends Controller {
  static targets = ["text", "more"];
  static values = {required: Number};

  initialize(){
    this.requiredValue -= 1;
    this.textTargets.forEach((element, index) => {
      element.hidden = index > this.requiredValue;
      if(element.hidden && element.value != ""){
        this.requiredValue = index;
        element.hidden = false;
      }
    });
  }

  more(event){
    this.requiredValue++;
    this.textTargets.forEach((element, index) => {
      element.hidden = index > this.requiredValue
    });
  }
}
