# Author: Mateusz Skrzydlo
# ID: A00020956
# Date: 05/11/2024

import re
from datetime import datetime
from tabulate import tabulate

def get_ID():
    """
    Prompts the user for a student ID. Ensures the ID is exactly two digits or the string 'end'.
    :return: Valid student ID or 'end' to terminate input.
    """
    while True:
        user_ID = input("Enter a student ID (2 digits): ")
        if re.fullmatch(r'\d{2}', user_ID) or re.fullmatch(r'^end$', user_ID):
            return user_ID
        else:
            print("The input you entered was invalid.")


def get_dob(dob_string=None, prompt="Enter your Date of Birth (YYYY-MM-DD): "):
    """
    Prompts the user for their date of birth in YYYY-MM-DD format.
    Validates the input and calculates the age.
    :param prompt: Custom prompt message.
    :return: Tuple of date of birth and calculated age.
    """
    while True:
        try:
            if dob_string:
                user_input = dob_string
            else:
                user_input = input(prompt)

            dob = datetime.strptime(user_input, "%Y-%m-%d")
            today = datetime.now()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            return dob.date(), age
        except ValueError:
            print("The input you entered was invalid.")
            # If dob_string is invalid, raise an error instead of looping
            raise ValueError(f"Invalid date format: {dob_string}. Please use YYYY-MM-DD.")


def get_student_name():
    """
    Prompts the user for their name.
    :return: Entered student name.
    """
    return input("Enter your name: ")


def get_input():
    """
    Prompts the user for scores of coursework and the final exam.
    Ensures all inputs are numeric and between 0 and 100.
    :return: List of valid grades.
    """
    while True:
        try:
            m1 = float(input("Enter your score for coursework 1: "))
            m2 = float(input("Enter your score for coursework 2: "))
            m3 = float(input("Enter your score for coursework 3: "))
            m4 = float(input("Enter your score for the final exam: "))

            if all(0 <= score <= 100 for score in (m1, m2, m3, m4)):
                return [m1, m2, m3, m4]
            else:
                print("Error: All scores must be between 0 and 100. Please try again.")
        except ValueError:
            print("Error: Please enter a valid numeric score.")


def calculate_overall_score(grades, weights):
    """
    Calculates the overall weighted score based on grades and their corresponding weights.
    :param grades: List of grades.
    :param weights: List of weights.
    :return: Overall weighted score.
    :raises ValueError: If grades and weights are not of the same length.
    """

    if len(grades) != len(weights):
        raise ValueError("Grades and weights must be of the same length.")
    return sum(grade * weight for grade, weight in zip(grades, weights))


def round_to_category(overall_score):
    """
    Rounds the overall score to the nearest predefined value and assigns a category.
    :param overall_score: Calculated overall score.
    :return: Tuple of nearest score and corresponding category.
    """
    scores = [
        100, 92, 85, 82, 78, 75, 72,
        68, 65, 62, 58, 55, 52,
        48, 45, 42, 38, 35, 32,
        25, 15, 5, 0
    ]
    nearest_score = min(scores, key=lambda x: abs(overall_score - x))
    category = determine_category(nearest_score)
    return nearest_score, category


def determine_category(overall_score_rounded):
    """
    Determines the category for a given rounded score.
    :param overall_score_rounded: Rounded score.
    :return: Corresponding category as a string.
    """
    if not (0 <= overall_score_rounded <= 100):
        return "Ungraded"
    elif overall_score_rounded == 100:
        return "Aurum Standard"
    elif overall_score_rounded >= 82:
        return "Upper First"
    elif overall_score_rounded >= 72:
        return "First"
    elif overall_score_rounded >= 62:
        return "2:1"
    elif overall_score_rounded >= 52:
        return "2:2"
    elif overall_score_rounded >= 42:
        return "Third"
    elif overall_score_rounded >= 32:
        return "Condonable Fail"
    elif overall_score_rounded >= 5:
        return "Fail"
    elif overall_score_rounded == 0:
        return "Defecit Opus"


def user_choice_input_type():

    while True:
        prompt = input("Enter '1' for manual input or '2' to load from file: ")
        if prompt == "1":
            print("You chose manual input.")
            return prompt
        if prompt == "2":
            print("You chose to load from file.")
            return prompt
        else:
            print("Invalid choice. Please enter 1 or 2.")
    
