from tkinter import *
from tkinter.ttk import Notebook
import psycopg2
from prettytable import PrettyTable
from prettytable import from_db_cursor
from datetime import datetime, date
import tkinter
from tkinter import messagebox
from  tkinter import ttk


connection = psycopg2.connect(database="orders_test", user="postgres", password="123456", host="127.0.0.1", port="5432")
cursor = connection.cursor () 
    
mytable = PrettyTable()

cursor.execute("select * from licenses order by id asc")
mytable = from_db_cursor(cursor)
print(mytable)

app = Tk()

app.title("Проверка лицензий")
app.iconbitmap("green.ico")
#app["bg"] = "#A349A4"
w = app.winfo_screenwidth()
h = app.winfo_screenheight()
app.geometry("1000x600+600+200")

notebook = Notebook(app)
notebook.pack(pady=10, expand=True)


frame1 = Frame(notebook, width=980, height=580)
frame2 = Frame(notebook, width=980, height=580)
frame3 = Frame(notebook, width=980, height=580)
frame4 = Frame(notebook, width=980, height=580)

frame1.pack(fill='both', expand=True)
frame2.pack(fill='both', expand=True)
frame3.pack(fill='both', expand=True)
frame4.pack(fill='both', expand=True)

def tab1():
    '''Данная кнопка выводит информацию о таблице клиентов из БД'''
       
    def show_customer_table():
        cursor.execute("select * from customer order by id asc")
        mytable = from_db_cursor(cursor)
    
        #печатаем текст с прокруткой
        txt = Text(frame1, wrap="none", height=15, width=100)
        txt.grid(row=0, column=1) 
        txt.insert(1.0,mytable)
        txt.config(bg='#D9D8D7', state='disabled')

        #вертикальная полоса прокрутки
        sb = Scrollbar(frame1, orient=VERTICAL)
        sb.grid(row=0, column=1, sticky=NS+E)
        txt.config(yscrollcommand=sb.set)
        sb.config(command=txt.yview)
        #горизонтальная полоса прокрутки
        sb2 = Scrollbar( frame1, orient=HORIZONTAL)
        sb2.grid(row=0, column=1, sticky=EW+S)
        txt.config(xscrollcommand=sb2.set)
        sb2.config(command=txt.xview)

    def add_customer_table():
        '''Данная кнопка дает возможность заполнить таблицу customer в БД, здесь же есть проверка на ввод данных'''
        
        app2 = Tk()
        app2.title("Добавление данных")
        app2.geometry("600x100+100+200")
        
        #информация по полям ввода
        Label(app2, text="Введите id заказчика (целое число)").grid(column=0, row=0)
        Label(app2, text="Введите короткое имя заказчика (любте значение)").grid(column=0, row=1)
        Label(app2, text="Введите полное имя заказчика (любое значение)").grid(column=0, row=2)
    
        #располагаем поля ввода
        text1 = Entry(app2, width=10)
        text1.grid(column=1, row=0)
        text2 = Entry(app2, width=30)
        text2.grid(column=1, row=1)
        text3 = Entry(app2, width=30)
        text3.grid(column=1, row=2)
    

        def add_information_customer():
            '''#функция нужна для ввода данных в таблицу клиентов'''
        
            t1 = text1.get() #получаем значения со всех 3 полей
            t2 = text2.get()
            t3 = text3.get()
            k=0 #маркер, изначально 0, но если 1, то данные запишутся в БД
            n=0 #маркер для проверки уникальности id
            if t1=="" or t2=="" or t3=="": #если одно из поле пустой, то дальше не пойдем
                app2.destroy()
                messagebox.showinfo('Отказано', 'Вы не заполнили все поля')
            else:
                try:
                    t1=int(t1) #пробуем конвертировать строку в число, если в строке ввода написали число, то проблем нет
                    k=1
                except:
                    app2.destroy()
                    messagebox.showinfo('Отказано', 'id должно представлять целое число')
                if k: #данные верны, 1 поле это число, остальные два это текст
                    cursor.execute("select * from customer") #проверим, нет ли такого id уже
                    for row in cursor:
                        if t1==row[0] or t2==row[1] or t3==row[2]: #если такой id или имя заказчика уже есть, то пишем ошибку и дальше по коду не идем
                            n=1

                    if n==1:
                        app2.destroy()
                        messagebox.showinfo('Отказано', 'Заказчик с таким именем или id уже существует')
                    else: #если id уникальный, то записываем его в таблицу БД
                        answer = messagebox.askyesno(title="Вопрос", message="Записать данные в таблицу?") #диалоговое окно да/нет
                        if answer:
                            cursor.execute(f"INSERT INTO customer VALUES ({t1},'{t2}','{t3}')")
                            connection.commit()
                            app2.destroy()
                            messagebox.showinfo('Успешно', 'Данные занесены')
                        
        #кнопка для добавления данных в таблицу        
        btn = Button(app2, text="Добавить",command=add_information_customer)
        btn.grid(row=1, column=2, padx=5)

    def delete_customer_table():
        '''Данная кнопка будет удалять данные из таблицы customer по их id'''
        
        app2 = Tk()
        app2.title("Добавление данных")
        app2.geometry("400x100+100+200")
        #поле с информацией
        Label(app2, text="Введите id, которое хотите удалить").grid(column=0, row=0)
        #поле ввода
        text1 = Entry(app2, width=10)
        text1.grid(column=1, row=0)
    
    
        def delete_information_customer():
            '''#функция проверит введеное значение и удалит данные по id из customer'''
            t1 = text1.get()
            k=0 #проверка ввели ли мы число, если да, то k=1
            n=0 #проврека, есть ли такой id в нашей табличке, есть ли есть, то n=1
        
            try:
                t1=int(t1) #конвертируем в int
                k=1
            except:
                app2.destroy()
                messagebox.showinfo('Отказано', 'Вы должны ввести целое число')
       
            cursor.execute("select id from customer") #проверим, есть ли такой id в табличке
            for row in cursor:
                if t1 == row[0]:
                    n=1 #если есть то пишем n=1

            if k: #если это число
                if n: #если оно есть в табличке
                    answer = messagebox.askyesno(title="Вопрос", message="Удалить данные из таблицы?\nВнимание, все дочерние записи из других таблиц тоже удалятся") #вопрос подтверждения
                    if answer: #если отвечаем да
                        cursor.execute(f"DELETE FROM customer where ID={t1}") #удаляем запись из таблицы
                        connection.commit()
                        app2.destroy()
                        messagebox.showinfo('Успешно', 'Удалено')
                else:
                    app2.destroy()
                    messagebox.showinfo('Отказано', 'Такого id нет')
    
        #кнопка удалит данные из таблицы
        btn = Button(app2, text="Удалить",command=delete_information_customer)
        btn.grid(column=2,row=0, padx=5)

    def update_customer_table():
        '''Данная кнопка будет изменять данные в таблице customer'''
        app2 = Tk()
        app2.title("Добавление данных")
        app2.geometry("600x200+100+200")
        #поле с информацией
        Label(app2, text="Введите id, где нужно изменить значения").grid(column=0, row=0)
        #поле ввода id
        text1 = Entry(app2, width=10)
        text1.grid(column=1, row=0)
    
        def update_customer_check_id():
            '''Данная кнопка будет проверять есть ли такой id в таблице и в дальнейшем изменять содержимое таблицы'''
            t1 = text1.get()
            k=0 #проверка ввели ли мы число, если да, то k=1
            n=0 #проврека, есть ли такой id в нашей табличке, есть ли есть, то n=1
            
            try:
                t1=int(t1) #конвертируем в int
                k=1
            except:
                app2.destroy()
                messagebox.showinfo('Отказано', 'Вы должны ввести целое число')

            cursor.execute("select id from customer") #проверим, есть ли такой id в табличке
            for row in cursor:
                if t1 == row[0]:
                    n=1 #если есть то пишем n=1

            if k==1 and n==0:
                app2.destroy()
                messagebox.showinfo('Отказано', 'Такого id в таблице нет')
            elif k and n:
                #данный блок будет принимать данные, а затем изменять табличку customer

                #подписи к полям ввода
                Label(app2, text="Введите новое id").grid(column=0, row=1)
                Label(app2, text="Введите сокращенное имя заказчика").grid(column=2, row=1)
                Label(app2, text="Введите полное имя заказчика").grid(column=2, row=3)

                #поля ввода
                text2 = Entry(app2, width=10)
                text2.grid(column=0, row=2)
                text3 = Entry(app2, width=30)
                text3.grid(column=2, row=2)
                text4 = Entry(app2, width=30)
                text4.grid(column=2, row=4)
            

                def update_customer_id():
                    '''Данная функция добавит данные в табличку в поле ID'''
                    #получаем 2 поле ввода
                    t2 = text2.get()

                    if t2!="":
                        #если оно не пустые

                        m=0 #проверка на ввод цифр
                        l=0 #проверка на наличие такого id в таблице
                        try:
                            t2=int(t2) #конвертируем в int
                            m=1
                        except:
                            app2.destroy()
                            messagebox.showinfo('Отказано', 'Вы должны ввести целое число')
                    
                        cursor.execute("select id from customer") #проверим, есть ли такой id в табличке
                        for row in cursor:
                            print(row[0], text1.get())
                            if t2 == row[0]:
                                l=1 #если есть то пишем n=1
                                app2.destroy()
                                messagebox.showinfo('Отказано', 'Данный id уже занят')
                        if m and l==0:
                            #если все правильно введено, то обновляем id в табличке
                            answer = messagebox.askyesno(title="Вопрос", message="Изменить таблицу?")
                            if answer:
                                cursor.execute(f"UPDATE customer SET id = {t2} WHERE id = {t1}")
                                connection.commit()
                                app2.destroy()
                                messagebox.showinfo('Успешно', 'Данные обновлены')
                    else:
                        app2.destroy()
                        messagebox.showinfo('Отказано', 'Поле ID пустое')
                def update_customer():
                    '''Данная функция добавит данные в табличку, если пользователь ввел id, либо имена заказчика'''
                    #получаем два поля ввода
                    t3 = text3.get()
                    t4 = text4.get()
                

                    if t3!="" and t4!="" :
                        #если оба поля не пустые
                        answer = messagebox.askyesno(title="Вопрос", message="Изменить имена заказчиков?")
                        if answer:
                            cursor.execute(f"UPDATE customer SET name_short = '{t3}' WHERE id = {t1}")
                            cursor.execute(f"UPDATE customer SET name_full = '{t4}' WHERE id = {t1}")
                            connection.commit()
                            app2.destroy()
                            messagebox.showinfo('Успешно', 'Данные обновлены')
                    else:
                        app2.destroy()
                        messagebox.showinfo('Отказано', 'Заполните оба поля имени заказчика')


                #данная кнопка добавит данные в табличку
                btn1 = Button(app2, text="Изменить ID", command=update_customer_id)
                btn1.grid(column=0,row=3)
                btn2 = Button(app2, text="Изменить имена заказчиков", command=update_customer)
                btn2.grid(column=2,row=5)

        #кнопка подтверждения
        Button(app2, text="Подтвердить", command=update_customer_check_id).grid(column=2,row=0, padx=5)
    

    #кнопка добавление данных
    btn = Button(frame1, text="Показать таблицу", command=show_customer_table)
    btn.grid(column=0, row=0)
    #кнопка добавление данных
    btn = Button(frame1, text="Добавить", command=add_customer_table)
    btn.grid(column=0, row=1)
    #кнопка удаление данных
    btn = Button(frame1, text="Удалить", command=delete_customer_table)
    btn.grid(column=0,row=2)
    #кнопка изменения данных
    btn = Button(frame1, text="Изменить", command=update_customer_table)
    btn.grid(column=0,row=3)
  

