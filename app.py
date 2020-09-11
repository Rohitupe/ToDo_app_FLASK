# from flask import Flask, render_template, url_for
#
# app = Flask(__name__)
#
# @app.route('/')
# def Home():
#     return render_template('index.html')
#
# if __name__ == '__main__':
#     app.run(debug=True)

"""Now work with sql alchemy"""

from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# /// 3 slaches relative path ,  //// 4 slashes absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# This class is to create database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200),nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime,default=datetime.now())

    def __repr__(self):
        return f"Task Created With ID {self.id}"


@app.route('/',methods=['POST','GET'])
def homePage():
    if request.method == "POST":
        taskContent = request.form['content']  # content form request
        taskInput = Todo(content = taskContent)
        print((taskInput))
        print((taskContent))
        try :
            db.session.add(taskInput)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue"

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')
def deleteTask(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Task YOu Want To delete not Found"

@app.route('/update/<int:id>',methods=['GET','POST'])
def updateTask(id):
    tasks = Todo.query.get_or_404(id)

    if request.method == "POST":
        tasks.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Update Fail"
    else:
        return render_template('update.html',tasks=tasks)

if __name__ == '__main__':
    app.run()
