import os
import matplotlib.pyplot as plt
def indexes_list(string, substring):
    list=[]
    deleted_chrs=0
    while string.find(substring) != -1:
        list+=[string.index(substring)+deleted_chrs]
        deleted_chrs+=string.index(substring)+1
        string=string[string.index(substring)+1:]
    return list
def substring_replace(string, substring_old, substring_new):
    list1=indexes_list(string, substring_old)
    list2=[]
    for i in string:
        list2+=[i]
    string=""
    for i in list1:
        list2[i:i+len(substring_old)]=substring_new
    for i in list2:
        string+=i
    return string
def lines(text):
    list = []
    word=""
    for i in range(len(text)):
        if text[i] == "\n" and word != "":
            list+=[word]
            word=""
        elif i == len(text)-1:
            word+=text[i]
            list+=[word]
        else:
            word+=text[i]
    return list
def display_menu():
    print("1. Student grade\n2. Assignment statistics\n3. Assignment graph\n")
    return input("Enter your selection: ")
def find_student(name, id_list):
    for info in id_list:
        if name == info[3:]:
            return info[:3]
    return None
def find_student_grades(name, id_list, submissions_list):
    id=find_student(name, id_list)
    grade_list=[]
    if id != None:
        for grade in submissions_list:
            if id == grade[0:3]:
                grade_list+=[grade]
    return grade_list
def student_id_list(id_list):
    students=id_list+[]
    for i in range(len(students)):
        students[i]=students[i][0:3]
    return students
def student_grade_id_list(name, id_list, submissions_list):
    grades=find_student_grades(name, id_list, submissions_list)
    for i in range(len(grades)):
        grades[i]=grades[i][4:]
        grades[i]=grades[i][:grades[i].index("|")]
    return grades
def grade_weight_list(name, id_list, submissions_list, weights_list):
    grades=student_grade_id_list(name, id_list, submissions_list)
    for i in range(len(grades)):
        grades[i]=weights_list[weights_list.index(grades[i])+1]
    return grades
def grades_list(name, id_list, submissions_list):
    grades=find_student_grades(name, id_list, submissions_list)
    for i in range(len(grades)):
        grades[i] = grades[i][4:]
        grades[i]=grades[i][grades[i].index("|")+1:]
    return grades
def calculate_total_grade(name, id_list, submissions_list, weights_list):
    grades=grades_list(name, id_list, submissions_list)
    weights=grade_weight_list(name, id_list, submissions_list, weights_list)
    for i in range(len(grades)):
        grades[i]=int(grades[i])
        weights[i]=int(weights[i])
        grades[i]*=weights[i]/100
    return round(sum(grades)/10)
def print_total_grade(name, id_list, submissions_list, weights_list):
    print(f"{round(calculate_total_grade(name, id_list, submissions_list, weights_list))}%")
def find_assignment_submissions(name, submissions_list, weights_list):
    grade_list=[]
    id=weights_list[weights_list.index(name)+1]
    for i in range(len(submissions_list)):
        if submissions_list[i][4:].split("|")[0] == id:
            grade_list+=[submissions_list[i]]
    return grade_list
def grade_id_list(weights_list):
    id_list=[]
    for i in range(len(weights_list)):
        if i%3 == 1:
            id_list+=[weights_list[i]]
    return id_list
def find_assignment_stats(name, submissions_list, weights_list):
    grade_list=find_assignment_submissions(name, submissions_list, weights_list)
    for i in range(len(grade_list)):
        grade_list[i]=int(grade_list[i].split("|")[2])
    grade_list.sort()
    min=grade_list[0]
    average = round(sum(grade_list) / len(grade_list))
    max=grade_list[-1]
    return [min, average, max]
def find_assignment(name, weights_list):
    if name in weights_list:
        return weights_list[weights_list.index(name)+1]
    return None
def _():
    print("",end="")
def find_assignment_grades(name, submissions_list, weights_list):
    grade_list = find_assignment_submissions(name, submissions_list, weights_list)
    for i in range(len(grade_list)):
        grade_list[i] = int(grade_list[i].split("|")[2])
    grade_list.sort()
    return grade_list
def main():
    file1 = lines(open("data/assignments.txt").read())
    file2 = lines(open("data/students.txt").read())
    file = [open(f"data/submissions/{item}") for item in os.listdir("data/submissions")]
    for i in range(len(file)):
        file[i] = file[i].read()
    print(file1)
    print(file2)
    print(file)
    print(student_id_list(file2))
    option = display_menu()
    if option == "1":
        name=input("What is the student's name: ")
        if find_student(name, file2) != None:
            #grades=grade_weight_list(name, file2, file, file1)
            #grades=grade_weight_list(name, file2, file, file1)
            #grades=calculate_total_grade(name, file2, file, file1)
            print_total_grade(name, file2, file, file1)
            #print(grade_id_list(file1))
            #print(find_assignment_submissions("Quiz 1", file, file1))
            #print(find_assignment_stats("Quiz 1", file, file1))
        else:
            print("Student not found")
    elif option == "2":
        name=input("What is the assignment name: ")
        if find_assignment(name, file1) != None:
            stats=find_assignment_stats(name, file, file1)
            print(f"Min: {stats[0]}%\nAvg: {stats[1]}%\nMax: {stats[2]}%")
        else:
            print("Assignment not found")
    elif option == "3":
        name=input("What is the assignment name: ")
        if find_assignment(name, file1) != None:
            grades=find_assignment_grades(name, file, file1)
            plt.hist(grades)
            #plt.hist(grades, bins=[0,25,50,75,100])
            plt.show()
            #I couldn't get the graph to be correct, but I got it working at least.
        else:
            print("Assignment not found")
if __name__ == "__main__":
    main()