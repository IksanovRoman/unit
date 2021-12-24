'''Обе кнопки работают нормально customer, tools'''
import psycopg2
from prettytable import PrettyTable
from prettytable import from_db_cursor
from datetime import datetime, date
import tkinter
from tkinter import messagebox
from tkinter import *
from  tkinter import ttk



connection = psycopg2.connect(database="orders_test", user="postgres", password="123456", host="127.0.0.1", port="5432")
cursor = connection.cursor () 
    
mytable = PrettyTable()

cursor.execute("select * from licenses order by id asc")
mytable = from_db_cursor(cursor)
print(mytable)


def show_customer_table():
    '''Данная кнопка выводит информацию о таблице клиентов из БД'''
    cursor.execute("select * from customer order by id asc")
    mytable = from_db_cursor(cursor)
    print(mytable)
    
    #печатаем текст с прокруткой
    txt = Text(app, height=5, width=100,  wrap=WORD)
    txt.grid(row=0, column=1) 
    txt.insert(1.0,mytable) # вставляем информацию из БД
    txt.config(bg='#D9D8D7', state='disabled')
    
    sb = Scrollbar( app, orient=VERTICAL)
    sb.grid(row=0, column=1, sticky=NS+E)
    txt.config(yscrollcommand=sb.set)
    sb.config(command=txt.yview)

    #кнопка добавление данных
    btn = Button(app, text="Добавить", command=add_customer_table, bg="#11A40D", font=("Arial", 12, "bold"))
    btn.grid(column=0, row=1)
    #кнопка удаление данных
    btn = Button(app, text="Удалить", command=delete_customer_table,bg="#11A40D", font=("Arial", 12, "bold"))
    btn.grid(column=0,row=2)
    #кнопка изменения данных
    btn = Button(app, text="Изменить", command=update_customer_table, bg="#11A40D", font=("Arial", 12, "bold"))
    btn.grid(column=0,row=3)
 
def add_customer_table():
    '''Данная кнопка дает возможность заполнить таблицу customer в БД, здесь же есть проверка на ввод данных'''
    #информация по полям ввода
    lbl = Label(app, text="Введите id заказчика (целое число)")
    lbl.grid(column=1, row=1, sticky=W)
    lbl = Label(app, text="Введите короткое имя заказчика (любте значение)")
    lbl.grid(column=1, row=2, sticky=W)
    lbl = Label(app, text="Введите полное имя заказчика (любое значение)")
    lbl.grid(column=1, row=3, sticky=W)
    
    #располагаем поля ввода
    text1 = Entry(app, width=30)
    text1.grid(column=1, row=1)
    text2 = Entry(app, width=30)
    text2.grid(column=1, row=2)
    text3 = Entry(app, width=30)
    text3.grid(column=1, row=3)
    

    def add_information_customer():
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
                cursor.execute("select * from customer") #проверим, нет ли такого id уже
                for row in cursor:
                    if t1==row[0] or t2==row[1] or t3==row[2]: #если такой id или имя заказчика уже есть, то пишем ошибку и дальше по коду не идем
                        n=1

                if n==1:
                    messagebox.showinfo('Отказано', 'Заказчик с таким именем или id уже существует')
                else: #если id уникальный, то записываем его в таблицу БД
                    answer = messagebox.askyesno(title="Вопрос", message="Записать данные в таблицу?") #диалоговое окно да/нет
                    if answer:
                        cursor.execute(f"INSERT INTO customer VALUES ({t1},'{t2}','{t3}')")
                        connection.commit()
                        messagebox.showinfo('Успешно', 'Данные занесены')
                        
    #кнопка для добавления данных в таблицу        
    btn = Button(app, text="Добавить",command=add_information_customer, bg="#11A40D", font=("Arial", 12, "bold"))
    btn.grid(row=2, column=1, sticky=E)

def delete_customer_table():
    '''Данная кнопка будет удалять данные из таблицы customer по их id'''
    
    #поле с информацией
    lbl = Label(app, text="Введите id, которое хотите удалить")
    lbl.grid(column=1, row=4, sticky=W)
    #поле ввода
    text1 = Entry(app, width=30)
    text1.grid(column=1, row=4)
    
    
    def delete_information_customer():
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
            if num == row[0]:
                n=1 #если есть то пишем n=1

        if k: #если это число
            if n: #если оно есть в табличке
                answer = messagebox.askyesno(title="Вопрос", message="Удалить данные из таблицы?\nВнимание, все дочерние записи из других таблиц тоже удалятся") #вопрос подтверждения
                if answer: #если отвечаем да
                    cursor.execute(f"DELETE FROM customer where ID={num}") #удаляем запись из таблицы
                    connection.commit()
                    messagebox.showinfo('Успешно', 'Удалено')
            else:
                messagebox.showinfo('Отказано', 'Такого id нет')
    
    #кнопка удалит данные из таблицы
    btn = Button(app, text="Удалить",command=delete_information_customer, bg="#11A40D", font=("Arial", 12, "bold"))
    btn.grid(column=1,row=4, sticky=E)

