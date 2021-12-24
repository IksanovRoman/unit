import psycopg2
from prettytable import PrettyTable
from prettytable import from_db_cursor
import tkinter
from tkinter import messagebox
from tkinter import *
from  tkinter import ttk



connection = psycopg2.connect(database="orders", user="postgres", password="123456", host="127.0.0.1", port="5432")
cursor = connection.cursor () 

mytable = PrettyTable()


#извлечение данных
cursor.execute("select customer.name_short, tools.name, licenses.date_end from licenses join customer on customer.id = licenses.customerid join tools on tools.id = licenses.toolid")
rows = cursor.fetchall()
for row in rows:
    mytable.add_row(row)
   # print(row)

print(mytable)

#print(mytable)

#app = App()
#app.mainloop()

#описываем функционал кнопок

#def gettext():
#    print(text1.get())

def button1():
    '''Данная кнопка выводит информацию о таблице customer из БД'''
    cursor.execute("select * from customer")
    mytable = from_db_cursor(cursor)
    print(mytable)
    
    #печатаем текст с прокруткой
    text_box = Text(app, height=10, width=100, font=("Arial", 8), wrap=WORD)
    text_box.grid(row=0, column=1)
    text_box.config(bg='#D9D8D7')
    text_box.insert(1.0,mytable) # вставляем информацию из БД
    sb = Scrollbar( app, orient=VERTICAL)
    sb.grid(row=0, column=2, sticky=NS+W)
    text_box.config(yscrollcommand=sb.set)
    sb.config(command=text_box.yview)

    #кнопка добавление данных
    btn = Button(app, text="Добавить данные в customer", command=button1_2, bg="#11A40D", font=("Arial", 10, "bold"))
    btn.grid(column=0, row=1)
    #кнопка удаление данных
    btn = Button(app, text="Удаление данных из customer", command=button1_3, bg="#FF0F15", font=("Arial", 10, "bold"))
    btn.grid(column=0,row=2)
   

def button1_2():
    '''Данная кнопка дает возможность заполнить таблицу customer в БД, здесь же есть проверка на ввод данных'''
    #информация по полям ввода
    lbl = Label(app, text="Введите короткое имя заказчика")
    lbl.grid(column=1, row=1)
    lbl = Label(app, text="Введите полное имя заказчика")
    lbl.grid(column=1, row=2)
    
    #располагаем поля ввода
    text1 = Entry(app, width=50)
    text1.grid(column=2, row=1)
    text2 = Entry(app, width=50)
    text2.grid(column=2, row=2)

    #функция нужна для ввода даннхы в таблицу клиентов
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
    
    #кнопка для добавления данных в таблицу        
    btn = Button(app, text="Добавить",command=gettext, bg="#11A40D", font=("Arial", 10, "bold"))
    btn.grid(row=2, column=3)
def button1_3():
    '''Данная кнопка будет удалять данные из таблицы customer по их id'''
    #поле с информацией
    lbl = Label(app, text="Введите id, которое хотите удалить")
    lbl.grid(column=1, row=3)
    #поле ввода
    text1 = Entry(app, width=50)
    text1.grid(column=2, row=3)
    
    #функция проверит введеное значение и удалит данные по id из customer
    def deleterow():
        num = text1.get()
        if num.isdigit():
            answer = messagebox.askyesno(title="Вопрос", message="Удалить данные из таблицу?")
            if answer:
                cursor.execute(f"DELETE FROM customer where ID={num}")
                connection.commit()
                messagebox.showinfo('Успешно', 'Удалено')
        else:
            messagebox.showinfo('Отказано', 'Вы должны ввести целое число')
    
    #кнопка удалит данные из таблицы
    btn = Button(app, text="Удалить",command=deleterow, bg="#FF0F15", font=("Arial", 10, "bold"))
    btn.grid(column=3,row=3)


def button2():
    cursor.execute("select * from tools")
    mytable = from_db_cursor(cursor)
    print(mytable)
    lbl = Label(app, text=mytable)
    lbl.grid(column=1, row=4)
def button3():
    cursor.execute("select * from licenses")
    mytable = from_db_cursor(cursor)
    print(mytable)
    lbl = Label(app, text=mytable)
    lbl.grid(column=4, row=4)