def tab2():
    '''все о таблице tools'''

    def show_tools_table():
        cursor.execute("select * from tools order by id asc")
        mytable = from_db_cursor(cursor)
    
        #печатаем текст с прокруткой
        txt = Text(frame2, wrap="none", height=15, width=100)
        txt.grid(row=0, column=1) 
        txt.insert(1.0,mytable)
        txt.config(bg='#D9D8D7', state='disabled')

        #вертикальная полоса прокрутки
        sb = Scrollbar(frame2, orient=VERTICAL)
        sb.grid(row=0, column=1, sticky=NS+E)
        txt.config(yscrollcommand=sb.set)
        sb.config(command=txt.yview)
        #горизонтальная полоса прокрутки
        sb2 = Scrollbar( frame2, orient=HORIZONTAL)
        sb2.grid(row=0, column=1, sticky=EW+S)
        txt.config(xscrollcommand=sb2.set)
        sb2.config(command=txt.xview)
    
    def add_tools_table():
        '''Данная кнопка дает возможность заполнить таблицу tools в БД, здесь же есть проверка на ввод данных'''
    
        app2 = Tk()
        app2.title("Добавление данных")
        app2.geometry("400x100+100+200")
        
        #информация по полям ввода
        Label(app2, text="Новое ID (целое число)").grid(column=0, row=0)
        Label(app2, text="Новое средство защиты").grid(column=0, row=1)

        #располагаем поля ввода
        text1 = Entry(app2, width=30)
        text1.grid(column=1, row=0)
        text2 = Entry(app2, width=30)
        text2.grid(column=1, row=1)

        def add_information_tools():
            '''#функция нужна для ввода данных в таблицу средств защиты'''
        
            t1 = text1.get() #получаем значения с 2 полей
            t2 = text2.get()
            k=0 #маркер, изначально 0, но если 1, то данные запишутся в БД
            n=0 #маркер для проверки уникальности id
            if t1=="" or t2=="": #если одно из полей пустое, то дальше не пойдем
                app2.destroy()
                messagebox.showinfo('Отказано', 'Вы не заполнили все поля')
               
            else:
                try:
                    t1=int(t1) #пробуем конвертировать строку в число, если в строке ввода написали число, то проблем нет
                    k=1
                except:
                    app2.destroy()
                    messagebox.showinfo('Отказано', 'id должно представлять целое число')
                    
                if k: #данные верны, 1 поле это число, второе поле это текст
                    cursor.execute("select * from tools") #проверим, нет ли такого id уже
                    for row in cursor:
                        if t1==row[0] or t2==row[1]: #если такой id есть или средство защиты уже есть, то пишем ошибку и дальше по коду не идем
                            n=1
                    if n==1:
                        app2.destroy()
                        messagebox.showinfo('Отказано', 'Такое средство защиты или его id уже существует')
                        
                    else: #если id уникальный, то записываем его в таблицу БД
                        answer = messagebox.askyesno(title="Вопрос", message="Записать данные в таблицу?") #диалоговое окно да/нет
                        if answer:
                            cursor.execute(f"INSERT INTO tools VALUES ({t1},'{t2}')")
                            connection.commit()
                            app2.destroy()
                            messagebox.showinfo('Успешно', 'Данные занесены')
                            
                          
        #кнопка для добавления данных в таблицу        
        btn = Button(app2, text="Добавить",command=add_information_tools)
        btn.grid(row=0, column=2, padx=5)
          
    def delete_tools_table():
        '''Данная кнопка будет удалять данные из таблицы tools по их id'''
        app2 = Tk()
        app2.title("Удаление")
        app2.geometry("400x100+100+200")
        
        #поле с информацией
        Label(app2, text="Введите id, которое хотите удалить").grid(column=0, row=0)
        #поле ввода
        text1 = Entry(app2, width=10)
        text1.grid(column=1, row=0)

        def delete_information_tools():
            '''#функция проверит введеное значение и удалит данные по id из tools'''
            t1 = text1.get() #получаем строку из поля ввода
            k=0 #проверка ввели ли мы число, если да, то k=1
            n=0 #проврека, есть ли такой id в нашей табличке, есть ли есть, то n=1

            try:
                t1=int(t1) #конвертируем в int
                k=1
            except:
                app2.destroy()
                messagebox.showinfo('Отказано', 'Вы должны ввести целое число')
                

            cursor.execute("select id from tools") #проверим, есть ли такой id в табличке
            for row in cursor:
                if t1 == row[0]:
                    n=1 #если есть то пишем n=1
        
            if k: #если это число
                if n: #если оно есть в табличке
                    answer = messagebox.askyesno(title="Вопрос", message="Удалить данные? Все дочерние записи из других таблиц тоже удалятся") #вопрос подтверждение
                    if answer:  #если отвечаем да
                        cursor.execute(f"DELETE FROM tools where ID={t1}") #удаляем запись из таблицы
                        connection.commit()
                        messagebox.showinfo('Успешно', 'Удалено')
                        app2.destroy()
                        
                else:
                    app2.destroy()
                    messagebox.showinfo('Отказано', 'Такого id нет')
                    
            

        #кнопка удалит данные из таблицы
        btn = Button(app2, text="Удалить",command=delete_information_tools)
        btn.grid(column=2,row=0, padx=5)

    def update_tools_table():
        '''Данная кнопка будет изменять данные в таблице tools'''
        
        app2 = Tk()
        app2.title("Проверка лицензий")
        app2.geometry("600x200+100+200")

        #поле с информацией
        Label(app2, text="Введите id, где нужно изменить значения").grid(column=0, row=0)
        #поле ввода id
        text1 = Entry(app2, width=10)
        text1.grid(column=1, row=0)

        def update_tools_check_id():
            '''Данная кнопка будет проверять есть ли такой id в таблице и в дальнейшем изменять содержимое таблицы'''
            t1 = text1.get() #получаем текст из поля ввода
            k=0 #если мы ввели число, то k=1
            n=0 #если такой id есть, то n=1
            

            try:
                t1=int(t1) #конвертируем в int
                k=1
            except:
                app2.destroy()
                messagebox.showinfo('Отказано', 'Вы должны ввести целое число')
                
        
            cursor.execute("select id from tools") #проверим, есть ли такой id в табличке
            for row in cursor:
                
                if t1 == row[0]:
                    n=1 #если есть то пишем n=1

            if k==1 and n==0:
                app2.destroy()
                messagebox.showinfo('Отказано', 'Такого id в таблице нет')
                
            elif k and n:
                #данный блок будет принимать данные, а затем изменять табличку tools
            
                #подписи к полям ввода
                Label(app2, text="Введите новое id").grid(column=0, row=1)
                Label(app2, text="Введите название средства защиты").grid(column=1, row=1)

                #поля ввода
                text2 = Entry(app2, width=10)
                text2.grid(column=0, row=2)
                text3 = Entry(app2, width=30)
                text3.grid(column=1, row=2)

                def update_tools_id():
                    '''Данная функция добавит данные в табличку в поле ID'''
                    #получаем 2 поле ввода
                    t2 = text2.get()

                    if t2!="":
                        #если оно не пустые

                        m=0 #проверка на ввод цифр
                        l=0 #проверка на наличие такого id в таблице
                        try:
                            t2=int(t2) #конвертируем в int
                            m=1
                        except:
                            app2.destroy()
                            messagebox.showinfo('Отказано', 'Вы должны ввести целое число')
                            
                    
                        cursor.execute("select id from tools") #проверим, есть ли такой id в табличке
                        for row in cursor:
                            if t2 == row[0]:
                                l=1 #если есть то пишем n=1
                                app2.destroy()
                                messagebox.showinfo('Отказано', 'Данный id уже занят')
                                
                        if m and l==0:
                            #если все правильно введено, то обновляем id в табличке
                            answer = messagebox.askyesno(title="Вопрос", message="Изменить таблицу?")
                            if answer:
                                cursor.execute(f"UPDATE tools SET id = {t2} WHERE id = {t1}")
                                connection.commit()
                                app2.destroy()
                                messagebox.showinfo('Успешно', 'Данные обновлены')
                                
                                
                                
                    else:
                        app2.destroy()
                        messagebox.showinfo('Отказ', 'Поле ID пустое')
                        
                    
                def update_tools():
                    '''Данная функция добавит данные в табличку, если пользователь ввел id, либо поле средста защиты'''
                    t3 = text3.get()
                
                    if t3!="":
                        #если оба поля не пустые
                        answer = messagebox.askyesno(title="Вопрос", message="Изменить данные?")
                        if answer:
                            cursor.execute(f"UPDATE tools SET license_name = '{t3}' WHERE id = {t1}")
                            connection.commit()
                            app2.destroy()
                            messagebox.showinfo('Успешно', 'Данные обновлены')
                            
                    else:
                        app2.destroy()
                        messagebox.showinfo('Отказано', 'Заполните поле')
                        


                #данная кнопка добавит данные в табличку
                btn1 = Button(app2, text="Изменить ID", command=update_tools_id)
                btn1.grid(column=0,row=3, pady=5)
                btn2 = Button(app2, text="Изменить средство защиты", command=update_tools)
                btn2.grid(column=1,row=3, pady=5)

            

        #кнопка подтверждения
        btn = Button(app2, text="Подтвердить", command=update_tools_check_id)
        btn.grid(column=2,row=0, padx=5)
        
    
        
    btn = Button(frame2, text="Показать средства защиты", command=show_tools_table)
    btn.grid(column=0, row=0)
    #кнопка добавление данных
    btn = Button(frame2, text="Добавить", command=add_tools_table)
    btn.grid(column=0, row=1)
    #кнопка удаление данных
    btn = Button(frame2, text="Удалить", command=delete_tools_table)
    btn.grid(column=0,row=2)
    #кнопка изменения данных
    btn = Button(frame2, text="Изменить", command=update_tools_table)
    btn.grid(column=0,row=3)


