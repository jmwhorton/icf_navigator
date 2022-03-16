import { Controller } from "stimulus"

export default class extends Controller {
  static targets = ["text", "score"];
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

  updateScore(){
    let score = this.getScores(this.textTarget.value);
    var newScore = this.grade(this.textTarget.value);
    let k = Math.pow(10, 2);
    newScore = Math.floor((newScore * k) + 0.5 * Math.sign(newScore)) / k;
    if(newScore > 0){
      this.scoreTarget.innerHTML = `Grade: ${score.fleschKincaidGrade} / ${newScore}`;
    } else {
      this.scoreTarget.innerHTML = '';
    }
  }

  // Taken from https://github.com/sahava/readability-score-javascript
  getScores(text) {

    /* 
     * To speed the script up, you can set a sampling rate in words. For example, if you set
     * sampleLimit to 1000, only the first 1000 words will be parsed from the input text.
     * Set to 0 to never sample.
     */     
    var sampleLimit = 1000;

    // Manual rewrite of the textstat Python library (https://github.com/shivam5992/textstat/)

    /* 
     * Regular expression to identify a sentence. No, it's not perfect. 
     * Fails e.g. with abbreviations and similar constructs mid-sentence.
     */
    var sentenceRegex = new RegExp('[.?!]\\s[^a-z]', 'g');

    /*
     * Regular expression to identify a syllable. No, it's not perfect either.
     * It's based on English, so other languages with different vowel / consonant distributions
     * and syllable definitions need a rewrite.
     * Inspired by https://bit.ly/2VK9dz1
     */
    var syllableRegex = new RegExp('[aiouy]+e*|e(?!d$|ly).|[td]ed|le$', 'g');

    // Baseline for FRE - English only
    var freBase = {
      base: 206.835,
      sentenceLength: 1.015,
      syllablesPerWord: 84.6,
      syllableThreshold: 3
    };

    var cache = {};

    var punctuation = ['!','"','#','$','%','&','\'','(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[',']','^','_','`','{','|','}','~'];

    var legacyRound = function(number, precision) {
      var k = Math.pow(10, (precision || 0));
      return Math.floor((number * k) + 0.5 * Math.sign(number)) / k;
    };

    var charCount = function(text) {
      if (cache.charCount) return cache.charCount;
      if (sampleLimit > 0) text = text.split(' ').slice(0, sampleLimit).join(' ');
      text = text.replace(/\s/g, '');
      return cache.charCount = text.length;
    };

    var removePunctuation = function(text) {
      return text.split('').filter(function(c) {
        return punctuation.indexOf(c) === -1;
      }).join('');
    };

    var letterCount = function(text) {
      if (sampleLimit > 0) text = text.split(' ').slice(0, sampleLimit).join(' ');
      text = text.replace(/\s/g, '');
      return removePunctuation(text).length;
    };

    var lexiconCount = function(text, useCache, ignoreSample) {
      if (useCache && cache.lexiconCount) return cache.lexiconCount;
      if (ignoreSample !== true && sampleLimit > 0) text = text.split(' ').slice(0, sampleLimit).join(' ');
      text = removePunctuation(text);
      var lexicon = text.split(' ').length;
      return useCache ? cache.lexiconCount = lexicon : lexicon;
    };

    var getWords = function(text, useCache) {
      if (useCache && cache.getWords) return cache.getWords;
      if (sampleLimit > 0) text = text.split(' ').slice(0, sampleLimit).join(' ');
      text = text.toLowerCase();
      text = removePunctuation(text);
      var words = text.split(' ');
      return useCache ? cache.getWords = words : words;
    }

    var syllableCount = function(text, useCache) {
      if (useCache && cache.syllableCount) return cache.syllableCount;
      var count = 0;
      var syllables = getWords(text, useCache).reduce(function(a, c) {  
        return a + (c.match(syllableRegex) || [1]).length;
      }, 0);
      return useCache ? cache.syllableCount = syllables : syllables;
    };

    var polySyllableCount = function(text, useCache) {
      var count = 0;
      getWords(text, useCache).forEach(function(word) {
        var syllables = syllableCount(word);
        if (syllables >= 3) {
          count += 1;
        }
      });
      return count;
    };

    var sentenceCount = function(text, useCache) {
      if (useCache && cache.sentenceCount) return cache.sentenceCount;
      if (sampleLimit > 0) text = text.split(' ').slice(0, sampleLimit).join(' ');
      var ignoreCount = 0;
      var sentences = text.split(sentenceRegex);
      sentences.forEach(function(s) {
        if (lexiconCount(s, true, false) <= 2) { ignoreCount += 1; }
      });
      var count = Math.max(1, sentences.length - ignoreCount);
      return useCache ? cache.sentenceCount = count : count;
    };

    var avgSentenceLength = function(text) {
      var avg = lexiconCount(text, true) / sentenceCount(text, true);
      return legacyRound(avg, 2);
    };

    var avgSyllablesPerWord = function(text) {
      var avg = syllableCount(text, true) / lexiconCount(text, true);
      return legacyRound(avg, 2);
    };

    var avgCharactersPerWord = function(text) {
      var avg = charCount(text) / lexiconCount(text, true);
      return legacyRound(avg, 2);
    };

    var avgLettersPerWord = function(text) {
      var avg = letterCount(text, true) / lexiconCount(text, true);
      return legacyRound(avg, 2);
    };

    var avgSentencesPerWord = function(text) {
      var avg = sentenceCount(text, true) / lexiconCount(text, true);
      return legacyRound(avg, 2);
    };

    var fleschReadingEase = function(text) {
      var sentenceLength = avgSentenceLength(text);
      var syllablesPerWord = avgSyllablesPerWord(text);
      return legacyRound(
        freBase.base - 
        freBase.sentenceLength * sentenceLength - 
        freBase.syllablesPerWord * syllablesPerWord,
        2
      );
    };

    var fleschKincaidGrade = function(text) {
      var sentenceLength = avgSentenceLength(text);
      var syllablesPerWord = avgSyllablesPerWord(text);
      return legacyRound(
        0.39 * sentenceLength +
        11.8 * syllablesPerWord -
        15.59,
        2
      );
    };

    var smogIndex = function(text) {
      var sentences = sentenceCount(text, true);
      if (sentences >= 3) {
        var polySyllables = polySyllableCount(text, true);
        var smog = 1.043 * (Math.pow(polySyllables * (30 / sentences), 0.5)) + 3.1291;
        return legacyRound(smog, 2);
      }
      return 0.0;
    };

    var colemanLiauIndex = function(text) {
      var letters = legacyRound(avgLettersPerWord(text) * 100, 2);
      var sentences = legacyRound(avgSentencesPerWord(text) * 100, 2);
      var coleman = 0.0588 * letters - 0.296 * sentences - 15.8;
      return legacyRound(coleman, 2);
    };

    var automatedReadabilityIndex = function(text) {
      var chars = charCount(text);
      var words = lexiconCount(text, true);
      var sentences = sentenceCount(text, true);
      var a = chars / words;
      var b = words / sentences;
      var readability = (
        4.71 * legacyRound(a, 2) +
        0.5 * legacyRound(b, 2) -
        21.43
      );
      return legacyRound(readability, 2); 
    };

    var linsearWriteFormula = function(text) {
      var easyWord = 0;
      var difficultWord = 0;
      var roughTextFirst100 = text.split(' ').slice(0,100).join(' ');
      var plainTextListFirst100 = getWords(text, true).slice(0,100);
      plainTextListFirst100.forEach(function(word) {
        if (syllableCount(word) < 3) {
          easyWord += 1;
        } else {
          difficultWord += 1;
        }
      });
      var number = (easyWord + difficultWord * 3) / sentenceCount(roughTextFirst100);
      if (number <= 20) {
        number -= 2;
      }
      return legacyRound(number / 2, 2);
    };

    var rix = function(text) {
      var words = getWords(text, true);
      var longCount = words.filter(function(word) {
        return word.length > 6;
      }).length;
      var sentencesCount = sentenceCount(text, true);
      return legacyRound(longCount / sentencesCount, 2);
    };

    var readingTime = function(text) {
      var wordsPerSecond = 4.17;
      // To get full reading time, ignore cache and sample
      return legacyRound(lexiconCount(text, false, true) / wordsPerSecond, 2);
    };

    // Build textStandard
    var grade = [];
    var obj = {};
    (function() {

      // FRE
      var fre = obj.fleschReadingEase = fleschReadingEase(text);
      if (fre < 100 && fre >= 90) {
        grade.push(5);
      } else if (fre < 90 && fre >= 80) {
        grade.push(6);
      } else if (fre < 80 && fre >= 70) {
        grade.push(7);
      } else if (fre < 70 && fre >= 60) {
        grade.push(8);
        grade.push(9);
      } else if (fre < 60 && fre >= 50) {
        grade.push(10);
      } else if (fre < 50 && fre >= 40) {
        grade.push(11);
      } else if (fre < 40 && fre >= 30) {
        grade.push(12);
      } else {
        grade.push(13);
      }

      // FK
      var fk = obj.fleschKincaidGrade = fleschKincaidGrade(text);
      grade.push(Math.floor(fk));
      grade.push(Math.ceil(fk));

      // SMOG
      var smog = obj.smogIndex = smogIndex(text);
      grade.push(Math.floor(smog));
      grade.push(Math.ceil(smog));

      // CL
      var cl = obj.colemanLiauIndex = colemanLiauIndex(text);
      grade.push(Math.floor(cl));
      grade.push(Math.ceil(cl));

      // ARI
      var ari = obj.automatedReadabilityIndex = automatedReadabilityIndex(text);
      grade.push(Math.floor(ari));
      grade.push(Math.ceil(ari));

      // LWF
      var lwf = obj.linsearWriteFormula = linsearWriteFormula(text);
      grade.push(Math.floor(lwf));
      grade.push(Math.ceil(lwf));

      // RIX
      var rixScore = obj.rix = rix(text);
      if (rixScore >= 7.2) {
        grade.push(13);
      } else if (rixScore < 7.2 && rixScore >= 6.2) {
        grade.push(12);
      } else if (rixScore < 6.2 && rixScore >= 5.3) {
        grade.push(11);
      } else if (rixScore < 5.3 && rixScore >= 4.5) {
        grade.push(10);
      } else if (rixScore < 4.5 && rixScore >= 3.7) {
        grade.push(9);
      } else if (rixScore < 3.7 && rixScore >= 3.0) {
        grade.push(8);
      } else if (rixScore < 3.0 && rixScore >= 2.4) {
        grade.push(7);
      } else if (rixScore < 2.4 && rixScore >= 1.8) {
        grade.push(6);
      } else if (rixScore < 1.8 && rixScore >= 1.3) {
        grade.push(5);
      } else if (rixScore < 1.3 && rixScore >= 0.8) {
        grade.push(4);
      } else if (rixScore < 0.8 && rixScore >= 0.5) {
        grade.push(3);
      } else if (rixScore < 0.5 && rixScore >= 0.2) {
        grade.push(2);
      } else {
        grade.push(1);
      }

      // Find median grade
      grade = grade.sort(function(a, b) { return a - b; });
      var midPoint = Math.floor(grade.length / 2);
      var medianGrade = legacyRound(
        grade.length % 2 ? 
        grade[midPoint] : 
        (grade[midPoint-1] + grade[midPoint]) / 2.0
      );
      obj.medianGrade = medianGrade;

    })();

    obj.readingTime = readingTime(text);

    return obj;
  };

  // Taken from https://github.com/dana-ross/flesch-kincaid
  syllables(x) {
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
    return (x.split(/\s+/) || ['']).length;
  };

  sentences(x) {
    return (x.split('. ') || ['']).length;
  };

  syllablesPerWord(x) {
    return this.syllables(x) / this.words(x);
  };

  wordsPerSentence(x) {
    return this.words(x) / this.sentences(x);
  };

  rate(x) {
    return 206.835 - 1.015 * this.wordsPerSentence(x) - 84.6 * this.syllablesPerWord(x);
  };

  grade(x) {
    return 0.39 * this.wordsPerSentence(x) + 11.8 * this.syllablesPerWord(x) - 15.59;
  };
}