def button4():

    def choise():
        print(selected.get())
        #получаем данные из БД в зависимости от выбранной пользователем кнопки, 0,3,7,30 дней
        cursor.execute(f"select customer.name_short, tools.name, licenses.date_end from licenses join customer on customer.id = licenses.customerid join tools on tools.id = licenses.toolid where licenses.date_end - current_date <= {selected.get()}")
        mytable = from_db_cursor(cursor)
        
        #печатаем таблицы с прокруткой     
        text_box = Text(app, height=10, width=100, font=("Arial", 8), wrap=WORD)
        text_box.grid(row=8, column=1)
        text_box.config(bg='#D9D8D7')
        text_box.insert(1.0,mytable) # вставляем информацию из БД
        sb = Scrollbar( app, orient=VERTICAL)
        sb.grid(row=8, column=2, sticky=NS+W)
        text_box.config(yscrollcommand=sb.set)
        sb.config(command=text_box.yview)

    #выбираем количество дней 1,3,7,30
    lbl = Label(app, text="Выберите количество дней")
    lbl.grid(column=0, row=7)
    selected = IntVar()
    rad1 = Radiobutton(app,text='Сегодня', value=0, variable=selected)  
    rad2 = Radiobutton(app,text='3', value=3, variable=selected)  
    rad3 = Radiobutton(app,text='7', value=7, variable=selected)
    rad4 = Radiobutton(app,text='30', value=30, variable=selected)
    rad1.grid(column=0, row=8,sticky=W)  
    rad2.grid(column=0, row=9,sticky=W)  
    rad3.grid(column=0, row=10,sticky=W)   
    rad4.grid(column=0, row=11,sticky=W)

    #нажав на кнопку, печатаем это все в окне
    btn = Button(app, text="Показать", command=choise, bg="#00A2E8", font=("Arial", 10, "bold"))
    btn.grid(column=0, row=8)
    

    
    #cursor.execute("select customer.name_short, tools.name, licenses.date_end from licenses join customer on customer.id = licenses.customerid join tools on tools.id = licenses.toolid")
    #mytable = from_db_cursor(cursor)
    #print(mytable)
    #lbl = Label(app, text=mytable)
    #lbl.grid(column=1, row=6)




#def clicked():
#    lbl.configure(text="Я же просил...")  


app = Tk()

app.title("Проверка лицензий")
app.iconbitmap("green.ico")
#app["bg"] = "#A349A4"
#app.geometry("1000x600")



#text_box = Text(
#    app,
#    height=20,
#    width=50, 
#    font=(5)  
#)

#text_box.grid(row=0, column=0)
#text_box.config(bg='#D9D8D7')
#text_box.insert(1.0,mytable)

#sb = Scrollbar(
#    app,
#    orient=VERTICAL, 
#    )

#sb.grid(row=0, column=1, sticky=NS)
#text_box.config(yscrollcommand=sb.set)
#sb.config(command=text_box.yview)



 


mainmenu = Menu(app)
app.config(menu=mainmenu)
first_menu = Menu(mainmenu, tearoff=0)
first_menu.add_command(label='Просмотр таблиц', command=button1)
first_menu.add_command(label='Изменение таблиц')
first_menu.add_command(label='Удаление таблиц')
first_menu.add_command(label='ХАХ таблиц')
mainmenu.add_cascade(label="Файл", menu=first_menu)



#первая кнопка вывод таблицы
btn = Button(app, text="Нажмите, чтобы открыть таблицу customer!", command=button1, bg="#11A40D", font=("Arial", 10, "bold"))
btn.grid(column=0, row=0)


#btn = Button(app, text="нажмите, чтобы открыть таблицу tools!", command=button2)
#btn.grid(column=0, row=4)
#btn = Button(app, text="нажмите, чтобы открыть таблицу licenses!", command=button3)
#btn.grid(column=3, row=4)
#кнопка показывает истекающие лицензии
btn = Button(app, text="нажмите, чтобы открыть истекающие лицензии!", command=button4, bg="#00A2E8", font=("Arial", 10, "bold"))
btn.grid(column=0, row=6)




app.mainloop()
connection.close()