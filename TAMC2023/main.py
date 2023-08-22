import os, random, datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


cur_dir=os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(cur_dir, "tamc2023.sqlite3")
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

class Student(db.Model):
	__tablename__= "student"
	roll_no = db.Column(db.Integer, primary_key=True)
	student_name = db.Column(db.String, nullable=False)
	parent_name = db.Column(db.String, nullable=False)
	email = db.Column(db.String, unique=True)
	grade = db.Column(db.Integer, nullable=False)
	school = db.Column(db.Text, nullable=False)
	contact = db.Column(db.String, nullable=False)
	address = db.Column(db.Text, nullable=False)
	time = db.Column(db.String, nullable=False)
	date = db.Column(db.String, nullable=False)

db.create_all()

@app.route('/', methods = ['GET', 'POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html')

@app.route('/honour_code', methods = ['GET', 'POST'])
def honour_code():
	if request.method == 'GET':
		return render_template('honour_code.html')
	if request.method == 'POST':
		#flag = True
		for value in request.form.keys():
			if request.form[value] != "ok":
				return render_template('honour_code.html')
		return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register():
    form = request.form
    try:
        student = Student(
            roll_no=int(form["phone"][-3:] + datetime.datetime.now().strftime("%H%S")[-3:]),
            student_name=form["name"],
            parent_name=form["parentsName"],
            email=form["email"],
            grade=int(form["class"]),
            school=form["school"],
            contact=form["phone"],
            address=form["address"],
            time=datetime.datetime.now().strftime("%H:%M"),
            date=datetime.datetime.now().strftime("%d-%m-%y")
        )
        db.session.add(student)
        db.session.commit()
        return render_template('hall_ticket.html', student=student)
    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route('/check_registration', methods = ['GET', 'POST'])
def check_registration():
	if request.method == 'GET':
		return render_template('check_registration.html')
	if request.method == 'POST':
		try:
			form = request.form
			user = db.session.execute(db.select(Student).filter_by(roll_no = int(form["roll_no"]))).scalar_one()
			return render_template('hall_ticket.html', student = user)
		except:
			return '<title>Not Registered</title><h4>You are not registered</h4>'


if __name__ == '__main__':
	app.run()