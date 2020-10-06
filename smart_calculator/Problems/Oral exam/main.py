from collections import deque

queue = deque()
n = int(input())
passed = []
for _ in range(n):
    expression = input()
    if "READY" in expression:
        queue.appendleft(expression.split()[1])
    elif "PASSED" in expression:
        passed.append(queue.pop())
    elif "EXTRA" in expression:
        queue.appendleft(queue.pop())

for i in passed:
    print(i)
