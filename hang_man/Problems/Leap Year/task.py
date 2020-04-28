#  Posted from EduTools plugin
year = int(input())

if ((year % 4 == 0) & (year % 100 != 0)) or year % 400 == 0:
    print('Leap')
else:
    print('Ordinary')