def tab3():
    '''Данная кнопка выводит информацию о таблице лицензий из БД'''

    def show_customer_table():
        app2 = Tk()
        app2.title("Проверка лицензий")
        app2.geometry("600x200+0+400")
        cursor.execute("select * from customer order by id asc")
        mytable = from_db_cursor(cursor)
    
        #печатаем текст с прокруткой
        txt = Text(app2, wrap="none", height=13, width=80)
        txt.grid(row=0, column=0) 
        txt.insert(1.0,mytable)
        txt.config(bg='#D9D8D7', state='disabled')

        #вертикальная полоса прокрутки
        sb = Scrollbar(app2, orient=VERTICAL)
        sb.grid(row=0, column=0, sticky=NS+E)
        txt.config(yscrollcommand=sb.set)
        sb.config(command=txt.yview)
        #горизонтальная полоса прокрутки
        sb2 = Scrollbar( app2, orient=HORIZONTAL)
        sb2.grid(row=0, column=0, sticky=EW+S)
        txt.config(xscrollcommand=sb2.set)
        sb2.config(command=txt.xview)

    def show_tools_table():
        app2 = Tk()
        app2.title("Проверка лицензий")
        app2.geometry("600x200+0+630")
        cursor.execute("select * from tools order by id asc")
        mytable = from_db_cursor(cursor)
    
        #печатаем текст с прокруткой
        txt = Text(app2, wrap="none", height=13, width=80)
        txt.grid(row=0, column=0) 
        txt.insert(1.0,mytable)
        txt.config(bg='#D9D8D7', state='disabled')

        #вертикальная полоса прокрутки
        sb = Scrollbar(app2, orient=VERTICAL)
        sb.grid(row=0, column=0, sticky=NS+E)
        txt.config(yscrollcommand=sb.set)
        sb.config(command=txt.yview)
        #горизонтальная полоса прокрутки
        sb2 = Scrollbar( app2, orient=HORIZONTAL)
        sb2.grid(row=0, column=0, sticky=EW+S)
        txt.config(xscrollcommand=sb2.set)
        sb2.config(command=txt.xview)

    def show_licenses_table():
        cursor.execute("select * from licenses order by id asc")
        mytable = from_db_cursor(cursor)
    
        #печатаем текст с прокруткой
        txt = Text(frame3, wrap="none", height=12, width=100)
        txt.grid(row=0, column=1) 
        txt.insert(1.0,mytable)
        txt.config(bg='#D9D8D7', state='disabled')

        #вертикальная полоса прокрутки
        sb = Scrollbar(frame3, orient=VERTICAL)
        sb.grid(row=0, column=1, sticky=NS+E)
        txt.config(yscrollcommand=sb.set)
        sb.config(command=txt.yview)
        #горизонтальная полоса прокрутки
        sb2 = Scrollbar( frame3, orient=HORIZONTAL)
        sb2.grid(row=0, column=1, sticky=EW+S)
        txt.config(xscrollcommand=sb2.set)
        sb2.config(command=txt.xview)

    def add_licenses_table():
        '''Данная кнопка дает возможность заполнить таблицу licenses в БД, здесь же есть проверка на ввод данных'''
        app2 = Tk()
        app2.title("Проверка лицензий")
        app2.geometry("600x200+50+150")

        #информация по полям ввода
        Label(app2, text="Введите id лицензии (целое число)").grid(column=0, row=0)
        Label(app2, text="Введите id заказчика (целое число)").grid(column=0, row=1)
        Label(app2, text="Введите id средства защиты (целое число)").grid(column=0, row=2)
        Label(app2, text="Введите дату начала лицензии (формат даты: день/месяц/год)").grid(column=0, row=3)
        Label(app2, text="Введите дату окончания лицензии (формат даты: день/месяц/год)").grid(column=0, row=4)
        Label(app2, text="Введите ключ технической поддержки (любое значение)").grid(column=0, row=5)
        Label(app2, text="Введите дату окончания ключа (формат даты: день/месяц/год)").grid(column=0, row=6)

   
        #располагаем поля ввода
        text1 = Entry(app2, width=10)
        text1.grid(column=1, row=0)
        text2 = Entry(app2, width=10)
        text2.grid(column=1, row=1)
        text3 = Entry(app2, width=10)
        text3.grid(column=1, row=2)
        text4 = Entry(app2, width=10)
        text4.grid(column=1, row=3)
        text5 = Entry(app2, width=10)
        text5.grid(column=1, row=4)
        text6 = Entry(app2, width=10)
        text6.grid(column=1, row=5)
        text7 = Entry(app2, width=10)
        text7.grid(column=1, row=6)

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
                app2.destroy()
                messagebox.showinfo('Отказано', 'Вы не заполнили все поля')
            else:
                try:
                    t1=int(t1) #пробуем конвертировать строку в число, если в строке ввода написали число, то проблем нет
                    t2=int(t2)
                    t3=int(t3)
                    k=1
                except:
                    app2.destroy()
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
                            app2.destroy()
                            messagebox.showinfo('Отказано', 'Запись с таким ID уже есть')
                        elif cust==0:
                            app2.destroy()
                            messagebox.showinfo('Отказано', 'Заказчика с таким ID нету')
                        elif tool==0:
                            app2.destroy()
                            messagebox.showinfo('Отказано', 'Средство защиты с таким ID нету.')
                    else: #если id уникальный и остальные поля в порядке, то записываем его в таблицу БД
                        try:
                            d1 = datetime.strptime(t4, "%d/%m/%Y") #преобразуем три поля ввода в дату
                            d2 = datetime.strptime(t5, "%d/%m/%Y")
                            d3 = datetime.strptime(t7, "%d/%m/%Y")
                            date=1
                        except:
                            app2.destroy()
                            messagebox.showinfo('Отказано', 'Дата заполнена не правильно')
                        if date: #если все даты в порядке, то пишем в БД
                            answer = messagebox.askyesno(title="Вопрос", message="Записать данные в таблицу?") #диалоговое окно да/нет
                            if answer:
                                cursor.execute(f"INSERT INTO licenses VALUES ({t1},{t2},{t3},'{t4}','{t5}','{t6}','{t7}')")
                                connection.commit()
                                app2.destroy()
                                messagebox.showinfo('Успешно', 'Данные занесены')
        #кнопка для добавления данных в таблицу        
        Button(app2, text="Добавить",command=add_information_licenses).grid(row=6, column=2,padx=5)

    def delete_licenses_table():
        '''Данная кнопка будет удалять данные из таблицы licenses по их id'''
        app2 = Tk()
        app2.title("Проверка лицензий")
        app2.geometry("400x100+50+150")

        #поле с информацией
        Label(app2, text="Введите ID, которое хотите удалить").grid(column=0, row=0)
        #поле ввода
        text1 = Entry(app2, width=10)
        text1.grid(column=1, row=0)
    
        def delete_information_licenses():
            '''#функция проверит введеное значение и удалит данные по id из licenses'''
            t1 = text1.get()
            k=0 #проверка ввели ли мы число, если да, то k=1
            n=0 #проврека, есть ли такой id в нашей табличке, есть ли есть, то n=1
           
        
            try:
                t1=int(t1) #конвертируем в int
                k=1
            except:
                app2.destroy()
                messagebox.showinfo('Отказано', 'Вы должны ввести целое число')
       
            cursor.execute("select id from licenses") #проверим, есть ли такой id в табличке
            for row in cursor:
                if t1 == row[0]:
                    n=1 #если есть то пишем n=1
            if k: #если это число
                if n: #если оно есть в табличке
                    answer = messagebox.askyesno(title="Вопрос", message="Удалить данные из таблицы?") #вопрос подтверждения
                    if answer: #если отвечаем да
                        cursor.execute(f"DELETE FROM licenses where ID={t1}") #удаляем запись из таблицы
                        connection.commit()
                        app2.destroy()
                        messagebox.showinfo('Успешно', 'Удалено')
                else:
                    app2.destroy()
                    messagebox.showinfo('Отказано', 'Такого ID нет')
            #кнопка удалит данные из таблицы
        Button(app2, text="Удалить",command=delete_information_licenses).grid(column=2,row=0,padx=5)

    def update_licenses_table():
        '''Данная кнопка будет изменять данные в таблице licenses'''
        app2 = Tk()
        app2.title("Проверка лицензий")
        app2.geometry("900x200+50+150")

        #поле с информацией
        Label(app2, text="Введите ID, где нужно изменить значения (целое число)").grid(column=0, row=0)
        #поле ввода id
        text1 = Entry(app2, width=10)
        text1.grid(column=1, row=0)

        def update_licenses_check_id():
            '''Данная кнопка будет проверять есть ли такой id в таблице и в дальнейшем изменять содержимое таблицы'''
        
            k=0 #проверка ввели ли мы число, если да, то k=1
            n=0 #проврека, есть ли такой id в нашей табличке, есть ли есть, то n=1
            t1 = text1.get() #получаем текст из поля ввода
        
            try:
                t1=int(t1) #конвертируем в int
                k=1
            except:
                app2.destroy()
                messagebox.showinfo('Отказано', 'Вы должны ввести целое число')

            cursor.execute("select id from licenses") #проверим, есть ли такой id в табличке
            for row in cursor:
                if t1 == row[0]:
                    n=1 #если есть то пишем n=1

            if k==1 and n==0:
                app2.destroy()
                messagebox.showinfo('Отказано', 'Такого id в таблице нет')
            elif k and n:
                #данный блок будет принимать данные, а затем изменять табличку licenses
            
                #подписи к полям ввода
                Label(app2, text="Новое ID (введите целое число)").grid(column=0, row=1)
                Label(app2, text="Введите ID заказчика (введите целое число)").grid(column=1, row=1)
                Label(app2, text="Введите ID средства защиты (введите целое число)").grid(column=1, row=2)
                Label(app2, text="Введите дату начала лицензии (введите дату в формате: день/месяц/год)").grid(column=1, row=3)
                Label(app2, text="Менять дату окончания лицензии (введите дату в формате: день/месяц/год)").grid(column=1, row=4)
                Label(app2, text="Введите ключ технической поддержки (введите любое значение)").grid(column=1, row=5)
                Label(app2, text="Введите дату окончания ключа (введите дату в формате: день/месяц/год)").grid(column=1, row=6)
            

                #поля ввода
                text2 = Entry(app2, width=10)
                text2.grid(column=0, row=2)
                text3 = Entry(app2, width=10)
                text3.grid(column=2, row=1)
                text4 = Entry(app2, width=10)
                text4.grid(column=2, row=2)
                text5 = Entry(app2, width=20)
                text5.grid(column=2, row=3)
                text6 = Entry(app2, width=20)
                text6.grid(column=2, row=4)
                text7 = Entry(app2, width=20)
                text7.grid(column=2, row=5)
                text8 = Entry(app2, width=20)
                text8.grid(column=2, row=6)

                def update_licenses_id():
                    '''Данная функция добавит данные в табличку в поле ID'''
                    #получаем 2 поле ввода
                    t2 = text2.get()

                    if t2!="":
                        #если оно не пустые

                        m=0 #проверка на ввод цифр
                        l=0 #проверка на наличие такого id в таблице
                        try:
                            t2=int(t2) #конвертируем в int
                            m=1
                        except:
                            app2.destroy()
                            messagebox.showinfo('Отказано', 'Вы должны ввести целое число')
                    
                        cursor.execute("select id from licenses") #проверим, есть ли такой id в табличке
                        for row in cursor:
                            print(row[0], text1.get())
                            if t2 == row[0]:
                                l=1 #если есть то пишем n=1
                                app2.destroy()
                                messagebox.showinfo('Отказано', 'Данный id уже занят')
                        if m and l==0:
                            #если все правильно введено, то обновляем id в табличке
                            answer = messagebox.askyesno(title="Вопрос", message="Изменить таблицу?")
                            if answer:
                                cursor.execute(f"UPDATE licenses SET id = {t2} WHERE id = {t1}")
                                connection.commit()
                                app2.destroy()
                                messagebox.showinfo('Успешно', 'Данные обновлены')

                    else:
                        messagebox.showinfo('Успешно', 'Поле ID пустое')
                def update_licenses_table():
                    '''Данная функция изменит в зависимости от поле табличку licenses'''
                    count=0 #считаем кол-во добавленных данных
                    error=0 #если есть ошибка ввода

                    #получаем все поля ввода
                    t3 = text3.get()
                    t4 = text4.get()
                    t5 = text5.get()
                    t6 = text6.get()
                    t7 = text7.get()
                    t8 = text8.get()
                

                    check_insert = {"text1":False,"text2":False,"text3":False,"text4":False,"text5":False,"text6":False,} #используем для проверки потом на ввод данных, если какая-то будет true, то запишем данные только для true
                    #проверяем каждое поле, если оно не пустое, то потом мы в него запишем данные
                    if t3!="":
                        m=0 #проверка на ввод цифр
                        l=0 #проверка на наличие такого id в таблице
                    
                        try:
                            t3=int(t3) #конвертируем в int
                            m=1
                        except:
                            pass
                    
                        cursor.execute("select id from customer") #проверим, есть ли такой id в табличке
                        for row in cursor:
                            print(row[0], text1.get())
                            if t3 == row[0]:
                                l=1 #если есть то пишем n=1
                        if m==0 or l==0:
                            error+=1
                        elif m and l:
                            #если все правильно введено, то обновляем id в табличке
                            check_insert["text1"]=True
                            count+=1      
                    if t4!="":
                        m=0 #проверка на ввод цифр
                        l=0 #проверка на наличие такого id в таблице
                    
                        try:
                            t4=int(t4) #конвертируем в int
                            m=1
                        except:
                            pass
                    
                        cursor.execute("select id from tools") #проверим, есть ли такой id в табличке
                        for row in cursor:
                            print(row[0], text1.get())
                            if t4 == row[0]:
                                l=1 #если есть то пишем n=1
                    
                        if m==0 or l==0:
                            error+=1
                        elif m and l:
                            #если все правильно введено, то обновляем id в табличке
                            check_insert["text2"]=True
                            count+=1
                    if t5!="":
                        date=0
                    
                        try:
                            d1 = datetime.strptime(t5, "%d/%m/%Y") #преобразуем три поля ввода в дату
                            date=1
                        except:
                            pass
                        if date==0:
                            error+=1
                        elif date:
                            check_insert["text3"]=True
                            count+=1
                    if t6!="":
                        date=0
                    
                        try:
                            d2 = datetime.strptime(t6, "%d/%m/%Y") #преобразуем три поля ввода в дату
                            date=1
                        except:
                            pass
                        if date==0:
                            error+=1
                        elif date:
                            check_insert["text4"]=True
                            count+=1
                    if t7!="":
                        check_insert["text5"]=True
                        count+=1
                    if t8!="":
                        date=0
                    
                        try:
                            d3 = datetime.strptime(t8, "%d/%m/%Y") #преобразуем три поля ввода в дату
                            date=1
                        except:
                            pass
                        if date==0:
                            error+=1
                        elif date:
                            check_insert["text6"]=True
                            count+=1

                    if error>0:
                        app2.destroy()
                        messagebox.showinfo('Отказ', 'Проврерьте правильность ввода')
                    elif count>0:
                        answer = messagebox.askyesno(title="Вопрос", message="Записать данные в таблицу?") #диалоговое окно да/нет
                        if answer:
                            if check_insert["text1"]:
                                cursor.execute(f"UPDATE licenses SET customerid = {t3} WHERE id = {t1}")
                            if check_insert["text2"]:
                                cursor.execute(f"UPDATE licenses SET toolid = {t4} WHERE id = {t1}")
                            if check_insert["text3"]:
                                cursor.execute(f"UPDATE licenses SET licenses_date_start = '{d1}' WHERE id = {t1}")
                            if check_insert["text4"]:
                                cursor.execute(f"UPDATE licenses SET licenses_date_end = '{d2}' WHERE id = {t1}")
                            if check_insert["text5"]:
                                cursor.execute(f"UPDATE licenses SET key_techsupport_name = '{t7}' WHERE id = {t1}")
                            if check_insert["text6"]:
                                cursor.execute(f"UPDATE licenses SET key_date_end = '{d3}' WHERE id = {t1}")
                            connection.commit()
                            app2.destroy()
                            messagebox.showinfo('Успешно', 'Данные обновлены')
                    else:
                        app2.destroy()
                        messagebox.showinfo('Отказ', 'Введите данные')

                #первая кнопка изменит id, вторая изменит остальные данные
                Button(app2, text="Изменить ID", command=update_licenses_id).grid(column=0,row=3)
                Button(app2, text="Изменить все поля", command=update_licenses_table).grid(column=2,row=7)
           
        #кнопка подтверждения
        Button(app2, text="Подтвердить", command=update_licenses_check_id).grid(column=2,row=0,padx=5)

    
    
    #Показать данные
    Button(frame3, text="Показать лицензии", command=show_licenses_table).grid(column=0, row=0)
    #Добавить
    Button(frame3, text="Добавить", command=add_licenses_table).grid(column=0, row=1)
    #Удалить
    Button(frame3, text="Удалить", command=delete_licenses_table).grid(column=0,row=2)
    #Изменить
    Button(frame3, text="Изменить", command=update_licenses_table).grid(column=0,row=3)
    Button(frame3, text="Показать клиентов", command=show_customer_table).grid(column=0, row=4)
    Button(frame3, text="Показать средства защиты", command=show_tools_table).grid(column=0, row=5)


