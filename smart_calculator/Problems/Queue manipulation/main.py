from collections import deque

num = int(input())
queue = deque()

for _ in range(num):
    try:
        op, number = input().split()
        queue.appendleft(number)
    except ValueError:
        queue.pop()

for i in range(len(queue)):
    print(queue.pop())
