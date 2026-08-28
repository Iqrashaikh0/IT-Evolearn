from flask import Flask, render_template, request, redirect, url_for, flash, session
import markdown
import os
from dotenv import load_dotenv

# =========================================================
# AI MODULES
# =========================================================

from ai.generatenotes import generate_notes
from ai.generatequiz import generate_quiz
from ai.askai import ask_ai_response
from ai.recommendation import generate_recommendation


# =========================================================
# ENVIRONMENT
# =========================================================

basedir = os.path.abspath(os.path.dirname(__file__))

dotenv_path = os.path.join(
    basedir,
    ".env"
)

load_dotenv(dotenv_path)


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)

app.secret_key = os.getenv(
    "FLASK_SECRET_KEY",
    "it-evolearn-secret-key"
)


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route("/login")
def login():

    return render_template(
        "login.html"
    )


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        level = request.form.get("level")
        password = request.form.get("password")
        confirm_password = request.form.get(
            "confirm_password"
        )

        if password != confirm_password:

            flash(
                "Passwords do not match."
            )

            return redirect(
                url_for("register")
            )

        flash(
            "Registration successful! You can now login."
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html"
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    return render_template(
        "dashboard.html"
    )


# =========================================================
# SECONDARY
# =========================================================

@app.route("/secondary")
def secondary():

    return render_template(
        "secondary/secondary.html"
    )


@app.route("/computerbasics")
def computerbasics():

    return render_template(
        "secondary/computerbasics.html"
    )


@app.route("/msword")
def msword():

    return render_template(
        "secondary/msword.html"
    )


@app.route("/scratch")
def scratch():

    return render_template(
        "secondary/scratch.html"
    )


@app.route("/htmlcss")
def htmlcss():

    return render_template(
        "secondary/htmlcss.html"
    )


@app.route("/python")
def python():

    return render_template(
        "secondary/python.html"
    )


@app.route("/internetsafety")
def internetsafety():

    return render_template(
        "secondary/internetsafety.html"
    )


# =========================================================
# JUNIOR
# =========================================================

@app.route("/junior")
def junior():

    return render_template(
        "junior/junior.html"
    )


@app.route("/junior/cprogramming")
def cprogramming():

    return render_template(
        "junior/cprogramming.html"
    )


@app.route("/junior/dbms")
def dbms():

    return render_template(
        "junior/dbms.html"
    )


@app.route("/junior/ai")
def ai():

    return render_template(
        "junior/ai.html"
    )


@app.route("/junior/robotics")
def robotics():

    return render_template(
        "junior/robotics.html"
    )


@app.route("/junior/cyber")
def cyber():

    return render_template(
        "junior/cyber.html"
    )


@app.route("/junior/computernetwork")
def computernetwork():

    return render_template(
        "junior/computernetwork.html"
    )


# =========================================================
# DEGREE
# =========================================================

@app.route("/degree")
def degree():

    return render_template(
        "degree/degree.html"
    )


@app.route("/cloud")
def cloud():

    return render_template(
        "degree/cloud.html"
    )


@app.route("/datastructure")
def datastructure():

    return render_template(
        "degree/datastructure.html"
    )


@app.route("/java")
def java():

    return render_template(
        "degree/java.html"
    )


@app.route("/webdevelopment")
def webdevelopment():

    return render_template(
        "degree/webdevelopment.html"
    )


@app.route("/operatingsystems")
def operatingsystems():

    return render_template(
        "degree/operatingsystems.html"
    )


@app.route("/softwareengineering")
def softwareengineering():

    return render_template(
        "degree/softwareengineering.html"
    )


# =========================================================
# POST GRADUATION
# =========================================================

@app.route("/pg")
def pg():

    return render_template(
        "pg/pg.html"
    )


@app.route("/pg/aai")
def aai():

    return render_template(
        "pg/aai.html"
    )


@app.route("/pg/acn")
def acn():

    return render_template(
        "pg/acn.html"
    )


@app.route("/pg/acs")
def acs():

    return render_template(
        "pg/acs.html"
    )


@app.route("/pg/bigdata")
def bigdata():

    return render_template(
        "pg/bigdata.html"
    )


@app.route("/pg/ml")
def ml():

    return render_template(
        "pg/ml.html"
    )


@app.route("/pg/nlp")
def nlp():

    return render_template(
        "pg/nlp.html"
    )


# =========================================================
# AI NOTES
# =========================================================

@app.route("/notes/<chapter>")
def notes(chapter):

    notes = generate_notes(
        chapter
    )

    notes_html = markdown.markdown(
        notes,
        extensions=[
            "fenced_code",
            "tables"
        ]
    )

    return render_template(
        "notes.html",
        chapter=chapter,
        notes=notes_html
    )


# =========================================================
# AI QUIZ
# =========================================================

@app.route(
    "/quiz/<chapter>",
    methods=["GET", "POST"]
)
def quiz(chapter):

    # =====================================================
    # GET REQUEST
    # Generate quiz only ONCE
    # =====================================================

    if request.method == "GET":

        questions = generate_quiz(
            chapter
        )

        # If quiz generation fails
        if not questions:

            return render_template(
                "result.html",
                score=0,
                total=0,
                percentage=0,
                chapter=chapter,
                results=[],
                error="Unable to generate quiz. Please try again."
            )

        # Save generated quiz in session
        session["quiz_questions"] = questions
        session["quiz_chapter"] = chapter

        return render_template(
            "quiz.html",
            chapter=chapter,
            questions=questions
        )


    # =====================================================
    # POST REQUEST
    # Use SAME questions from session
    # =====================================================

    questions = session.get(
        "quiz_questions",
        []
    )


    saved_chapter = session.get(
        "quiz_chapter",
        chapter
    )


    # If session quiz is missing
    if not questions:

        return redirect(
            url_for(
                "quiz",
                chapter=chapter
            )
        )


    # =====================================================
    # CALCULATE SCORE
    # =====================================================

    score = 0

    results = []


    for i, question in enumerate(
        questions,
        start=1
    ):

        # Student answer
        user_answer = request.form.get(
            f"q{i}",
            ""
        ).strip()


        # Correct answer
        correct_answer = str(
            question.get(
                "answer",
                ""
            )
        ).strip()


        # Check answer
        is_correct = (
            user_answer == correct_answer
        )


        if is_correct:

            score += 1


        # Store result for result page
        results.append({

            "question": question.get(
                "question",
                ""
            ),

            "user_answer": user_answer,

            "correct_answer": correct_answer,

            "is_correct": is_correct

        })


    # =====================================================
    # TOTAL
    # =====================================================

    total = len(
        questions
    )


    # =====================================================
    # PERCENTAGE
    # =====================================================

    if total > 0:

        percentage = round(
            (score / total) * 100
        )

    else:

        percentage = 0


    # =====================================================
    # CLEAR OLD QUIZ
    # =====================================================

    session.pop(
        "quiz_questions",
        None
    )

    session.pop(
        "quiz_chapter",
        None
    )


    # =====================================================
    # RESULT PAGE
    # =====================================================

    return render_template(
        "result.html",

        score=score,

        total=total,

        percentage=percentage,

        chapter=saved_chapter,

        results=results,

        error=None
    )


# =========================================================
# ASK AI
# =========================================================

@app.route(
    "/askai/<chapter>",
    methods=["GET", "POST"]
)
def askai(chapter):

    answer = ""


    if request.method == "POST":

        question = request.form.get(
            "question",
            ""
        )


        if question:

            answer = ask_ai_response(
                chapter,
                question
            )


            answer = markdown.markdown(
                answer,
                extensions=[
                    "fenced_code",
                    "tables"
                ]
            )


    return render_template(
        "askai.html",
        chapter=chapter,
        answer=answer
    )


# =========================================================
# AI RECOMMENDATION
# =========================================================

@app.route(
    "/recommendation/<chapter>"
)
def recommendation(chapter):

    score = request.args.get(
        "score",
        0
    )


    recommendation_text = generate_recommendation(
        chapter,
        score
    )


    recommendation_html = markdown.markdown(
        recommendation_text,
        extensions=[
            "fenced_code"
        ]
    )


    return render_template(
        "recommendation.html",
        chapter=chapter,
        recommendation=recommendation_html
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

