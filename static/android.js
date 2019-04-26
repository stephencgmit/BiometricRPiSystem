

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
        var gameOverHTML = "<h1>Quiz Over</h1>";
        var quizScore = quiz.score;
        gameOverHTML += "<h2> Your score is: " + quiz.score + "</h2>";
        this.populateIdWithHTML("quiz", gameOverHTML);
        this.populateIdWithHTML("score", quizScore);

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
    new Question("What is Pending Intent in android?", [ "It is a kind of an intent",
        "It is used to pass the data between activities",
        "It will fire at a future point of time.", "None of the Above"], "It is used to pass the data between activities"),
    new Question("What is splash screen in android?", ["Initial activity of an application","Initial service of an application",
    "Initial method of an application"," Initial screen of an application"], "Initial screen of an application"),

        new Question("What is ANR in android??", ["When the application is not responding ANR will occur.","Dialog box is called as ANR.",
    "When Android forcefully kills an application, it is called ANR"," None of the above"], "When the application is not responding ANR will occur."),

        new Question("What is sleep mode in android?", ["Only Radio interface layer and alarm are in active mode","Switched off",
    "Air plane mode"," None of the others"], "Only Radio interface layer and alarm are in active mode"),

        new Question("What is singleton class in android??", ["Anonymous class","Java class",
    "Manifest file."," A class that can create only one object"], "A class that can create only one object"),

        new Question("What is breakpoint in android?", ["Breaks the application","Breaks the development code",
    "Breaks the execution."," None of the above."], "Breaks the execution."),

        new Question("What is the library of Map View in android?", ["com.map","com.goggle.gogglemaps",
    "in.maps"," com.goggle.android.maps"], "com.goggle.android.maps"),

        new Question("Fragment in Android can be found through?", ["findByID()","findFragmentByID()",
    "getContext.findFragmentByID()","FragmentManager.findFragmentByID()"], "FragmentManager.findFragmentByID()"),

        new Question("Android deprecated version?", ["Android deprecated version","There is no value for 1",
    "Android doesn't allow min version 1"," None of the above"], "Android deprecated version"),

        new Question("What is an interface in android??", ["Interface is a class.","Interface is a layout file.",
    "Interface acts as a bridge between class and the outside world."," None of the above"], "Interface acts as a bridge between class and the outside world.")
];

//Create Quiz
var quiz = new Quiz(questions);

//Display Quiz
QuizUI.displayNext();