def update_customer_table():
    '''Данная кнопка будет изменять данные в таблице customer'''
    
    #поле с информацией
    lbl = Label(app, text="Введите id, где нужно изменить значения")
    lbl.grid(column=1, row=5)
    #поле ввода id
    text1 = Entry(app, width=30)
    text1.grid(column=1, row=6)
    
    def update_customer_check_id():
        '''Данная кнопка будет проверять есть ли такой id в таблице и в дальнейшем изменять содержимое таблицы'''

        k=0 #проверка ввели ли мы число, если да, то k=1
        n=0 #проврека, есть ли такой id в нашей табличке, есть ли есть, то n=1
        num = text1.get() #получаем текст из поля ввода
        
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

        if k==1 and n==0:
            messagebox.showinfo('Отказано', 'Такого id в таблице нет')
        elif k and n:
            #данный блок будет принимать данные, а затем изменять табличку customer

            #подписи к полям ввода
            lbl1 = Label(app, text="Поменять можно либо id, либо имя заказчика")
            lbl1.grid(column=1, row=7, sticky="W")
            lbl2 = Label(app, text="Введите новое id")
            lbl2.grid(column=1, row=8, sticky="W")
            lbl3 = Label(app, text="Введите сокращенное имя заказчика")
            lbl3.grid(column=1, row=8)
            lbl4 = Label(app, text="Введите полное имя заказчика")
            lbl4.grid(column=1, row=8, sticky="E")

            #поля ввода
            text2 = Entry(app, width=30)
            text2.grid(column=1, row=9, sticky="W")
            text3 = Entry(app, width=30)
            text3.grid(column=1, row=9)
            text4 = Entry(app, width=30)
            text4.grid(column=1, row=9, sticky="E")
            

            def update_customer_id():
                '''Данная функция добавит данные в табличку в поле ID'''
                #получаем 2 поле ввода
                t1 = text2.get()

                if t1!="":
                    #если оно не пустые

                    m=0 #проверка на ввод цифр
                    l=0 #проверка на наличие такого id в таблице
                    try:
                        t1=int(t1) #конвертируем в int
                        m=1
                    except:
                        messagebox.showinfo('Отказано', 'Вы должны ввести целое число')
                    
                    cursor.execute("select id from customer") #проверим, есть ли такой id в табличке
                    for row in cursor:
                        print(row[0], text1.get())
                        if t1 == row[0]:
                            l=1 #если есть то пишем n=1
                            messagebox.showinfo('Отказано', 'Данный id уже занят')
                    if m and l==0:
                        #если все правильно введено, то обновляем id в табличке
                        answer = messagebox.askyesno(title="Вопрос", message="Изменить таблицу?")
                        if answer:
                            cursor.execute(f"UPDATE customer SET id = {t1} WHERE id = {num}")
                            connection.commit()
                            messagebox.showinfo('Успешно', 'Данные обновлены')
                            
                            text2.grid_remove()
                            text3.grid_remove()
                            text4.grid_remove()
                            lbl1.grid_remove()
                            lbl2.grid_remove()
                            lbl3.grid_remove()
                            lbl4.grid_remove()
                            btn1.grid_remove()
                            btn2.grid_remove()
                else:
                    messagebox.showinfo('Успешно', 'Поле ID пустое')
            def update_customer():
                '''Данная функция добавит данные в табличку, если пользователь ввел id, либо имена заказчика'''
                #получаем два поля ввода
                t2 = text3.get()
                t3 = text4.get()
                

                if t2!="" and t3!="" :
                    #если оба поля не пустые
                    answer = messagebox.askyesno(title="Вопрос", message="Изменить имена заказчиков?")
                    if answer:
                        cursor.execute(f"UPDATE customer SET name_short = '{t2}' WHERE id = {num}")
                        cursor.execute(f"UPDATE customer SET name_full = '{t3}' WHERE id = {num}")
                        connection.commit()
                        messagebox.showinfo('Отказано', 'Данные обновлены')
                else:
                    messagebox.showinfo('Отказано', 'Заполните оба поля имени заказчика')


            #данная кнопка добавит данные в табличку
            btn1 = Button(app, text="Изменить ID", command=update_customer_id, bg="#11A40D", font=("Arial", 12, "bold"))
            btn1.grid(column=1,row=10,sticky="W")
            btn2 = Button(app, text="Изменить имена заказчиков", command=update_customer, bg="#11A40D", font=("Arial", 12, "bold"))
            btn2.grid(column=1,row=10)

    #кнопка подтверждения
    btn = Button(app, text="Подтвердить", command=update_customer_check_id, bg="#11A40D", font=("Arial", 12, "bold"))
    btn.grid(column=1,row=7)
    
    


