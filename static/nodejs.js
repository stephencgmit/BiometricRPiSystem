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
    new Question("In which of the following areas, Node.js is perfect to use?", 
	[ "I/O bound Applications", "Data Streaming Applications", "Data Intensive Realtime Applications (DIRT)", "All of the above."], 
	"All of the above."),
    new Question("By default, npm installs any dependency in the global mode.", 
	["false","true", "maybe", "depends"], "false"),
	new Question("Which of the following is true about EventEmitter.emit property?", 
	[ "emit property is used to fire an event.", "emit property is used to locate an event handler.", "emit property is used to bind a function with the event.", "None of the above."], 
	"emit property is used to fire an event."),
    new Question("Which method of fs module is used to write a file?", 
	["fs.writeFile(path, flags[, mode], callback)","fs.write(path, flags[, mode], callback)", 
	"fs.writePath(path, flags[, mode], callback)", "None of the above."], "fs.writeFile(path, flags[, mode], callback)"),
    new Question("Which method of fs module is used to delete a file?", 
	[ "fs.delete(fd, len, callback)", "fs.remove(fd, len, callback)", "fs.unlink(path, callback)", "None of the above."], "fs.unlink(path, callback)"),
    new Question("Which of the following code prints process version??", 
	["console.log('Current version: ' + process.version);",
	"console.log('Current version: ' + process.getVersion());", 
	"console.log('Current version: ' + process.version());", 
	"None of above"], "console.log('Current version: ' + process.version);"),
	new Question("Which of the following is the correct way to get an absolute path??", 
	[ "os.resolve('main.js')", "path.resolve('main.js')", "fs.resolve('main.js')", "None"], "path.resolve('main.js')"),
    new Question("net.isIP(input) returns 6 for IP version 6 addresses.", 
	["Depends","True", "False", "T"], "True"),
	new Question("Which of the following is true about fork methd of child_process module.", 
	[ "The fork() method method is a special case of the spawn() to create Node processes.", 
	"The fork method returns object with a built-in communication channel in addition to having all the methods in a normal ChildProcess instance.", 
	"Both of the above.", 
	"None of the above."], 
	"Both of the above."),
    new Question("A stream fires error event when there is any error receiving or writing data?", 
	["false","true", "depends", "depends"], "true")];

//Create Quiz
var quiz = new Quiz(questions);

//Display Quiz
QuizUI.displayNext();