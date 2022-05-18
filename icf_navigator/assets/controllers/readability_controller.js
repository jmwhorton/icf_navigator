import { Controller } from "stimulus"

export default class extends Controller {
  static targets = ["text", "score", "sentence", "syllable"];
  static values = { score: Number }

  connect() {
    if(this.hasTextTarget){
      this.updateScore();
    }
  }

  change() {
    if(this.hasTextTarget){
      this.updateScore();
    }
  }

  round(n){
    let k = Math.pow(10, 2);
    return Math.floor((n * k) + 0.5 * Math.sign(n)) / k;
  }

  updateScore(){
    // let score = this.getScores(this.textTarget.textContent);
    let text = this.textTarget.textContent;
    var grade = this.fkGrade(text);
    var score = this.fkRate(text);
    let smog = this.smogIndex(text);
    console.log(smog);
    score = this.round(score);
    grade = this.round(grade);
    if(grade > 0){
      this.scoreTarget.innerHTML = `Grade: ${grade} / Score: ${score}`;
      if(score > 70) {
        this.scoreTarget.style.color = 'black';
      } else if(score > 60){
        this.scoreTarget.style.color = 'gold';
      } else {
        this.scoreTarget.style.color = 'red';
      }
    } else {
      this.scoreTarget.innerHTML = '';
    }
    let sentenceCount = this.sentences(text).length;
    this.sentenceTarget.innerHTML = `Sentences: ${sentenceCount}`;
    let polySyllableCount = this.polySyllableCount(text);
    this.syllableTarget.innerHTML = `Polysyllables: ${polySyllableCount}`;
  }

  // Taken from https://github.com/dana-ross/flesch-kincaid
  syllableCount(x) {
    /*
     * basic algortithm: each vowel-group indicates a syllable, except for: final
     * (silent) e 'ia' ind two syl @AddSyl and @SubSyl list regexps to massage the
     * basic count. Each match from @AddSyl adds 1 to the basic count, each
     * @SubSyl match -1 Keep in mind that when the regexps are checked, any final
     * 'e' will have been removed, and all '\'' will have been removed.
     */
    var subSyl = [/cial/, /tia/, /cius/, /cious/, /giu/, // belgium!
    /ion/, /iou/, /sia$/, /.ely$/, // absolutely! (but not ely!)
    /sed$/];

    var addSyl = [/ia/, /riet/, /dien/, /iu/, /io/, /ii/, /[aeiouym]bl$/, // -Vble, plus -mble
    /[aeiou]{3}/, // agreeable
    /^mc/, /ism$/, // -isms
    /([^aeiouy])\1l$/, // middle twiddle battle bottle, etc.
    /[^l]lien/, // // alien, salient [1]
    /^coa[dglx]./, // [2]
    /[^gq]ua[^auieo]/, // i think this fixes more than it breaks
    /dnt$/];

    // (comments refer to titan's /usr/dict/words)
    // [1] alien, salient, but not lien or ebbullient...
    // (those are the only 2 exceptions i found, there may be others)
    // [2] exception for 7 words:
    // coadjutor coagulable coagulate coalesce coalescent coalition coaxial

    var xx = x.toLowerCase().replace(/'/g, '').replace(/e\b/g, '');
    var scrugg = xx.split(/[^aeiouy]+/).filter(Boolean); // '-' should be perhaps added?

    return undefined === x || null === x || '' === x ? 0 : 1 === xx.length ? 1 : subSyl.map(function (r) {
        return (xx.match(r) || []).length;
    }).reduce(function (a, b) {
        return a - b;
    }) + addSyl.map(function (r) {
        return (xx.match(r) || []).length;
    }).reduce(function (a, b) {
        return a + b;
    }) + scrugg.length - (scrugg.length > 0 && '' === scrugg[0] ? 1 : 0) +
    // got no vowels? ("the", "crwth")
    xx.split(/\b/).map(function (x) {
        return x.trim();
    }).filter(Boolean).filter(function (x) {
        return !x.match(/[.,'!?]/g);
    }).map(function (x) {
        return x.match(/[aeiouy]/) ? 0 : 1;
    }).reduce(function (a, b) {
        return a + b;
    });
  };

  words(x) {
    x = x.split('\n').map(t => t.trim()).filter(line => line.length > 0).join(' ');
    return (x.split(/\s+/) || ['']);
  };

  sentences(x) {
    x = x.split('\n').map(t => t.trim()).filter(line => line.length > 0).join('. ');
    let sentenceRegex = new RegExp('[.?!]\\s[^a-z]', 'g');
    console.log(x);
    console.log(x.split(sentenceRegex));
    return (x.split(sentenceRegex) || ['']);
  };

  polySyllableCount(x) {
    var count = 0;
    for(let word of this.words(x)){
      if(this.syllableCount(word) >= 3){
        count += 1;
      }
    }
    return count;
  };

  syllablesPerWord(x) {
    return this.syllableCount(x) / this.words(x).length;
  };

  wordsPerSentence(x) {
    return this.words(x).length / this.sentences(x).length;
  };

  letterCount(x) {
    return this.words(x).replace(/\s+/g, '').length;
  };

  lettersPerWord(x) {
    let letterCount = this.letterCount(x);
    let wordCount = this.words(x).length;
    if(wordCount > 0){
      return letterCount / wordCount;
    } else {
      return 0;
    }
  };

  sentencePerWord(x) {
    let sentences = this.sentences(x).length;
    let words = this.words(x).length;
    if(wordCount > 0){
      return sentences / words;
    } else {
      return 0;
    }
  };

  fkRate(x) {
    console.log(`Syllables: ${this.syllableCount(x)}`);
    console.log(`Words: ${this.words(x).length}`);
    console.log(`Sentences: ${this.sentences(x).length}`);
    return 206.835 - 1.015 * this.wordsPerSentence(x) - 84.6 * this.syllablesPerWord(x);
  };

  fkGrade(x) {
    return 0.39 * this.wordsPerSentence(x) + 11.8 * this.syllablesPerWord(x) - 15.59;
  };

  smogIndex(x) {
    let sentences = this.sentences(x).length;
    let pollySyllables = this.polySyllableCount(x);
    let smog = 1.043 * (Math.pow(pollySyllables * (30 / sentences), 0.5)) + 3.1291;
    return smog;
  };

  clIndex(x) {
    let lettersPerWord = this.lettersPerWord(x) * 100;
    let sentencesPerWord = this.sentencesPerWord(x) * 100;
    let coleman = 0.0588 * lettersPerWord - 0.296 * sentences - 15.8;
    return coleman;
  };
}