def show_tools_table():
    '''Данная кнопка выводит информацию о таблице средств защиты из БД'''
    cursor.execute("select * from tools order by id asc")
    mytable = from_db_cursor(cursor)
    
    #печатаем текст с прокруткой
    txt = Text(app, height=5, width=100, wrap=WORD)
    txt.grid(row=11, column=1) 
    txt.insert(1.0,mytable) # вставляем информацию из БД
    txt.config(bg='#D9D8D7', state='disabled')

    sb = Scrollbar( app, orient=VERTICAL)
    sb.grid(row=11, column=1, sticky=NS+E)
    txt.config(yscrollcommand=sb.set)
    sb.config(command=txt.yview)

    #кнопка добавление данных
    btn = Button(app, text="Добавить", command=add_tools_table, bg="#00A2E8", font=("Arial", 12, "bold"))
    btn.grid(column=0, row=12)
    #кнопка удаление данных
    btn = Button(app, text="Удалить", command=delete_tools_table,bg="#00A2E8", font=("Arial", 12, "bold"))
    btn.grid(column=0,row=14)
    #кнопка изменения данных
    btn = Button(app, text="Изменить", command=update_tools_table, bg="#00A2E8", font=("Arial", 12, "bold"))
    btn.grid(column=0,row=15)

def add_tools_table():
    '''Данная кнопка дает возможность заполнить таблицу tools в БД, здесь же есть проверка на ввод данных'''

    #информация по полям ввода
    lbl = Label(app, text="Введите id средства защиты (целое число)")
    lbl.grid(column=1, row=12, sticky=W)
    lbl = Label(app, text="Введите наименование средства защиты (любое значение)")
    lbl.grid(column=1, row=13, sticky=W)

    #располагаем поля ввода
    text1 = Entry(app, width=30)
    text1.grid(column=1, row=12)
    text2 = Entry(app, width=30)
    text2.grid(column=1, row=13)

    def add_information_tools():
        '''#функция нужна для ввода данных в таблицу средств защиты'''
        
        t1 = text1.get() #получаем значения с 2 полей
        t2 = text2.get()
        k=0 #маркер, изначально 0, но если 1, то данные запишутся в БД
        n=0 #маркер для проверки уникальности id
        if t1=="" or t2=="": #если одно из полей пустое, то дальше не пойдем
           messagebox.showinfo('Отказано', 'Вы не заполнили все поля')
        else:
            try:
                t1=int(t1) #пробуем конвертировать строку в число, если в строке ввода написали число, то проблем нет
                k=1
            except:
                messagebox.showinfo('Отказано', 'id должно представлять целое число')
            if k: #данные верны, 1 поле это число, второе поле это текст
                cursor.execute("select * from tools") #проверим, нет ли такого id уже
                for row in cursor:
                    if t1==row[0] or t2==row[1]: #если такой id есть или средство защиты уже есть, то пишем ошибку и дальше по коду не идем
                        n=1
                if n==1:
                    messagebox.showinfo('Отказано', 'Такое средство защиты или его id уже существует')
                else: #если id уникальный, то записываем его в таблицу БД
                    answer = messagebox.askyesno(title="Вопрос", message="Записать данные в таблицу?") #диалоговое окно да/нет
                    if answer:
                        cursor.execute(f"INSERT INTO tools VALUES ({t1},'{t2}')")
                        connection.commit()
                        messagebox.showinfo('Успешно', 'Данные занесены')

    #кнопка для добавления данных в таблицу        
    btn = Button(app, text="Добавить",command=add_information_tools, bg="#00A2E8", font=("Arial", 12, "bold"))
    btn.grid(row=13, column=1, sticky=E)

def delete_tools_table():
    '''Данная кнопка будет удалять данные из таблицы tools по их id'''

    #поле с информацией
    lbl = Label(app, text="Введите id, которое хотите удалить")
    lbl.grid(column=1, row=14, sticky=W)
    #поле ввода
    text1 = Entry(app, width=30)
    text1.grid(column=1, row=14)

    def delete_information_tools():
        '''#функция проверит введеное значение и удалит данные по id из tools'''
        
        k=0 #проверка ввели ли мы число, если да, то k=1
        n=0 #проврека, есть ли такой id в нашей табличке, есть ли есть, то n=1
        num = text1.get() #получаем строку из поля ввода

        try:
            num=int(num) #конвертируем в int
            k=1
        except:
            messagebox.showinfo('Отказано', 'Вы должны ввести целое число')

        cursor.execute("select id from tools") #проверим, есть ли такой id в табличке
        for row in cursor:
            if num == row[0]:
                n=1 #если есть то пишем n=1
        
        if k: #если это число
            if n: #если оно есть в табличке
                answer = messagebox.askyesno(title="Вопрос", message="Удалить данные из таблицы?\nВнимание, все дочерние записи из других таблиц тоже удалятся") #вопрос подтверждение
                if answer:  #если отвечаем да
                    cursor.execute(f"DELETE FROM tools where ID={num}") #удаляем запись из таблицы
                    connection.commit()
                    messagebox.showinfo('Успешно', 'Удалено')
            else:
                messagebox.showinfo('Отказано', 'Такого id нет')


    #кнопка удалит данные из таблицы
    btn = Button(app, text="Удалить",command=delete_information_tools, bg="#00A2E8", font=("Arial", 12, "bold"))
    btn.grid(column=1,row=14, sticky=E)

