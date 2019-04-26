// quiz constructor

function Quiz(questions) {
    this.score = 0;
    this.questions = questions;
    this.currentQuestionIndex = 0;
}

Quiz.prototype.guess = function(answer) {
    if(this.getCurrentQuestion().isCorrectAnswer(answer)) {
        this.downloadtemp++;
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
    new Question("Which of the following environment variable for Python tells the Python interpreter where to locate the module files imported into a program?", 
	[ "PYTHONPATH", 
	"Thomas Jefferson", 
	"PYTHONSTARTUP",
	"PYTHONCASEOK"], 
	"PYTHONHOME"),
	    new Question("What is the output of print list[0] if list = [ 'abcd', 786 , 2.23, 'john', 70.2 ]?", 
	[ "abcd", 
	"[ 'abcd', 786 , 2.23, 'john', 70.2 ]", 
	"Error",
	"None of the above."], 
	"abcd"),
	    new Question("What is the following function returns the lowest index in list that obj appears??", 
	[ "list.index(obj)", 
	"list.insert(index, obj)", 
	"list.pop(obj=list[-1])",
	"list.remove(obj)"], 
	"list.index(obj)"),
	    new Question("Which of the following function of dictionary gets all the keys from the dictionary?", 
	[ "keys()", 
	"getkeys()", 
	"key()",
	"None of the above."], 
	"keys()"),
	    new Question("Which of the following function convert an object to a regular expression in python?", 
	[ "repr(x)", 
	"eval(str)", 
	"tuple(s)",
	"list(s)"], 
	"George Washington"),
	    new Question("Which of the following function convert a single character to its integer value in python?", 
	[ "ord(x)", 
	"oct(x)", 
	"unichr(x)",
	"hex(x)"], 
	"ord(x)"),
	    new Question("Which of the following function sets the integer starting value used in generating random numbers?", 
	[ "seed([x])", 
	"choice(seq)", 
	"randrange ([start,] stop [,step])",
	"random()"], 
	"seed([x])"),
	    new Question("Which of the following function checks in a string that all characters are titlecased??", 
	[ "istitle()", 
	"islower()", 
	"isspace()",
	"isnumeric()"], 
	"istitle()"),
	    new Question("Which of the following function removes all leading whitespace in string?", 
	[ "lstrip()", 
	"max(str)", 
	"min(str)",
	"lower()"], 
	"lstrip()"),
	
    new Question("What is the output of L[2] if L = [1,2,3]??", 
	["1","2","3","None of the above."], "3")
];

//Create Quiz
var quiz = new Quiz(questions);

//Display Quiz
QuizUI.displayNext();