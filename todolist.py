from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker

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
    print("2) Add task")
    print("0) Exit")

    selection = int(input())

    if selection == 1:
        print()
        rows = session.query(Table).all()

        if len(rows) == 0:
            print('Nothing to do!')
            continue
        else:
            for row in rows:
                print(row)
                continue

    elif selection == 2:
        print()
        print('Enter task')

        task_input = input()

        new_row = Table(task='{}'.format(task_input),
                        deadline=datetime.strptime('2021-01-28', '%Y-%m-%d').date())
        session.add(new_row)
        session.commit()
        print('Task has been added!')
        continue

    elif selection == 0:
        print()
        print('Bye!')
        break