def update_tools_table():
    '''Данная кнопка будет изменять данные в таблице tools'''

    #поле с информацией
    lbl = Label(app, text="Введите id, где нужно изменить значения")
    lbl.grid(column=1, row=15)
    #поле ввода id
    text1 = Entry(app, width=30)
    text1.grid(column=1, row=16)

    def update_tools_check_id():
        '''Данная кнопка будет проверять есть ли такой id в таблице и в дальнейшем изменять содержимое таблицы'''
        
        k=0 #если мы ввели число, то k=1
        n=0 #если такой id есть, то n=1
        num = text1.get() #получаем текст из поля ввода

        try:
            num=int(num) #конвертируем в int
            k=1
        except:
            messagebox.showinfo('Отказано', 'Вы должны ввести целое число')
        
        cursor.execute("select id from tools") #проверим, есть ли такой id в табличке
        for row in cursor:
            print(row[0], text1.get())
            if num == row[0]:
                n=1 #если есть то пишем n=1

        if k==1 and n==0:
            messagebox.showinfo('Отказано', 'Такого id в таблице нет')
        elif k and n:
            #данный блок будет принимать данные, а затем изменять табличку tools
            
            #подписи к полям ввода
            lbl1 = Label(app, text="Поменять можно либо id, либо средство защиты")
            lbl1.grid(column=1, row=17, sticky="W")
            lbl2 = Label(app, text="Введите новое id")
            lbl2.grid(column=1, row=18, sticky="W")
            lbl3 = Label(app, text="Введите название средства защиты")
            lbl3.grid(column=1, row=18)

            #поля ввода
            text2 = Entry(app, width=30)
            text2.grid(column=1, row=19, sticky="W")
            text3 = Entry(app, width=30)
            text3.grid(column=1, row=19)

            def update_tools_id():
                '''Данная функция добавит данные в табличку в поле ID'''
                #получаем 2 поле ввода
                t1 = text2.get()

                if t1!="":
                    #если оно не пустые

                    m=0 #проверка на ввод цифр
                    l=0 #проверка на наличие такого id в таблице
                    try:
                        t1=int(t1) #конвертируем в int
                        m=1
                    except:
                        messagebox.showinfo('Отказано', 'Вы должны ввести целое число')
                    
                    cursor.execute("select id from tools") #проверим, есть ли такой id в табличке
                    for row in cursor:
                        print(row[0], text1.get())
                        if t1 == row[0]:
                            l=1 #если есть то пишем n=1
                            messagebox.showinfo('Отказано', 'Данный id уже занят')
                    if m and l==0:
                        #если все правильно введено, то обновляем id в табличке
                        answer = messagebox.askyesno(title="Вопрос", message="Изменить таблицу?")
                        if answer:
                            cursor.execute(f"UPDATE tools SET id = {t1} WHERE id = {num}")
                            connection.commit()
                            messagebox.showinfo('Успешно', 'Данные обновлены')
                            
                            text2.grid_remove()
                            text3.grid_remove()
                            lbl1.grid_remove()
                            lbl2.grid_remove()
                            lbl3.grid_remove()
                            btn1.grid_remove()
                            btn2.grid_remove()
                else:
                    messagebox.showinfo('Отказ', 'Поле ID пустое')
            def update_tools():
                '''Данная функция добавит данные в табличку, если пользователь ввел id, либо поле средста защиты'''
                #получаем поля ввода
                t2 = text3.get()
                

                if t2!="":
                    #если оба поля не пустые
                    answer = messagebox.askyesno(title="Вопрос", message="Изменить средство защиты?")
                    if answer:
                        cursor.execute(f"UPDATE tools SET license_name = '{t2}' WHERE id = {num}")
                        connection.commit()
                        messagebox.showinfo('Отказано', 'Данные обновлены')
                else:
                    messagebox.showinfo('Отказано', 'Заполните поле')
                

            #данная кнопка добавит данные в табличку
            btn1 = Button(app, text="Изменить ID", command=update_tools_id, bg="#00A2E8", font=("Arial", 12, "bold"))
            btn1.grid(column=1,row=20, sticky="W")
            btn2 = Button(app, text="Изменить средство защиты", command=update_tools, bg="#00A2E8", font=("Arial", 12, "bold"))
            btn2.grid(column=1,row=20)


    #кнопка подтверждения
    btn = Button(app, text="Подтвердить", command=update_tools_check_id, bg="#00A2E8", font=("Arial", 12, "bold"))
    btn.grid(column=1,row=17)

        


def show_licenses_table():
    '''Данная кнопка выводит информацию о таблице лицензий из БД'''
    cursor.execute("select * from licenses order by id asc")
    mytable = from_db_cursor(cursor)
    print(mytable)

    #печатаем текст с прокруткой
    txt = Text(app, height=10, width=150,  wrap=WORD)
    txt.grid(row=20, column=1) 
    txt.insert(1.0,mytable) # вставляем информацию из БД
    txt.config(bg='#D9D8D7', state='disabled')
    
    sb = Scrollbar( app, orient=VERTICAL)
    sb.grid(row=20, column=1, sticky=NS+E)
    txt.config(yscrollcommand=sb.set)
    sb.config(command=txt.yview)

    #кнопка добавление данных
    btn = Button(app, text="Добавить", command=add_licenses_table, bg="#FF7F27", font=("Arial", 12, "bold"))
    btn.grid(column=0, row=21)
    #кнопка удаление данных
    btn = Button(app, text="Удалить", command=delete_licenses_table,bg="#FF7F27", font=("Arial", 12, "bold"))
    btn.grid(column=0,row=28)
    #кнопка изменения данных
    btn = Button(app, text="Изменить", command=update_licenses_table, bg="#FF7F27", font=("Arial", 12, "bold"))
    btn.grid(column=0,row=29)

