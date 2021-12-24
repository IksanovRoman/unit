import psycopg2
from prettytable import PrettyTable
from prettytable import from_db_cursor
import tkinter
from tkinter import messagebox
from tkinter import *
from  tkinter import ttk



connection = psycopg2.connect(database="orders_test", user="postgres", password="123456", host="127.0.0.1", port="5432")
cursor = connection.cursor () 
    
#cursor.execute("")
#try:
#    cursor.execute("update licenses set customerid=2 where customerid=4")
#except:
#    print("Ошибка ввода")
#connection.commit()    

mytable = PrettyTable()

cursor.execute("select * from licenses order by id asc")
mytable = from_db_cursor(cursor)
print(mytable)


def button1():
    '''Данная кнопка выводит информацию о таблице customer из БД'''
    cursor.execute("select * from customer order by id asc")
    mytable = from_db_cursor(cursor)
    print(mytable)
    
    #печатаем текст с прокруткой
    text_box = Text(app, height=10, width=100, font=("Arial", 10), wrap=WORD)
    text_box.grid(row=0, column=1)
    text_box.config(bg='#D9D8D7')
    text_box.insert(1.0,mytable) # вставляем информацию из БД
    sb = Scrollbar( app, orient=VERTICAL)
    sb.grid(row=0, column=2, sticky=NS+W)
    text_box.config(yscrollcommand=sb.set)
    sb.config(command=text_box.yview)

    #кнопка добавление данных
    btn = Button(app, text="Добавить", command=button1_2, bg="#11A40D", font=("Arial", 10, "bold"))
    btn.grid(column=0, row=1)
    #кнопка удаление данных
    btn = Button(app, text="Удалить", command=button1_3,bg="#11A40D", font=("Arial", 10, "bold"))
    btn.grid(column=0,row=2)
    #кнопка изменения данных
    btn = Button(app, text="Изменить", command=button1_4, bg="#11A40D", font=("Arial", 10, "bold"))
    btn.grid(column=0,row=3)
   

def button1_2():
    '''Данная кнопка дает возможность заполнить таблицу customer в БД, здесь же есть проверка на ввод данных'''
    #информация по полям ввода
    lbl = Label(app, text="Введите id заказчика")
    lbl.grid(column=1, row=1, sticky=W)
    lbl = Label(app, text="Введите короткое имя заказчика")
    lbl.grid(column=1, row=2, sticky=W)
    lbl = Label(app, text="Введите полное имя заказчика")
    lbl.grid(column=1, row=3, sticky=W)
    
    #располагаем поля ввода
    text1 = Entry(app, width=30)
    text1.grid(column=1, row=1)
    text2 = Entry(app, width=30)
    text2.grid(column=1, row=2)
    text3 = Entry(app, width=30)
    text3.grid(column=1, row=3)
    

    def gettext():
        '''#функция нужна для ввода данных в таблицу клиентов'''
        
        t1 = text1.get() #получаем значения со всех 3 полей
        t2 = text2.get()
        t3 = text3.get()
        k=0 #маркер, изначально 0, но если 1, то данные запишутся в БД
        n=0 #маркер для проверки уникальности id
        if t1=="" or t2=="" or t3=="": #если одно из поле пустой, то дальше не пойдем
           messagebox.showinfo('Отказано', 'Вы не заполнили все поля')
        else:
            try:
                t1=int(t1) #пробуем конвертировать строку в число, если в строке ввода написали число, то проблем нет
                k=1
            except:
                messagebox.showinfo('Отказано', 'id должно представлять целое число')
            if k: #данные верны, 1 поле это число, остальные два это текст
                answer = messagebox.askyesno(title="Вопрос", message="Записать данные в таблицу?") #диалоговое окно да/нет
                if answer:
                    cursor.execute("select id from customer") #проверим, нет ли такого id уже
                    for row in cursor:
                        if t1==row[0]: #если такой id есть, то пишем ошибку и дальше по коду не идем
                            n=1
                            messagebox.showinfo('Отказано', 'Такой id уже есть')
                    if n==0: #если id уникальный, то записываем его в таблицу БД
                        try:
                            cursor.execute(f"INSERT INTO customer VALUES ({t1},'{t2}','{t3}')")
                            connection.commit()
                            messagebox.showinfo('Успешно', 'Данные занесены')
                        except:
                            messagebox.showinfo('Отказано', 'Неверное заполнение.\nСтрока id не должна повторять значение из таблицы.\nСтрока имени заказчика может быть любой.')

    #кнопка для добавления данных в таблицу        
    btn = Button(app, text="Добавить",command=gettext, bg="#11A40D", font=("Arial", 10, "bold"))
    btn.grid(row=2, column=1, sticky=E)


