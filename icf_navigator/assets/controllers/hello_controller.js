import { Controller } from "stimulus"

export default class extends Controller {
  static targets = [ "name" ];

  initialize() {
    console.log("alive");
  }

  initialize() {
    console.log("connect");
  }

  greet() {
    alert(`Hello, ${this.name}`);
  }

  get name(){
    return this.nameTarget.value
  }
}