def add_licenses_table():
    '''Данная кнопка дает возможность заполнить таблицу licenses в БД, здесь же есть проверка на ввод данных'''
    #информация по полям ввода
    lbl = Label(app, text="Введите id лицензии (целое число)")
    lbl.grid(column=1, row=21, sticky=W)
    lbl = Label(app, text="Введите id заказчика (целое число)")
    lbl.grid(column=1, row=22, sticky=W)
    lbl = Label(app, text="Введите id средства защиты (целое число)")
    lbl.grid(column=1, row=23, sticky=W)
    lbl = Label(app, text="Введите дату начала лицензии (формат даты: день/месяц/год)")
    lbl.grid(column=1, row=24, sticky=W)
    lbl = Label(app, text="Введите дату окончания лицензии (формат даты: день/месяц/год)")
    lbl.grid(column=1, row=25, sticky=W)
    lbl = Label(app, text="Введите ключ технической поддержки (любое значение)")
    lbl.grid(column=1, row=26, sticky=W)
    lbl = Label(app, text="Введите дату окончания ключа (формат даты: день/месяц/год)")
    lbl.grid(column=1, row=27, sticky=W)

   
    #располагаем поля ввода
    text1 = Entry(app, width=30)
    text1.grid(column=1, row=21)
    text2 = Entry(app, width=30)
    text2.grid(column=1, row=22)
    text3 = Entry(app, width=30)
    text3.grid(column=1, row=23)
    text4 = Entry(app, width=30)
    text4.grid(column=1, row=24)
    text5 = Entry(app, width=30)
    text5.grid(column=1, row=25)
    text6 = Entry(app, width=30)
    text6.grid(column=1, row=26)
    text7 = Entry(app, width=30)
    text7.grid(column=1, row=27)

    def add_information_licenses():
        '''#функция нужна для ввода данных в таблицу лицензий'''
        
        t1 = text1.get() #получаем значения со всех 7 полей
        t2 = text2.get()
        t3 = text3.get()
        t4 = text4.get() 
        t5 = text5.get()
        t6 = text6.get()
        t7 = text7.get()
        k=0 #если 1 поле это число, то k=1
        n=0 #если есть id, то n=1
        cust=0 #если 2 поле это число, то cust=1
        tool=0 #если 3 поле это число, то tool=1
        date=0 #если все 3 даты заполнены правильно, то date=1

        if t1=="" or t2=="" or t3=="" or t4=="" or t5=="" or t6=="" or t7=="": #если одно из поле пустой, то дальше не пойдем
           messagebox.showinfo('Отказано', 'Вы не заполнили все поля')
        else:
            try:
                t1=int(t1) #пробуем конвертировать строку в число, если в строке ввода написали число, то проблем нет
                t2=int(t2)
                t3=int(t3)
                k=1
            except:
                messagebox.showinfo('Отказано', 'Все ID должны быть целыми числами')
            if k: #если в 1,2 и 3 поле числа, то заходим
                
                cursor.execute("select * from licenses") #проверим, есть ли такой id в licenses
                for row in cursor:
                    if t1==row[0]:
                        n=1

                cursor.execute("select * from customer") #проверим, есть ли такой id в customer
                for row in cursor:
                    if t2==row[0]:
                        cust=1

                cursor.execute("select * from tools") #проверим, есть ли такой id в tools
                for row in cursor:
                    if t3==row[0]:
                        tool=1

                if n==1 or cust == 0 or tool == 0: #если ID не уникальный, или если в других таблицах таких значений нет, то ошибка
                    if n==1:
                        messagebox.showinfo('Отказано', 'Запись с таким ID уже есть')
                    elif cust==0:
                        messagebox.showinfo('Отказано', 'Заказчика с таким ID нету')
                    elif tool==0:
                        messagebox.showinfo('Отказано', 'Средство защиты с таким ID нету.')
                else: #если id уникальный и остальные поля в порядке, то записываем его в таблицу БД
                    try:
                        d1 = datetime.strptime(t4, "%d/%m/%Y") #преобразуем три поля ввода в дату
                        d2 = datetime.strptime(t5, "%d/%m/%Y")
                        d3 = datetime.strptime(t7, "%d/%m/%Y")
                        date=1
                    except:
                        messagebox.showinfo('Отказано', 'Дата заполнена не правильно')
                    if date: #если все даты в порядке, то пишем в БД
                        answer = messagebox.askyesno(title="Вопрос", message="Записать данные в таблицу?") #диалоговое окно да/нет
                        if answer:
                            cursor.execute(f"INSERT INTO licenses VALUES ({t1},{t2},{t3},'{t4}','{t5}','{t6}','{t7}')")
                            connection.commit()
                            messagebox.showinfo('Успешно', 'Данные занесены')
    #кнопка для добавления данных в таблицу        
    btn = Button(app, text="Добавить",command=add_information_licenses, bg="#FF7F27", font=("Arial", 12, "bold"))
    btn.grid(row=27, column=1, sticky=E)

