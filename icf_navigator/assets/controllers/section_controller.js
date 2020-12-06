import { Controller } from "stimulus"

export default class extends Controller {
  static targets = ["qgroup"];
  static values = { index: Number }

  next() {
    this.indexValue++;
  }

  previous(){
    this.indexValue--;
  }

  indexValueChanged(){
    if(this.indexValue < 0 && this.qgroupTargets.length > 0){
      this.indexValue = this.qgroupTargets.length - 1
    }
    this.indexValue = this.indexValue % this.qgroupTargets.length;
    this.showCurrentQGroup();
  }

  showCurrentQGroup(){
    this.qgroupTargets.forEach((element, index) => {
      element.hidden = index != this.indexValue
    });
  }
}