def default():
    """
    Collect data for up to three students, calculate scores, and assign categories.
    :return: List of student data dictionaries.
    """
    students = []
    for _ in range(3):  # Loop for up to three students
        student_ID = get_ID()
        if student_ID.lower() == 'end':  # Allow case-insensitive 'end'
            break

        # Collect student details
        student_name = get_student_name()
        student_DOB, age = get_dob()
        grades = get_input()

        # Calculate scores and categories
        overall_score = calculate_overall_score(grades, [0.1, 0.2, 0.3, 0.4])
        rounded_score, category = round_to_category(overall_score)

        # Add student data to the list
        students.append({
            "UID": student_ID,
            "Name": student_name,
            "D.o.B": student_DOB,
            "Age": age,
            "Raw Score": overall_score,
            "Rounded Score": rounded_score,
            "Category": category
        })

    return students


def User_Choice_Setup_module():
    while True:
        answer = input("Would you like to configure a module? (y/n): ")
        if answer == "y":
            return "y"
        elif answer == "n":
            return "n"
        else: print("Invalid input, try again...")

        
def advanced(file_name, weights):
    """
    Processes a file containing student data, calculates scores, and assigns categories.
    :param file_name: Name of the file containing student data.
    :param weights: List of weights for each grade component.
    :return: List of student data dictionaries.
    """
    try:
        # Read file content
        with open(file_name, "r") as file:
            content = file.read()

        students_imported = content.split("\n")
        students = []

        for line in students_imported:
            if not line.strip():  # Skip empty lines
                continue

            data = line.split(",")
            if len(data) < 7:  # Ensure data has enough columns
                print(f"Skipping invalid row: {line}")
                continue

            # Parse student details
            student_ID = data[0][1:]  # Assuming the ID is wrapped with quotes, remove them
            student_name = data[1]
            student_DOB = data[2].strip('"').strip("'")  # Clean DOB string

            # Validate and parse grades
            try:
                grades = [int(data[i]) for i in range(3, 7)]
            except ValueError:
                print(f"Invalid grades for student {student_ID}. Skipping.")
                continue

            # Calculate age, scores, and category
            try:
                _, age = get_dob(student_DOB)
                overall_score = calculate_overall_score(grades, weights)
                rounded_score, category = round_to_category(overall_score)
            except ValueError as e:
                print(f"Skipping student {student_ID} due to error: {e}")
                continue

            # Add student data to the list
            students.append({
                "UID": student_ID,
                "Name": student_name,
                "D.o.B": student_DOB,
                "Age": age,
                "Raw Score": overall_score,
                "Rounded Score": rounded_score,
                "Category": category
            })

        # Output results
        output_results(students)
        return students

    except FileNotFoundError:
        print(f"No such file: {file_name}. Please try again.")
        raise


def Setup_module(module_name, number_of_components, weights):
    try:
        input("Enter module name: ")
        number_of_modules = int(input("Enter number of components: "))
        weights = []
        for c in range(number_of_modules):
            input("Enter component name: ")
            component_weight = int(input(f"Enter weight: "))
            weights.append(component_weight)
            students = []

        weights = [weight / 100 for weight in weights]

        for s in range(3):
            student_ID = get_ID()
            if student_ID == 'end':
                break

            student_name = get_student_name()  
            student_DOB, age = get_dob()
            grades = []
            for c in range(number_of_modules):
                try:
                    m = float(input(f"Enter your score for coursework {c+1}: "))

                    if (0 <= m <= 100):
                        grades.append(m)
                    else:
                        print("Error: All scores must be between 0 and 100. Please try again.")
                except ValueError:
                    print("Error: Please enter a valid numeric score.")
            
            print(grades, weights)

            overall_score = calculate_overall_score(grades, weights)
            overall_score_rounded, category = round_to_category(overall_score)

            student = {
                "UID": student_ID,
                "Name": student_name,
                "D.o.B": student_DOB,
                "Age": age,
                "Raw Score": overall_score,
                "Rounded Score": overall_score_rounded,
                "Category": category
            }

            students.append(student)

        print("module configuration complete.")
        return students
    except:
        print("Error")


def output_results(students):
    if not students:
        print("No student data available.")
        return

    # Print the table to the console
    print(tabulate(students, headers="keys"))

    # Save the table to the file
    with open("students.txt", 'w') as file:
        file.write(tabulate(students, headers="keys"))



def main():
    configure_choice = input("Would you like to configure a module? (y/n): ")
    if configure_choice.lower() == "y":
        Setup_module()
    elif configure_choice.lower() != "n":
        print("Invalid choice for module configuration.")
        return

    print("1. Enter student data manually")
    print("2. Use advanced mode (read from file)")

    choice = input("Enter your choice (1/2): ")

    if choice == "1":
        students = Setup_module()
        if students:
            output_results(students)
        else:
            print("No student data to display.")

    elif choice == "2":
        filename = input("Enter the filename: ")
        advanced(filename)

    else:
        print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()
 