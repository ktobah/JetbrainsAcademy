# put your python code here
exp = input()
stack = []
error = False
for i in exp:
    if i == '(':
        stack.append(i)
    if i == ')':
        if len(stack) > 0:
            stack.pop()
        else:
            error = True

if len(stack) != 0:
    error = True

if error:
    print("ERROR")
else:
    print('OK')