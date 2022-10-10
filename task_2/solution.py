from asyncio.windows_events import NULL
from lib2to3.pgen2.token import RARROW
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
    __separator = ';'

    def addItem(self):

        item = input(f'Введіть задачу, яку потрібно виконати\n(Якщо ви хочете добавити декілька використовуйте {self.__separator} як знак розділення)\n')
        os.system('cls')

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
        self.__cursor.execute(f'SELECT * FROM {self.__ToDoTable} where IsDone = 0')
        row = self.__cursor.fetchone()

        if row is None:
            print("На даний момент, список задач пустий!")
            
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
        id = input("Введіть ід задачі\n>>>>")
        os.system('cls')

        self.__cursor.execute(f'update {self.__ToDoTable} set IsDone = 1 where ItemId = {id}')
        self.__cursor.execute(f"insert into {self.__DoneTable} (ItemId,[Date]) values ({str(id)},'{str(date.today()).replace('-','.')}')")
        self.__cursor.commit()
        
        print("Дані успішно редаговано!")

    def showDoneItems(self):
        self.__cursor.execute(f'select {self.__DoneTable}.ItemId,Item,[Date] from {self.__DoneTable} join {self.__ToDoTable} on {self.__DoneTable}.ItemId = {self.__ToDoTable}.ItemId order by [Date]')
        row = self.__cursor.fetchone()
        counter = 1 

        while row:
            print(str(counter) + '. ' + str(row[2]) + ' ' + row[1] )
            row = self.__cursor.fetchone()
            counter +=1
    
    def deleteItem(self):
        while(True):
            self.showItems()
            id = input("Введіть id задачі,яку хочете видалити:\n>>>>")
            os.system('cls')

            try:
                self.__cursor.execute(f'DELETE FROM {self.__ToDoTable} where ItemId = {id}')
                self.__cursor.commit()
            except:
                print('Ви ввели неправильне ід, спробуйте ще раз!')
                click.pause()
                os.system('cls')
            finally:
                print("Задачу успішно видалено!")
                break
    
    def deleteDoneItem(self):
        self.showDoneItems()
        date = input('Введіть дату по якій хочете видалити записи, або ж * якщо хочете видалити все.\n>>>>')
        os.system('cls')

        if date is '*':
            self.__cursor.execute(f'TRUNCATE TABLE {self.__DoneTable}')
            self.__cursor.execute(f'DELETE FROM {self.__ToDoTable} where IsDone = 1')
            self.__cursor.commit()
            print('Усі виконані задачі успішно видалено!')
        else:
            print()
            date = str(date).replace('-','.')
            self.__cursor.execute(f"SELECT [ItemId] FROM {self.__DoneTable} where [Date] = '{date}'")
            row = self.__cursor.fetchone()
            listId = []

            if row is None:
                print('Помилка введення дати')
            else:
                while row:
                    listId.append(row[0])
                    row = self.__cursor.fetchone()
            
            self.__cursor.execute(f"DELETE FROM {self.__DoneTable} where [Date] = '{date}'")

            for id in listId:
                self.__cursor.execute(f"DELETE FROM {self.__ToDoTable} where ItemId = {id}")

            self.__cursor.commit()
            print(f'Виконані справи за {date} успішно видалено')
            
        
        
        



if __name__ == '__main__':
    todo = TODO()
    os.system('cls')
    menu = """1. Переглянути список невиконаних задач
2. Додати одну або декілька задач
3. Виконати задачу
4. Видалити задачу
5. Переглянути список виконаних задач
6. Очистити список виконаних задач за конкретний день
0. Зупинити програму"""

    while True:
        print('Меню')
        print(menu)
        key = input(">>>>")
        os.system('cls')
        try:
            if key == '1':
                todo.showItems()
            elif key == '2':
                todo.addItem()
            elif key == '3':
                todo.performItem()
            elif key == '4':
                todo.deleteItem()
            elif key == '5':
                todo.showDoneItems()
            elif key == '6':
                todo.deleteDoneItem()
            elif key == '0':
                os.system('cls')
                break
            else:
                print("Ви ввели неправильний номер, спробуйте знову!")
        except:
            print('Виникла помилка спробуйте знову!')
        click.pause()
        os.system('cls')
        