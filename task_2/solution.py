from sqlite3 import Cursor
import pyodbc,os,click
from datetime import date,datetime

class Sql:
    def __init__(self, database, server="DESKTOP-SU7SNM7\SQLEXPRESS01"):
        self.cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                   "Server="+server+";"
                                   "Database="+database+";"
                                   "Trusted_Connection=yes;")
        self.query = "-- {}\n\n-- Made in Python".format(datetime.now()
                                                         .strftime("%d/%m/%Y"))
class TODO(object):
    __sql = Sql('todoDB')
    __cursor = __sql.cnxn.cursor()
    __ToDoTable = 'ToDoTable'
    __DoneTable = 'DoneItems'
    __separator = '|'
    def addItem(self):
        item = input(f'Введіть задачу, яку потрібно виконати\n(Якщо ви хочете добавити декілька використовуйте {self.__separator} як знак розділення)\n')
        if self.__separator not in item:
            self.__cursor.execute(f"INSERT INTO {self.__ToDoTable} (Item) VALUES ('{item}')")
            self.__cursor.commit()
        else:
            items = item.split(self.__separator)
            for i in items:
                self.__cursor.execute(f"INSERT INTO {self.__ToDoTable} (Item) VALUES ('{i.strip()}')")
            self.__cursor.commit()
        print("Задачу успішно додано!")
    def showItems(self):
        self.__cursor.execute(f'SELECT * FROM {self.__ToDoTable}')
        row = self.__cursor.fetchone()
        while row:
            status = ""
            if row[2]:
                status = "Виконано"
            else:
                status = "Не виконано"
            print(str(row[0]) + '. ' + row[1] + ' -- ' + status )
            row = self.__cursor.fetchone()
    def performItem(self):
        self.showItems()
        id = input("Введіть ід задачі\n")
        self.__cursor.execute(f'update {self.__ToDoTable} set IsDone = 1 where ItemId = {id}')
        self.__cursor.execute(f"insert into {self.__DoneTable} (ItemId,[Date]) values ({str(id)},'{str(date.today()).replace('-','.')}')")
        self.__cursor.commit()
        print("Дані успішно редаговано!")
    def showDoneItems(self):
        self.__cursor.execute(f'select {self.__DoneTable}.ItemId,Item,[Date] from {self.__DoneTable} join {self.__ToDoTable} on {self.__DoneTable}.ItemId = {self.__ToDoTable}.ItemId')
        row = self.__cursor.fetchone()
        while row:
            print(str(row[0]) + '. ' + row[1] + ' ' + str(row[2]))
            row = self.__cursor.fetchone()
        


if __name__ == '__main__':
    menu = """1. Переглянути список задач
2. Додати одну або декілька задач
3. Виконати задачу
4. Переглянути список виконаних задач
0. Зупинити програму"""
    todo = TODO()
    while True:
        print('Меню')
        print(menu)
        key = input(">>>>")
        if key == '1':
            todo.showItems()
        elif key == '2':
            todo.addItem()
        elif key == '3':
            todo.performItem()
        elif key == '4':
            todo.showDoneItems()
        elif key == '0':
            os.system('cls')
            break
        click.pause()
        os.system('cls')
        