def delete_licenses_table():
    '''Данная кнопка будет удалять данные из таблицы licenses по их id'''
    
    #поле с информацией
    lbl = Label(app, text="Введите ID, которое хотите удалить (целое число)")
    lbl.grid(column=1, row=28, sticky=W)
    #поле ввода
    text1 = Entry(app, width=30)
    text1.grid(column=1, row=28)
    
    def delete_information_licenses():
        '''#функция проверит введеное значение и удалит данные по id из licenses'''

        k=0 #проверка ввели ли мы число, если да, то k=1
        n=0 #проврека, есть ли такой id в нашей табличке, есть ли есть, то n=1
        num = text1.get() #получаем строку из поля ввода
        
        try:
            num=int(num) #конвертируем в int
            k=1
        except:
            messagebox.showinfo('Отказано', 'Вы должны ввести целое число')
       
        cursor.execute("select id from licenses") #проверим, есть ли такой id в табличке
        for row in cursor:
            if num == row[0]:
                n=1 #если есть то пишем n=1
        if k: #если это число
            if n: #если оно есть в табличке
                answer = messagebox.askyesno(title="Вопрос", message="Удалить данные из таблицы?") #вопрос подтверждения
                if answer: #если отвечаем да
                    cursor.execute(f"DELETE FROM licenses where ID={num}") #удаляем запись из таблицы
                    connection.commit()
                    messagebox.showinfo('Успешно', 'Удалено')
            else:
                messagebox.showinfo('Отказано', 'Такого ID нет')
        #кнопка удалит данные из таблицы
    btn = Button(app, text="Удалить",command=delete_information_licenses, bg="#FF7F27", font=("Arial", 12, "bold"))
    btn.grid(column=1,row=28, sticky=E)

