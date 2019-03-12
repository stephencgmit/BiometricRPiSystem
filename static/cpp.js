// quiz constructor

function Quiz(questions) {
    this.score = 0;
    this.questions = questions;
    this.currentQuestionIndex = 0;
}

Quiz.prototype.guess = function(answer) {
    if(this.getCurrentQuestion().isCorrectAnswer(answer)) {
        this.score++;
    }
    this.currentQuestionIndex++;
};


Quiz.prototype.getCurrentQuestion = function() {
    return this.questions[this.currentQuestionIndex];
};

Quiz.prototype.hasEnded = function() {
    return this.currentQuestionIndex >= this.questions.length;
};


// question

function Question(text, choices, answer) {
    this.text = text;
    this.choices = choices;
    this.answer = answer;
}

Question.prototype.isCorrectAnswer = function (choice) {
    return this.answer === choice;
};

// quiz ui

var QuizUI = {
    displayNext: function () {
        if (quiz.hasEnded()) {
            this.displayScore();
        } else {
            this.displayQuestion();
            this.displayChoices();
            this.displayProgress();
        }
    },
   displayQuestion: function() {
        this.populateIdWithHTML("question", quiz.getCurrentQuestion().text);
    },
   displayChoices: function() {
        var choices = quiz.getCurrentQuestion().choices;

        for(var i = 0; i < choices.length; i++) {
            this.populateIdWithHTML("choice" + i, choices[i]);
            this.guessHandler("guess" + i, choices[i]);
        }
    },

    displayScore: function() {
        var gameOverHTML = "<h1>Game Over</h1>";
        gameOverHTML += "<h2> Your score is: " + quiz.score + "</h2>";
        this.populateIdWithHTML("quiz", gameOverHTML);
    },

    populateIdWithHTML: function(id, text) {
        var element = document.getElementById(id);
        element.innerHTML = text;
    },

    guessHandler: function(id, guess) {
        var button = document.getElementById(id);
        button.onclick = function() {
            quiz.guess(guess);
            QuizUI.displayNext();
        }
    },

  displayProgress: function() {
        var currentQuestionNumber = quiz.currentQuestionIndex + 1;
        this.populateIdWithHTML("progress", "Question " + currentQuestionNumber + " of " + quiz.questions.length);
    }
};




//Create Questions
var questions = [
    new Question("C++ does not supports the following?", [ "Multilevel inheritance", "Hierarchical inheritance", "Hybrid inheritance", "None of the above"], "None of the above"),
    new Question("Which operator is required to be overloaded as member function only??", [ "_", "_ _", "++ (postfix version)", "="], "="),
    new Question("How many number of arguments can a destructor of a class receives?", [ "0", "1", "2", "None of the above"], "0"),
    new Question("Objects created using new operator are stored in __ memory.?", [ "Cache", "Heap", "Stack", "None of the above"], "Heap"),
    new Question("A C++ program statements can be commented using?", [ "Single line comment", "Multi line comment", "Either (a) or (b)", "Both (a) and (b)"], "Both (a) and (b)"),
    new Question(" i) Exception handling technically provides multi branching.\n" +
        "ii) Exception handling can be mimicked using ‘goto’ construct.", [ "Only (i) is true", "Only (ii) is true", "Both (i) & (ii) are true", "Both (i) && (ii) are false"], "Only (i) is true"),
    new Question("What is the size of ‘int’??", [ "8 bit", "4 bit", "2 bit", "Compiler dependent"], "Compiler dependent"),
    new Question("i) Exceptions can be traced and controlled using conditional statements.\n" +
        "ii) For critical exceptions compiler provides the handler", [ "Only (i) is true", "Only (ii) is true", "Both (i) & (ii) are true", "Both (i) && (ii) are false"], "Only (ii) is true"),
    new Question("In C++ the name main has ________ scope", [ "program", "standard", "local", "global"], "global"),
    new Question("Which one of the following statements best descrives the C++ programming language?", ["C++ is a low level language","C++ is a procedural programming language","C++ is a multiparadigm programming language","C++ is an object orientated language"], "C++ is a multiparadigm language")
];

//Create Quiz
var quiz = new Quiz(questions);

//Display Quiz
QuizUI.displayNext();