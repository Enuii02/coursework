from datetime import datetime
from pprint import pprint
import tabulate

class Student:
    def __init__(self, name, UID, DOB, scores, user_choice, module_name, weights):
        #primary:
        self.name = name
        self.UID = UID
        self.DOB = DOB
        self.age = None
        self.raw_score = None
        self.rounded_score = None
        self.category = None
        #cusotm modules:
        self.customModuleName = module_name
        self.custom_module = user_choice
        #secondary:
        self.weights = weights if weights else [0.1, 0.2, 0.3, 0.4]
        self.scores = scores
    #methods 
    def get_age(self):
        dob = datetime.strptime(self.DOB, "%Y-%m-%d")
        today = datetime.now()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        self.age = age

    def get_rawScore(self):

        if all(0 <= score <= 100 for score in self.scores):
            sum_of_weights = sum(self.weights)
            if sum_of_weights != 1:
                raise ValueError("The weights should add up to 100%")
            if len(self.scores) != len(self.weights):
                 raise ValueError(f'Error, the length of scores does not match the length of weights. Scores length: {len(self.scores)}, Weights length: {len(self.weights)}')
            else:
                raw_score = sum(score * weight for score, weight in zip(self.scores, self.weights))
                self.raw_score = raw_score
        else:
            raise ValueError('Error, at least one of the scores is above 100')

    def get_roundedScore(self):
        try:
            scores = [
            100, 92, 85, 82, 78, 75, 72,
            68, 65, 62, 58, 55, 52,
            48, 45, 42, 38, 35, 32,
            25, 15, 5, 0]
            rounded_score = min(scores, key=lambda x: abs(self.raw_score - x))
            self.rounded_score = rounded_score
        except: 
            raise ValueError("An error occured while calculating the rounded score")


    def get_category(self):
        if not (0 <= self.rounded_score <= 100):
            self.category = "Ungraded"
        elif self.rounded_score == 100:
            self.category = "Aurum Standard"
        elif self.rounded_score >= 82:
            self.category = "Upper First"
        elif self.rounded_score >= 72:
            self.category = "First"
        elif self.rounded_score >= 62:
            self.category = "2:1"
        elif self.rounded_score >= 52:
            self.category = "2:2"
        elif self.rounded_score >= 42:
            self.category = "Third"
        elif self.rounded_score >= 32:
            self.category = "Condonable Fail"
        elif self.rounded_score >= 5:
            self.category = "Fail"
        elif self.rounded_score == 0:
            self.category = "Deficit Opus"


def create_list_of_students(content):

    students_imported = content.split("\n")
    students = {}

    for line in students_imported:
        if not line.strip():  # Skip empty lines
            continue

        data = line.split(",")
        if len(data) < 7:  # Ensure data has enough columns
            print(f"Skipping invalid row: {line}")
        

        # Parse student details
        UID = data[0][1:]  # Assuming the ID is wrapped with quotes, remove them
        name = data[1]
        DOB = data[2].strip('"').strip("'")  # Clean DOB string

        # Validate and parse grades
        try:
            grades_list = [int(data[i]) for i in range(3, 7)]
        except ValueError:
            print(f"Invalid grades for student {name}. Skipping.")
            continue

        try:
            students[name] = {
                "UID": UID,
                "name": name,
                "DOB": DOB,
                "List of grades": grades_list
                }

        except ValueError as e:
            print(f"Skipping student {name} due to error: {e}")
            continue

    return students

if __name__ == "__main__":
    mateusz = Student()
    vars(mateusz)['name'] = 'Mateusz'
    vars(mateusz)['UID'] = 69
    vars(mateusz)['DOB'] = '2002-12-28'
    mateusz.get_age()
    vars(mateusz)['scores'] = [40, 43, 40, 40]
    mateusz.get_rawScore()
    mateusz.get_roundedScore()
    mateusz.get_category()
    print('-----------------------')
    pprint(vars(mateusz))
    print('-----------------------')    
    john = Student()
    vars(john)['custom_module'] = True
    vars(john)['scores'] = [40, 69, 20]
    vars(john)['weights'] = [0.3, 0.5, 0.2]
    john.get_rawScore()
    john.get_roundedScore()
    john.get_category()
    print('-----------------------')
    pprint(vars(john))