def button1_3():
    '''Данная кнопка будет удалять данные из таблицы customer по их id'''
    
    #поле с информацией
    lbl = Label(app, text="Введите id, которое хотите удалить")
    lbl.grid(column=1, row=4, sticky=W)
    #поле ввода
    text1 = Entry(app, width=30)
    text1.grid(column=1, row=4)
    
    
    def deleterow():
        '''#функция проверит введеное значение и удалит данные по id из customer'''

        k=0 #проверка ввели ли мы число, если да, то k=1
        n=0 #проврека, есть ли такой id в нашей табличке, есть ли есть, то n=1
        num = text1.get() #получаем строку из поля ввода
        
        try:
            num=int(num) #конвертируем в int
            k=1
        except:
            messagebox.showinfo('Отказано', 'Вы должны ввести целое число')
       
        cursor.execute("select id from customer") #проверим, есть ли такой id в табличке
        for row in cursor:
            print(row[0], text1.get())
            if num == row[0]:
                n=1 #если есть то пишем n=1

        if k: #если это число
            if n: #если оно есть в табличке
                answer = messagebox.askyesno(title="Вопрос", message="Удалить данные из таблицы?\nВнимание, все дочерние записи из других таблиц тоже удалятся") #если отвечаем да
                if answer: 
                    cursor.execute(f"DELETE FROM customer where ID={num}") #удаляем запись из таблицы
                    connection.commit()
                    messagebox.showinfo('Успешно', 'Удалено')
            else:
                messagebox.showinfo('Отказано', 'Такого id нет')
    
    #кнопка удалит данные из таблицы
    btn = Button(app, text="Удалить",command=deleterow, bg="#FF0F15", font=("Arial", 10, "bold"))
    btn.grid(column=1,row=4, sticky=E)


def button1_4():
    '''Данная кнопка будет изменять данные в таблице customer'''
    
    #поле с информацией
    lbl = Label(app, text="ID (старое и новое значение)")
    lbl.grid(column=1, row=5, sticky=W)
    lbl = Label(app, text="Имя (старое и новое значение)")
    lbl.grid(column=1, row=5)
    lbl = Label(app, text="Полное имя (старое и новое значение)")
    lbl.grid(column=1, row=5, sticky=E)
    #поля ввода
    text1 = Entry(app, width=30)
    text1.grid(column=1, row=6,sticky=W)
    text2 = Entry(app, width=30)
    text2.grid(column=1, row=6)
    text3 = Entry(app, width=30)
    text3.grid(column=1, row=6, sticky=E)
    text4 = Entry(app, width=30)
    text4.grid(column=1, row=7,sticky=W)
    text5 = Entry(app, width=30)
    text5.grid(column=1, row=7)
    text6 = Entry(app, width=30)
    text6.grid(column=1, row=7, sticky=E,pady=12)
    

    def update_text():
        pass
    
    btn = Button(app, text="Изменить", command=update_text, bg="#11A40D", font=("Arial", 10, "bold"))
    btn.grid(column=1,row=8)


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
w = app.winfo_screenwidth()
h = app.winfo_screenheight()
app.geometry('%dx%d+0+0' % (w, h))


#первая кнопка вывод таблицы
btn = Button(app, text="Показать клиентов", command=button1, bg="#11A40D", font=("Arial", 10, "bold"))
btn.grid(column=0, row=0)


##btn = Button(app, text="нажмите, чтобы открыть таблицу tools!", command=button2)
##btn.grid(column=0, row=4)
##btn = Button(app, text="нажмите, чтобы открыть таблицу licenses!", command=button3)
##btn.grid(column=3, row=4)
##кнопка показывает истекающие лицензии
#btn = Button(app, text="нажмите, чтобы открыть истекающие лицензии!", command=button4, bg="#00A2E8", font=("Arial", 10, "bold"))
#btn.grid(column=0, row=6)




app.mainloop()
connection.close()