def update_licenses_table():
    '''Данная кнопка будет изменять данные в таблице licenses'''

    #поле с информацией
    lbl = Label(app, text="Введите ID, где нужно изменить значения (целое число)")
    lbl.grid(column=1, row=29)
    #поле ввода id
    text1 = Entry(app, width=30)
    text1.grid(column=1, row=30)

    def update_licenses_check_id():
        '''Данная кнопка будет проверять есть ли такой id в таблице и в дальнейшем изменять содержимое таблицы'''
        
        k=0 #проверка ввели ли мы число, если да, то k=1
        n=0 #проврека, есть ли такой id в нашей табличке, есть ли есть, то n=1
        num = text1.get() #получаем текст из поля ввода
        
        try:
            num=int(num) #конвертируем в int
            k=1
        except:
            messagebox.showinfo('Отказано', 'Вы должны ввести целое число')

        cursor.execute("select id from licenses") #проверим, есть ли такой id в табличке
        for row in cursor:
            print(row[0], text1.get())
            if num == row[0]:
                n=1 #если есть то пишем n=1

        if k==1 and n==0:
            messagebox.showinfo('Отказано', 'Такого id в таблице нет')
        elif k and n:
            #данный блок будет принимать данные, а затем изменять табличку licenses
            
            #подписи к полям ввода
            lbl1 = Label(app, text="Новое ID (введите целое число)")
            lbl1.grid(column=1, row=32, sticky="W")
            lbl2 = Label(app, text="Введите ID заказчика (введите целое число)")
            lbl2.grid(column=1, row=33, sticky="W")
            lbl3 = Label(app, text="Введите ID средства защиты (введите целое число)")
            lbl3.grid(column=1, row=34, sticky="W")
            lbl4 = Label(app, text="Введите дату начала лицензии (введите дату в формате: день/месяц/год)")
            lbl4.grid(column=1, row=35, sticky="W")
            lbl5 = Label(app, text="Менять дату окончания лицензии (введите дату в формате: день/месяц/год)")
            lbl5.grid(column=1, row=36, sticky="W")
            lbl6 = Label(app, text="Введите ключ технической поддержки (введите любое значение)")
            lbl6.grid(column=1, row=37, sticky="W")
            lbl7 = Label(app, text="Введите дату окончания ключа (введите дату в формате: день/месяц/год)")
            lbl7.grid(column=1, row=38, sticky="W")
            

            #поля ввода
            text2 = Entry(app, width=30)
            text2.grid(column=1, row=32)
            text3 = Entry(app, width=30)
            text3.grid(column=1, row=33)
            text4 = Entry(app, width=30)
            text4.grid(column=1, row=34)
            text5 = Entry(app, width=30)
            text5.grid(column=1, row=35)
            text6 = Entry(app, width=30)
            text6.grid(column=1, row=36)
            text7 = Entry(app, width=30)
            text7.grid(column=1, row=37)
            text8 = Entry(app, width=30)
            text8.grid(column=1, row=38)

            def update_licenses_id():
                '''Данная функция добавит данные в табличку в поле ID'''
                #получаем 2 поле ввода
                t1 = text2.get()

                if t1!="":
                    #если оно не пустые

                    m=0 #проверка на ввод цифр
                    l=0 #проверка на наличие такого id в таблице
                    try:
                        t1=int(t1) #конвертируем в int
                        m=1
                    except:
                        messagebox.showinfo('Отказано', 'Вы должны ввести целое число')
                    
                    cursor.execute("select id from licenses") #проверим, есть ли такой id в табличке
                    for row in cursor:
                        print(row[0], text1.get())
                        if t1 == row[0]:
                            l=1 #если есть то пишем n=1
                            messagebox.showinfo('Отказано', 'Данный id уже занят')
                    if m and l==0:
                        #если все правильно введено, то обновляем id в табличке
                        answer = messagebox.askyesno(title="Вопрос", message="Изменить таблицу?")
                        if answer:
                            cursor.execute(f"UPDATE licenses SET id = {t1} WHERE id = {num}")
                            connection.commit()
                            messagebox.showinfo('Успешно', 'Данные обновлены')
                            
                            text2.grid_remove()
                            text3.grid_remove()
                            text4.grid_remove()
                            text5.grid_remove()
                            text6.grid_remove()
                            text7.grid_remove()
                            text8.grid_remove()
                            lbl1.grid_remove()
                            lbl2.grid_remove()
                            lbl3.grid_remove()
                            lbl4.grid_remove()
                            lbl5.grid_remove()
                            lbl6.grid_remove()
                            lbl7.grid_remove()
                            btn1.grid_remove()
                            btn2.grid_remove()
                else:
                    messagebox.showinfo('Успешно', 'Поле ID пустое')
            def update_licenses_table():
                '''Данная функция изменит в зависимости от поле табличку licenses'''
                count=0 #считаем кол-во добавленных данных
                error=0 #если есть ошибка ввода

                #получаем все поля ввода
                t2 = text3.get()
                t3 = text4.get()
                t4 = text5.get()
                t5 = text6.get()
                t6 = text7.get()
                t7 = text8.get()
                

                check_insert = {"text1":False,"text2":False,"text3":False,"text4":False,"text5":False,"text6":False,} #используем для проверки потом на ввод данных, если какая-то будет true, то запишем данные только для true
                #проверяем каждое поле, если оно не пустое, то потом мы в него запишем данные
                if t2!="":
                    m=0 #проверка на ввод цифр
                    l=0 #проверка на наличие такого id в таблице
                    
                    try:
                        t2=int(t2) #конвертируем в int
                        m=1
                    except:
                        pass
                    
                    cursor.execute("select id from customer") #проверим, есть ли такой id в табличке
                    for row in cursor:
                        print(row[0], text1.get())
                        if t2 == row[0]:
                            l=1 #если есть то пишем n=1
                    if m==0 or l==0:
                        error+=1
                    elif m and l:
                        #если все правильно введено, то обновляем id в табличке
                        check_insert["text1"]=True
                        count+=1      
                if t3!="":
                    m=0 #проверка на ввод цифр
                    l=0 #проверка на наличие такого id в таблице
                    
                    try:
                        t3=int(t3) #конвертируем в int
                        m=1
                    except:
                        pass
                    
                    cursor.execute("select id from tools") #проверим, есть ли такой id в табличке
                    for row in cursor:
                        print(row[0], text1.get())
                        if t3 == row[0]:
                            l=1 #если есть то пишем n=1
                    
                    if m==0 or l==0:
                        error+=1
                    elif m and l:
                        #если все правильно введено, то обновляем id в табличке
                        check_insert["text2"]=True
                        count+=1
                if t4!="":
                    date=0
                    
                    try:
                        d1 = datetime.strptime(t4, "%d/%m/%Y") #преобразуем три поля ввода в дату
                        date=1
                    except:
                        pass
                    if date==0:
                        error+=1
                    elif date:
                        check_insert["text3"]=True
                        count+=1
                if t5!="":
                    date=0
                    
                    try:
                        d2 = datetime.strptime(t5, "%d/%m/%Y") #преобразуем три поля ввода в дату
                        date=1
                    except:
                        pass
                    if date==0:
                        error+=1
                    elif date:
                        check_insert["text4"]=True
                        count+=1
                if t6!="":
                    check_insert["text5"]=True
                    count+=1
                if t7!="":
                    date=0
                    
                    try:
                        d3 = datetime.strptime(t7, "%d/%m/%Y") #преобразуем три поля ввода в дату
                        date=1
                    except:
                        pass
                    if date==0:
                        error+=1
                    elif date:
                        check_insert["text6"]=True
                        count+=1

                if error>0:
                    messagebox.showinfo('Отказ', 'Проврерьте правильность ввода')
                elif count>0:
                    answer = messagebox.askyesno(title="Вопрос", message="Записать данные в таблицу?") #диалоговое окно да/нет
                    if answer:
                        if check_insert["text1"]:
                            cursor.execute(f"UPDATE licenses SET customerid = {t2} WHERE id = {num}")
                        if check_insert["text2"]:
                            cursor.execute(f"UPDATE licenses SET toolid = {t3} WHERE id = {num}")
                        if check_insert["text3"]:
                            cursor.execute(f"UPDATE licenses SET licenses_date_start = '{d1}' WHERE id = {num}")
                        if check_insert["text4"]:
                            cursor.execute(f"UPDATE licenses SET licenses_date_end = '{d2}' WHERE id = {num}")
                        if check_insert["text5"]:
                            cursor.execute(f"UPDATE licenses SET key_techsupport_name = '{t6}' WHERE id = {num}")
                        if check_insert["text6"]:
                            cursor.execute(f"UPDATE licenses SET key_date_end = '{d3}' WHERE id = {num}")
                        connection.commit()
                        messagebox.showinfo('Успешно', 'Данные обновлены')
                else:
                    messagebox.showinfo('Отказ', 'Введите данные')

            #первая кнопка изменит id, вторая изменит остальные данные
            btn1 = Button(app, text="Изменить ID", command=update_licenses_id, bg="#FF7F27", font=("Arial", 12, "bold"))
            btn1.grid(column=1,row=32, sticky="E")
            btn2 = Button(app, text="Изменить все поля", command=update_licenses_table, bg="#FF7F27", font=("Arial", 12, "bold"))
            btn2.grid(column=1,row=33, sticky="E")
           
    #кнопка подтверждения
    btn = Button(app, text="Подтвердить", command=update_licenses_check_id, bg="#FF7F27", font=("Arial", 12, "bold"))
    btn.grid(column=1,row=31)