def tab4():

    def choise():
        text_box = Text(frame4, height=10, width=100, wrap=WORD)
        text_box.grid_remove()
        
        print(selected.get())
        row="" #проверка на пустую таблицу
        cursor.execute(f"select customer.name_short, tools.license_name, licenses.licenses_date_end from licenses join customer on customer.id = licenses.customerid join tools on tools.id = licenses.toolid where licenses.licenses_date_end - current_date <= {selected.get()} and licenses.licenses_date_end - current_date > 0")
        for row in cursor:
            pass

        if row=="":
            Label(frame4, text="Таблица пуста").grid(row=0,column=0)
        else:
            #получаем данные из БД в зависимости от выбранной пользователем кнопки, 0,3,7,30 дней
            cursor.execute(f"select customer.name_short, tools.license_name, licenses.licenses_date_end from licenses join customer on customer.id = licenses.customerid join tools on tools.id = licenses.toolid where licenses.licenses_date_end - current_date <= {selected.get()} and licenses.licenses_date_end - current_date > 0")
            mytable = from_db_cursor(cursor)
        
            #печатаем таблицы с прокруткой     
            text_box = Text(frame4, height=10, width=100)
            text_box.grid(row=0, column=0)
            text_box.config(bg='#D9D8D7')
            text_box.insert(1.0,mytable) # вставляем информацию из БД
            
            sb = Scrollbar( frame4, orient=VERTICAL)
            sb.grid(row=0, column=0, sticky=NS+E)
            text_box.config(yscrollcommand=sb.set)
            sb.config(command=text_box.yview)
            
            sb2 = Scrollbar( frame4, orient=HORIZONTAL)
            sb2.grid(row=0, column=0, sticky=EW+S)
            text_box.config(xscrollcommand=sb2.set)
            sb2.config(command=text_box.xview)

    #выбираем количество дней 1,3,7,30
    lbl = Label(frame4, text="Выберите количество дней")
    lbl.grid(column=0, row=1)
    selected = IntVar()
    rad1 = Radiobutton(frame4,text='Сегодня', value=0, variable=selected)  
    rad2 = Radiobutton(frame4,text='3', value=3, variable=selected)  
    rad3 = Radiobutton(frame4,text='7', value=7, variable=selected)
    rad4 = Radiobutton(frame4,text='30', value=30, variable=selected)
    rad1.grid(column=0, row=2)  
    rad2.grid(column=0, row=3)  
    rad3.grid(column=0, row=4)   
    rad4.grid(column=0, row=5)

    #нажав на кнопку, печатаем это все в окне
    btn = Button(frame4, text="Показать",command=choise)
    btn.grid(column=0, row=12)



tab1()
tab2()
tab3()
#tab4()

notebook.add(frame1, text='Клиенты')
notebook.add(frame2, text='Средства защиты')
notebook.add(frame3, text='Лицензии')
notebook.add(frame4, text='Посмотреть истекающие лицензии')


app.mainloop()