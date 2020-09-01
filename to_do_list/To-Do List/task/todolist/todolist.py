# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='Nothing to do!')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


def generate_database():
    engine = create_engine('sqlite:///todo.db?check_same_thread=True')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session


def create_task(session):
    task_description = input("Enter task")
    task_deadline = datetime.strptime(input("Enter deadline"), '%Y-%m-%d')
    new_row = Task(task=task_description, deadline=task_deadline)
    session.add(new_row)
    session.commit()
    print('The task has been added!\n')


def delete_task(session):
    print("Choose the number of the task you want to delete:")
    tasks = session.query(Task).order_by(Task.deadline).all()
    if tasks:
        for idx, task in enumerate(tasks):
            print(f"{idx+1}. {task.task}. {task.deadline.day} {task.deadline.strftime('%b')}")
        delete_choice = int(input())
        session.delete(tasks[delete_choice - 1])
        session.commit()
        print("The task has been deleted!\n")
    else:
        print("Nothing to delete\n")


def get_tasks(session, mode="today"):
    if mode == "today":
        today = datetime.today()
        tasks = session.query(Task).filter(Task.deadline == today.date()).all()
        print(f"Today {today.day} {today.strftime('%b')}:")
    elif mode == "all":
        tasks = session.query(Task).order_by(Task.deadline).all()
        print("All tasks:")
    elif mode == "week":
        today = datetime.today()
        next_day = today
        tasks = []
        i = 1
        task = session.query(Task).filter(Task.deadline == today.date()).all()
        if task:
            tasks.append({"date": f"{today.strftime('%A %d %b')}", "task": task[0].task})
        else:
            tasks.append({"date": f"{today.strftime('%A %d %b')}", "task": "Nothing to do!"})
        while i <= 6:
            i += 1
            next_day = next_day + timedelta(days=1)
            task = session.query(Task).filter(Task.deadline == next_day.date()).all()
            if task:
                tasks.append({"date": f"{next_day.strftime('%A %d %b')}", "task": task[0].task})
            else:
                tasks.append({"date": f"{next_day.strftime('%A %d %b')}", "task": "Nothing to do!"})
    elif mode == "missed":
        today = datetime.today()
        tasks = session.query(Task).filter(Task.deadline < today.date()).order_by(Task.deadline).all()
        print("Missed tasks:")
    if tasks:
        for idx, task in enumerate(tasks):
            if mode == "today":
                print(task.task)
            elif mode == "all" or mode == "missed":
                print(f"{idx+1}. {task.task}. {task.deadline.day} {task.deadline.strftime('%b')}")
            elif mode == "week":
                print(f"{task['date']}:")
                print(f"{task['task']}\n")
        print()
    else:
        print("Nothing to do!\n")


session = generate_database()

while True:
    print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
    action = int(input())
    print()
    if action == 1:
        get_tasks(session, mode="today")
    if action == 2:
        get_tasks(session, mode="week")
    if action == 3:
        get_tasks(session, mode="all")
    elif action == 4:
        get_tasks(session, mode="missed")
    elif action == 5:
        create_task(session)
    elif action == 6:
        delete_task(session)
    elif action == 0:
        print("\nBye!")
        break