def button4():

    def choise():
        print(selected.get())
        #получаем данные из БД в зависимости от выбранной пользователем кнопки, 0,3,7,30 дней
        cursor.execute(f"select customer.name_short, tools.license_name, licenses.licenses_date_end from licenses join customer on customer.id = licenses.customerid join tools on tools.id = licenses.toolid where licenses.licenses_date_end - current_date <= {selected.get()} and licenses.licenses_date_end - current_date > 0")
        mytable = from_db_cursor(cursor)
        
        #печатаем таблицы с прокруткой     
        text_box = Text(app, height=10, width=100, font=("Arial", 8), wrap=WORD)
        text_box.grid(row=40, column=1)
        text_box.config(bg='#D9D8D7')
        text_box.insert(1.0,mytable) # вставляем информацию из БД
        sb = Scrollbar( app, orient=VERTICAL)
        sb.grid(row=40, column=2, sticky=NS+W)
        text_box.config(yscrollcommand=sb.set)
        sb.config(command=text_box.yview)

    #выбираем количество дней 1,3,7,30
    lbl = Label(app, text="Выберите количество дней")
    lbl.grid(column=0, row=39)
    selected = IntVar()
    rad1 = Radiobutton(app,text='Сегодня', value=0, variable=selected)  
    rad2 = Radiobutton(app,text='3', value=3, variable=selected)  
    rad3 = Radiobutton(app,text='7', value=7, variable=selected)
    rad4 = Radiobutton(app,text='30', value=30, variable=selected)
    rad1.grid(column=0, row=40,sticky=W)  
    rad2.grid(column=0, row=41,sticky=W)  
    rad3.grid(column=0, row=42,sticky=W)   
    rad4.grid(column=0, row=43,sticky=W)

    #нажав на кнопку, печатаем это все в окне
    btn = Button(app, text="Показать", command=choise, bg="#00A2E8", font=("Arial", 10, "bold"))
    btn.grid(column=0, row=40)
    

    
    #cursor.execute("select customer.name_short, tools.name, licenses.date_end from licenses join customer on customer.id = licenses.customerid join tools on tools.id = licenses.toolid")
    #mytable = from_db_cursor(cursor)
    #print(mytable)
    #lbl = Label(app, text=mytable)
    #lbl.grid(column=1, row=6)


app = Tk()

app.title("Проверка лицензий")
app.iconbitmap("green.ico")
#app["bg"] = "#A349A4"
w = app.winfo_screenwidth()
h = app.winfo_screenheight()
app.geometry('%dx%d+0+0' % (w, h))


#вывод таблицы клиентов
btn = Button(app, text="Показать клиентов", command=show_customer_table, bg="#11A40D", font=("Arial", 12, "bold"))
btn.grid(column=0, row=0)

#выводтаблицы средств защиты
btn = Button(app, text="Показать средства защиты", command=show_tools_table, bg="#00A2E8", font=("Arial", 12, "bold"))
btn.grid(column=0, row=11)

#вывод таблицы лицензий
btn = Button(app, text="Показать даты лицензий", command=show_licenses_table, bg="#FF7F27", font=("Arial", 12, "bold"))
btn.grid(column=0, row=20)


#кнопка показывает истекающие лицензии
btn = Button(app, text="нажмите, чтобы открыть истекающие лицензии!", command=button4, bg="#00A2E8", font=("Arial", 10, "bold"))
btn.grid(column=0, row=37)




app.mainloop()
connection.close()