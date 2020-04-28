#  Posted from EduTools plugin
# put your python code here
student_1 = int(input())
student_2 = int(input())
student_3 = int(input())
students = [student_1, student_2, student_3]
desks = 0
for i in students:
    if i % 2 == 0:
        desks += i // 2
    else:
        desks += (i // 2) + 1
print(desks)
