from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    task = Column(String, default=None)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

while True:
    print()
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")

    selection = int(input())

    if selection == 1:
        print()
        rows = session.query(Table).all()

        if len(rows) == 0:
            print('Nothing to do!')
            print()
            continue
        else:
            for row in rows:
                print(row)
                continue

    elif selection == 2:
        print()
        weeks_tasks = session.query(Table).filter(
            Table.deadline.between(datetime.today().date(), datetime.today().date() + timedelta(days=7))).all()

        start_date = datetime.today().date()
        number_of_days = 7

        date_list = [(start_date + timedelta(days=day)) for day in range(number_of_days)]

        if len(weeks_tasks) == 0:
            for date in date_list:
                print(date.strftime('%A %d %b'))
                print('Nothing to do!')
                print()
            continue
        else:
            for date in date_list:
                date_tasks = []
                for tasks in weeks_tasks:
                    if tasks.deadline == date:
                        date_tasks.append(tasks)
                if len(date_tasks) == 0:
                    print(date.strftime('%A %d %b'))
                    print('Nothing to do!')
                    print()
                    continue
                else:
                    print(date.strftime('%A %d %b'))
                    for day_task in date_tasks:
                        print('{}. {}'.format(date_tasks.index(day_task), day_task.task))
                    print()

            continue

    elif selection == 3:
        print()
        all_tasks = session.query(Table).order_by(Table.deadline).all()
        for number in range(len(all_tasks)):
            print('{}. {}.{}'.format(number + 1, all_tasks[number], all_tasks[number].deadline.strftime('%e %b')))
        continue

    elif selection == 4:
        print()
        print('Missed tasks:')
        rows_missed = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
        if len(rows_missed) == 0:
            print('Nothing is missed!')
            continue
        else:
            for j in range(0, len(rows_missed)):
                print('{}. {}. {}'.format(j + 1, rows_missed[j].task, rows_missed[j].deadline))
                continue

    elif selection == 5:
        print()
        print('Enter task')

        task_input = input()
        print('Enter deadline')
        deadline_input = input()
        new_row = Table(task='{}'.format(task_input),
                        deadline=datetime.strptime(deadline_input, '%Y-%m-%d').date())
        session.add(new_row)
        session.commit()
        print('Task has been added!')
        continue

    elif selection == 6:
        print()
        print('Choose the number of the task you want to delete:')
        rows_delete = session.query(Table).all()
        for i in range(0, len(rows_delete)):
            print('{}. {}. {}'.format(i + 1, rows_delete[i].task, rows_delete[i].deadline))
        if len(rows_delete) == 0:
            continue
        else:
            specific_row = rows_delete[int(input()) - 1]
            session.delete(specific_row)
            session.commit()
            print('The task has been deleted!')
            continue

    elif selection == 0:
        print()
        print('Bye!')
        break
