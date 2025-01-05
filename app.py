from student_class import Student, create_list_of_students
from flask import Flask, render_template, request, send_file
from tabulate import tabulate
import os

app = Flask(__name__)

students = {}
list_of_students = {} #When importing from a file

@app.route("/")
def home():
    global students
    students = {}
    return render_template('home.html')


@app.route('/import_file', methods=['POST','GET'])
def import_file():

    successful_import = False

    if request.method == 'POST':
        finish = request.form.get('finish')
        if finish:
            pass

        try:
            if 'file' not in request.files or request.files['file'] == '':
                raise RuntimeError("Error, no file selected or empty file has been submitted")
            
            file = request.files['file']
            if not file.filename.endswith('.txt'):
                raise RuntimeError("Error, no text file submitted")
            
            content=file.read()
            decoded_content = content.decode('UTF-8')
            
            global list_of_students
            list_of_students = create_list_of_students(decoded_content)
            successful_import = True

            return render_template("import_file.html", students=list_of_students, successful_import=successful_import)


        except RuntimeError as e:
            return render_template('import_file.html', error_message=str(e))
    
    else:

        return render_template("import_file.html")  
    

@app.route('/file_imported', methods=['GET', 'POST'])
def file_sucess():
    try:
        weights = request.form.get('custom_weights')
        weights = weights.strip()
        if weights != "":
            weights_list = [(float(weight)/100) for weight in weights.split(" ")]
        else:
                weights_list = []

        global list_of_students
        global students
        for s in list_of_students.values():
            students[s["name"]] = Student(s["name"], s["UID"], s["DOB"], s["List of grades"], None, 'module', weights_list)
            students[s["name"]].get_age()
            students[s["name"]].get_rawScore()
            students[s["name"]].get_roundedScore()
            students[s["name"]].get_category()

        return render_template("end.html", students=students)
        # return f"<p>{weights_list}, {len(weights_list)} match my freak</p>"
    except ValueError as e:
        return render_template("import_file.html", error_message = str(e))
        
@app.route('/input', methods=['POST','GET'])
def input():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            UID = request.form.get('UID')
            DOB = request.form.get('DOB')
            grades = request.form.get('grades')
            grades_list = [int(grade) for grade in grades.split() if grade.strip()]
            user_choice = request.form.get('user_choice')
            module_name = request.form.get('module_name')
            weights = request.form.get('weights')
            weights = weights.strip()
            if weights != "":
                weights_list = [(float(weight)/100) for weight in weights.split(" ")]
            else:
                 weights_list = []
            

            students[name] = Student(name, UID, DOB, grades_list, user_choice, module_name, weights_list)

            students[name].get_age()
            students[name].get_rawScore()
            students[name].get_roundedScore()
            students[name].get_category()
            
            end_it = request.form.get('end_it')

            if end_it == "next":
                return render_template("input.html")
            elif end_it == "end":
                return render_template("end.html", students=students)
            else:
                raise ValueError(f"Something went wrong, try again later...")

        except ValueError as e:
            return render_template("input.html", error_message = str(e))

    else:
        return render_template('input.html')

@app.route('/download', methods=['POST', 'GET'])
def download():
    printable_students = []
    for keys, values in students.items():
        student_object = {
            "Name": keys["Name"]
        }

        printable_students.append(student_object)

    cur_path = os.path.dirname(__file__)
    new_path = os.path.join(cur_path, 'files', 'Students.txt')

    with open(new_path, 'w') as file:
        file.write(str(printable_students))

    return send_file('files/students.txt', as_attachment=True)
    

# @app.route('/end', methods=['POST','GET'])
# def end():
#     return render_template("end.html", students=students)


if __name__ == '__main__':
    app.run(debug=True)
