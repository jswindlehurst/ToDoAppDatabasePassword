from flask import Flask, render_template, request, redirect, make_response, url_for
from model import ToDo, db
import uuid
import hashlib
import datetime

app = Flask(__name__)
db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    session_token = request.cookies.get("session_token")
    if session_token:

        user = db.query(ToDo).filter_by(session_token=session_token).first()

    else:
        user = None

    return render_template("index.html", user=user)


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")
    password = request.form.get("user-password")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    content = "Welcome User"
    date = datetime.datetime.now()


    user = db.query(ToDo).filter_by(email=email).first()

    if not user:
        user = ToDo(name=name, email=email, password=hashed_password, content=content, date=date)
        db.add(user)
        db.commit()

    if hashed_password != user.password:
        return "Wrong Password"
    else:
        session_token = str(uuid.uuid4())
        user.session_token = session_token

        db.add(user)
        db.commit()

        response = make_response(redirect("/task"))
        response.set_cookie("session_token", session_token, httponly=True, samesite='Strict')

        return response

@app.route("/task", methods=["GET", "POST"])
def task():
    session = request.cookies.get("session_token")
    user = db.query(ToDo).filter_by(session_token=session).first()
    name = user.name

    if request.method == "POST":
        task_content = request.form.get("content")
        new_content = ToDo(name=name, content=task_content)

        db.add(new_content)
        db.commit()

        return redirect("/task")
    else:
        tasks = db.query(ToDo).filter_by(name=name).all()
        return render_template("task.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = db.query(ToDo).get(id)

    db.delete(task_to_delete)
    db.commit()

    return redirect("/task")



@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    task_to_edit = db.query(ToDo).get(id)

    if request.method == "POST":
        task_to_edit.content = request.form.get("new-content")
        db.commit()
        return redirect("/task")
    else:

        return render_template("edit.html", task_to_edit=task_to_edit)

@app.route("/logout", methods=["GET", "POST"])
def logout():

    session_token = ""

    response = make_response(redirect(url_for('index')))
    response.set_cookie("session_token", session_token)


    return response


if __name__ == '__main__':
    app.run(port=5004)