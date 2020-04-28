#  Posted from EduTools plugin
coor_1 = int(input())
coor_2 = int(input())

if (1 < coor_1 < 8) and (1 < coor_2 < 8):
    print(8)
elif coor_1 in (1, 8) and coor_2 in (1, 8):
    print(3)
else:
    print(5)
