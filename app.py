from flask import Flask
from flask import *
from models import *
import warnings

import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_name = "Grades.db"

app = Flask(__name__, static_url_path="/static", static_folder="static")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, db_name)
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

with app.app_context():
    db.create_all()


@ app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('404.html'), 404


@ app.route('/')
def static_file():
    return render_template("grades.html")


@ app.route('/grades', methods=['POST', 'GET'])
def handle_grades():
    if request.method == 'POST':
        data = request.json

        s_name = data["name"]
        s_grade = data["grade"]

        # If student in grades dict set the grade value for entry
        # to value from json
        try:
            add_student(s_name, s_grade)
            return "Success!", 200
        except ValueError:
            return f"{s_name} already exists", 409
        except Exception as e:
            warnings.warn(e)
    elif request.method == 'GET':
        return get_student_json()
    return "Method not supported", 501


@ app.route('/grades/<student_name>', methods=["GET", "PUT", "DELETE"])
def handle_grades_request(student_name):
    if request.method == 'GET':
        try:
            # Get the grade value for student
            grade = get_student_grade(student_name)
            return {student_name: grade}
        except KeyError:
            # Return that student not in dict
            return f"{student_name} does not exist", 404
        except Exception as e:
            warnings.warn(e)

    elif request.method == "PUT":
        data = request.json
        s_grade = data['grade']

        try:
            update_student(student_name, s_grade)
            return "Success!", 200
        except KeyError:
            # Return that student not in db
            return f"{student_name} does not exist", 404
        except Exception as e:
            warnings.warn(e)
    elif request.method == "DELETE":
        try:
            remove_student(student_name)
            return "Success!", 200
        except KeyError:
            # Return status that student not in db
            return f"{student_name} does not exist", 404
        except Exception as e:
            warnings.warn(e)
    return "Method not supported", 501


if __name__ == '__main__':
    app.run(debug=True)
