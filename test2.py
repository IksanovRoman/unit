import psycopg2
from prettytable import PrettyTable
from prettytable import from_db_cursor
import tkinter
from tkinter import messagebox
from tkinter import *


connection = psycopg2.connect(database="orders", user="postgres", password="123456", host="127.0.0.1", port="5432")
cursor = connection.cursor () 

mytable = PrettyTable()


#извлечение данных
#cursor.execute("select customer.name_short, tools.name, licenses.date_end from licenses join customer on customer.id = licenses.customerid join tools on tools.id = licenses.toolid")
#rows = cursor.fetchall()
#for row in rows:
#    mytable.add_row(row)
    #print(row)


#print(mytable)

#app = App()
#app.mainloop()

#описываем функционал кнопок

#def gettext():
#    print(text1.get())

def button1():
    '''Данная кнопка выводит информацию о таблице клиентов из БД'''
    cursor.execute("select * from customer")
    mytable = from_db_cursor(cursor)
    print(mytable)
    lbl = Label(app, text=mytable)
    lbl.grid(column=1, row=0)
def button1_2():
    '''Данная кнопка дает возможность заполнить таблицу клиентов в БД, здесь же есть проверка на ввод данных'''
    lbl = Label(app, text="Введите короткое имя заказчика")
    lbl.grid(column=1, row=1)
    lbl = Label(app, text="Введите полное имя заказчика")
    lbl.grid(column=1, row=2)
    
    text1 = Entry(app, width=50)
    text1.grid(column=2, row=1)
    text2 = Entry(app, width=50)
    text2.grid(column=2, row=2)

    def gettext():
        print(text1.get(), type(text1.get()), text2.get(), type(text2.get()))
        if text1.get()!="" and text2.get()!="": #проверка чтобы вводили оба поля
            answer = messagebox.askyesno(title="Вопрос", message="Записать данные в таблицу?")
            if answer:
                cursor.execute(f"INSERT INTO customer (name_short, name_full) VALUES ('{text1.get()}','{text2.get()}')")
                connection.commit()
                messagebox.showinfo('Успешно', 'Данные занесены')
        else:
            messagebox.showinfo('Отказано', 'Вы не заполнили все поля')
    btn = Button(app, text="Добавить",command=gettext)
    btn.grid(row=2, column=3)

    
def button2():
    cursor.execute("select * from tools")
    mytable = from_db_cursor(cursor)
    print(mytable)
    lbl = Label(app, text=mytable)
    lbl.grid(column=1, row=3)
def button3():
    cursor.execute("select * from licenses")
    mytable = from_db_cursor(cursor)
    print(mytable)
    lbl = Label(app, text=mytable)
    lbl.grid(column=1, row=4)
def button4():
    cursor.execute("select customer.name_short, tools.name, licenses.date_end from licenses join customer on customer.id = licenses.customerid join tools on tools.id = licenses.toolid")
    mytable = from_db_cursor(cursor)
    print(mytable)
    lbl = Label(app, text=mytable)
    lbl.grid(column=1, row=5)




def clicked():
    lbl.configure(text="Я же просил...")  


app = Tk()

app.title("Проверка лицензий")
app.iconbitmap("green.ico")
app.geometry("1000x600")


#первая кнопка вывод таблицы
btn = Button(app, text="Нажмите, чтобы открыть таблицу customer!", command=button1)
btn.grid(column=0, row=0)
#вторая кнопка добавление данных
btn = Button(app, text="Добавить данные", command=button1_2)
btn.grid(column=0, row=1)
#третья кнопка удаление данных

btn = Button(app, text="нажмите, чтобы открыть таблицу tools!", command=button2)
btn.grid(column=0, row=3)
btn = Button(app, text="нажмите, чтобы открыть таблицу licenses!", command=button3)
btn.grid(column=0, row=4)
btn = Button(app, text="нажмите, чтобы открыть общую таблицу!", command=button4)
btn.grid(column=0, row=5)




app.mainloop()
connection.close()