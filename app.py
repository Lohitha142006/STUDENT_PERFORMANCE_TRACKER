from flask import Flask, render_template, request, redirect, flash
from models import db, Student, Grade

app = Flask(__name__)
app.secret_key = "studenttracker"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    students = Student.query.all()
    return render_template('index.html', students=students)


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():

    if request.method == 'POST':

        name = request.form['name']
        roll = request.form['roll']

        existing = Student.query.filter_by(
            roll_number=roll
        ).first()

        if existing:
            flash("Roll Number already exists!")
            return redirect('/add_student')

        student = Student(
            name=name,
            roll_number=roll
        )

        db.session.add(student)
        db.session.commit()

        return redirect('/')

    return render_template('add_student.html')


@app.route('/add_grades/<int:id>', methods=['GET', 'POST'])
def add_grades(id):

    student = Student.query.get(id)

    if request.method == 'POST':

        subject = request.form['subject']
        marks = float(request.form['marks'])

        if marks < 0 or marks > 100:
            flash("Marks must be between 0 and 100")
            return redirect(f'/add_grades/{id}')

        grade = Grade(
            student_id=id,
            subject=subject,
            marks=marks
        )

        db.session.add(grade)
        db.session.commit()

        return redirect('/')

    return render_template(
        'add_grades.html',
        student=student
    )


@app.route('/student/<int:id>')
def student_details(id):

    student = Student.query.get(id)

    grades = Grade.query.filter_by(
        student_id=id
    ).all()

    total = sum(g.marks for g in grades)

    average = total / len(grades) if grades else 0

    return render_template(
        'student_details.html',
        student=student,
        grades=grades,
        average=average
    )


if __name__ == '__main__':
    app.run(debug=True)