from student_class import Student, create_list_of_students
from flask import Flask, render_template, request, redirect, url_for, g

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
    weights = request.form.get('custom_weights')

    global list_of_students
    global students
    for s in list_of_students.values():
        students[s["name"]] = Student(s["name"], s["UID"], s["DOB"], s["List of grades"], None, 'module', weights)
        students[s["name"]].get_age()
        students[s["name"]].get_rawScore()
        students[s["name"]].get_roundedScore()
        students[s["name"]].get_category()


    # return f"<p>{students} match my freak</p>"
    return render_template("end.html", students=students)
        
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

# @app.route('/end', methods=['POST','GET'])
# def end():
#     return render_template("end.html", students=students)


if __name__ == '__main__':
    app.run(debug=True)
