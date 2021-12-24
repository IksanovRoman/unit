from tkinter import *
from tkinter.ttk import Notebook
import psycopg2
from prettytable import PrettyTable,from_db_cursor
from datetime import datetime
from tkinter import messagebox, ttk

#подключаемся к базе данных, указываем имя базы данных, пользователя, его пароль, ip адрес и порт
connection = psycopg2.connect(database="orders_test", user="postgres", password="123456", host="127.0.0.1", port="5432")
cursor = connection.cursor () 

#создаем объект tk, он отвечает за окно вывода
app = Tk()
app.title("Проверка лицензий")
w = app.winfo_screenwidth()
h = app.winfo_screenheight()
app.geometry("1000x600+600+200")

#создаем объект вкладок от главного окна
notebook = Notebook(app)
notebook.pack(pady=10, expand=True)

#создаем четыре вкладки от объекта вкладок
frame1 = Frame(notebook, width=980, height=580)
frame2 = Frame(notebook, width=980, height=580)
frame3 = Frame(notebook, width=980, height=580)
frame4 = Frame(notebook, width=980, height=580)

frame1.pack(fill='both', expand=True)
frame2.pack(fill='both', expand=True)
frame3.pack(fill='both', expand=True)
frame4.pack(fill='both', expand=True)

def tab1():
    '''Данная вкладка взаимодействует с таблицой клиентов в БД'''
     
    def show_customer_table():
        '''Данная функция выводит таблицу клиентов, сортируя по id'''

        cursor.execute("select c.id as ID, c.name_short as заказчик,c.name_full as заказчик_полное_имя from customer as c order by id asc")
        mytable = from_db_cursor(cursor)
    
        #выводим текст
        txt = Text(frame1, wrap="none", height=15, width=100)
        txt.grid(row=0, column=1) 
        txt.insert(1.0,mytable)
        txt.config(bg='#D9D8D7', state='disabled')

        #каждую первую строку красим в другой цвет
        k=0
        cursor.execute("select id from customer order by id asc")
        for rows in cursor:
            k+=1 #считаем кол-во строк

        s=0
        for n in range(1,k+1):
            if n%2==1:
                s=n+3
                txt.tag_add("here",f"{s}.0", f"{s}.end") 
                txt.tag_config("here", background="#BEBEBE", foreground="black") #красим в другой цвет
                n+=1

        

        #добавляем вертикальную полосу прокрутки
        sb = Scrollbar(frame1, orient=VERTICAL)
        sb.grid(row=0, column=1, sticky=NS+E)
        txt.config(yscrollcommand=sb.set)
        sb.config(command=txt.yview)
        #добавляем горизонтальную полосу прокрутки
        sb2 = Scrollbar( frame1, orient=HORIZONTAL)
        sb2.grid(row=0, column=1, sticky=EW+S)
        txt.config(xscrollcommand=sb2.set)
        sb2.config(command=txt.xview)

    def add_customer_table():
        '''Данная функция дает возможность внести данные в таблицу клиентов'''
        
        #создаем новое всплывающее модальное окно
        app2 = Toplevel(app)
        app2.title("Добавление данных")
        app2.geometry("600x100+100+200")
        app2.grab_set()

        #добавляем подпись и поля ввода
        Label(app2, text="Введите короткое имя заказчика").grid(column=0, row=0)
        Label(app2, text="Введите полное имя заказчика").grid(column=0, row=1)
        text2 = Entry(app2, width=30)
        text2.grid(column=1, row=0)
        text3 = Entry(app2, width=30)
        text3.grid(column=1, row=1)

        def add_information_customer():
            '''#Ввод данных в таблицу клиентов'''

            #получаем всю информацию о клиентах
            cursor.execute("select id from customer order by id asc")
            rows = cursor.fetchall()
            if rows==[]:
                t1=1 #если таблица пустая t1=1

            sum=1
            for row in rows: #если таблица не пустая, ищем свободный id по порядку
                if sum!=row[0]: 
                    t1=sum #здесь хранится id в которое запишем
                    break
                else:
                    t1=row[0]+1
                sum+=1
            

            #получаем значения с полей ввода
            t2 = text2.get()
            t3 = text3.get()
            k=0

            #проверка на пустые строки
            if t2=="" or t3=="":
                btn1.config(state=DISABLED)
                messagebox.showerror('Отказано', 'Вы не заполнили все поля')
                btn1.config(state=NORMAL)
                
            elif t2.isalnum() and t3.isalnum():
                #проверяем на уникальность
                cursor.execute("select name_short, name_full from customer order by id asc")
                for row in cursor:
                    if t2==row[0].lower() or t3==row[1].lower():
                        k=1
                if k:
                    messagebox.showerror('Отказано', 'Такой заказчик уже есть')
                else:
                    #записываем данные, если нажимаем да
                    answer = messagebox.askyesno(title="Вопрос", message="Записать данные в таблицу?") #диалоговое окно да/нет
                    if answer:
                        cursor.execute(f"INSERT INTO customer VALUES ({t1},'{t2}','{t3}')")
                        connection.commit()
                        messagebox.showinfo('Успешно', 'Данные занесены')
                        app2.destroy()
                        show_customer_table()
            else:
                btn1.config(state=DISABLED)
                messagebox.showinfo('Отказ', 'Некорректный ввод')
                btn1.config(state=NORMAL)
        #кнопка для добавления данных в таблицу        
        btn1 = Button(app2, text="Добавить",command=add_information_customer)
        btn1.grid(row=0, column=2, padx=5)

    def delete_customer_table():
        '''Данная функция дает возможность удалить данные из таблицы клиентов'''
        
        app2 = Toplevel(app)
        app2.title("Удаление")
        app2.geometry("400x100+100+200")
        app2.grab_set()
        
        #подпись
        Label(app2, text="Выберите заказчика для удаления").grid(column=0, row=0)
        
        #выбираем кого хотим удалить
        customer_values=[]
        cursor.execute("select name_short from customer")
        for row in cursor:
            customer_values.append(row[0])
        customer_values.sort(key=lambda x: x.lower())
        text1 = ttk.Combobox(app2, values=customer_values, state="readonly")
        text1.grid(column=1, row=0) 
        
    
        def delete_information_customer():
            '''Функция проверит введеное значение и удалит данные по id из customer'''
            
            #проверка на пустую строку
            if text1.get()=="":
                btn1.config(state=DISABLED)
                messagebox.showerror('Отказано', 'Выберите заказчика')
                btn1.config(state=NORMAL)
            else:
                customerid=0
                cursor.execute(f"select id from customer where name_short='{text1.get()}'")
                for row in cursor:
                    customerid = row[0] #здесь хранится id заказчика

                #удаляем данные, если отвечаем да
                answer = messagebox.askyesno(title="Вопрос", message="Удалить данные из таблицы?\nВнимание, все дочерние записи из других таблиц тоже удалятся")
                if answer:
                    cursor.execute(f"DELETE FROM customer where ID={customerid}")
                    connection.commit()
                    messagebox.showinfo('Успешно', 'Удалено')
                    app2.destroy()
                    show_customer_table()
    
        #кнопка удалит данные из таблицы
        btn1 = Button(app2, text="Удалить",command=delete_information_customer)
        btn1.grid(column=2,row=0, padx=5)

    def update_customer_table():
        '''Данная функция дает возможность изменить данные в таблице клиентов'''

        app2 = Toplevel(app)
        app2.title("Добавление данных")
        app2.geometry("600x100+100+200")
        app2.grab_set()

        #поле с информацией
        Label(app2, text="Выберите заказчика для изменения").grid(column=0, row=0)

        #выбираем кого хотим изменить
        customer_values=[]
        cursor.execute("select name_short from customer")
        for row in cursor:
            customer_values.append(row[0]) #здесь сохраним всех заказчиков
        customer_values.sort(key=lambda x: x.lower())
        text1 = ttk.Combobox(app2, values=customer_values, state="readonly") #здесь сохраним наше имя заказчика
        text1.grid(column=1, row=0)
    
        def update_customer_check_id():
            '''Данная кнопка будет проверять есть ли такой id в таблице и в дальнейшем изменять содержимое таблицы'''
            if text1.get()=="":
                btn1.config(state=DISABLED)
                messagebox.showinfo('Отказ', 'Выберите заказчика')
                btn1.config(state=NORMAL)
            else:
                btn1.config(state=DISABLED)
                Label(app2, text="Введите новое имя заказчика").grid(column=0, row=1)
                Label(app2, text="Введите новое полное имя заказчика").grid(column=0, row=2)

                #поля ввода
                text2 = Entry(app2, width=30)
                text2.grid(column=1, row=1)
                text3 = Entry(app2, width=30)
                text3.grid(column=1, row=2)
            
                def update_customer():
                    '''Данная функция обновит данные'''
                    #получаем два поля ввода
                    t2 = text2.get()
                    t3 = text3.get()
                    k=0
                    if t2=="" and t3=="":
                        btn2.config(state=DISABLED)
                        messagebox.showinfo('Отказано', 'Заполните оба поля имени заказчика')
                        btn2.config(state=NORMAL)
                    elif t2.isalnum() and t3.isalnum() :
                    
                        cursor.execute("select name_short, name_full from customer order by id asc")
                        for row in cursor:
                            if t2==row[0].lower() or t3==row[1].lower():
                                k=1

                        if k:
                            messagebox.showerror('Отказ', 'Такой заказчик уже есть')
                        else:
                            customerid=0
                            cursor.execute(f"select id from customer where name_short='{text1.get()}'")
                            for row in cursor:
                                customerid = row[0] #здесь хранится id заказчика

                            answer = messagebox.askyesno(title="Вопрос", message="Изменить имена заказчиков?")
                            if answer:
                                cursor.execute(f"UPDATE customer SET name_short = '{t2}' WHERE id = {customerid}")
                                cursor.execute(f"UPDATE customer SET name_full = '{t3}' WHERE id = {customerid}")
                                connection.commit()
                                messagebox.showinfo('Успешно', 'Данные обновлены')
                                app2.destroy()
                                show_customer_table()
                    else:
                        btn2.config(state=DISABLED)
                        messagebox.showinfo('Отказано', 'Некорректный ввод')
                        btn2.config(state=NORMAL)



                #данная кнопка добавит данные в табличку
                btn2 = Button(app2, text="Изменить имена заказчиков", command=update_customer)
                btn2.grid(column=2,row=2)

        #кнопка подтверждения
        btn1 = Button(app2, text="Подтвердить", command=update_customer_check_id)
        btn1.grid(column=2,row=0, padx=5)
    

    #показать таблицу
    show_customer_table()
    frame1.photo = PhotoImage(file=r"C:\Users\Roman\Desktop\Python new (2)\postgresql\update.png") 
    Button(frame1, image=frame1.photo, command=show_customer_table, width="30", height="30").grid(column=0, row=0)
    #добавить данные
    Button(frame1, text="Добавить", command=add_customer_table).grid(column=0, row=1)
    #удалить данные
    Button(frame1, text="Удалить", command=delete_customer_table).grid(column=0,row=2)
    #изменить данные
    Button(frame1, text="Изменить", command=update_customer_table).grid(column=0,row=3)
  

def tab2():
    '''Данная вкладка взаимодействует с таблицой средств защиты в БД'''

    def show_tools_table():
        cursor.execute("select t.id as ID, t.license_name as название_лицензии from tools as t order by id asc")
        mytable = from_db_cursor(cursor)
    
        #печатаем текст с прокруткой
        txt = Text(frame2, wrap="none", height=15, width=100)
        txt.grid(row=0, column=1) 
        txt.insert(1.0,mytable)
        txt.config(bg='#D9D8D7', state='disabled')

        k=0
        cursor.execute("select id from tools order by id asc")
        for rows in cursor:
            k+=1

        s=0
        for n in range(1,k+1):
            if n%2==1:
                s=n+3
                txt.tag_add("here",f"{s}.0", f"{s}.end")
                txt.tag_config("here", background="#BEBEBE", foreground="black")
                n+=1

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
    
        app2 = Toplevel(app)
        app2.title("Добавление данных")
        app2.geometry("400x100+100+200")
        app2.grab_set()
        
        #информация по полям ввода
        Label(app2, text="Новое средство защиты").grid(column=0, row=0)

        #располагаем поля ввода
        text1 = Entry(app2, width=30)
        text1.grid(column=1, row=0)

        def add_information_tools():
            '''#функция нужна для ввода данных в таблицу средств защиты'''
            cursor.execute("select id from tools order by id asc")

            rows = cursor.fetchall()
            if rows==[]:
                t1=1

            sum=1
            for row in rows:
                if sum!=row[0]: 
                    t1=sum #здесь хранится id в которое запишем
                    break
                else:
                    t1=row[0]+1
                sum+=1



            t2 = text1.get() #получаем значения с 2 полей
            k=0 #маркер, изначально 0, но если 1, то данные запишутся в БД

            if t2=="": #если одно из полей пустое, то дальше не пойдем
                btn1.config(state=DISABLED)
                messagebox.showerror('Отказано', 'Вы не заполнили поле')
                btn1.config(state=NORMAL)
               
            elif t2.isalnum():
                cursor.execute("select license_name from tools order by id asc")
                for row in cursor:
                    if t2==row[0].lower():
                        k=1
                if k:
                    messagebox.showerror('Отказ', 'Такое средство защиты уже есть')
                else:
                    btn1.config(state=DISABLED)
                    answer = messagebox.askyesno(title="Вопрос", message="Записать данные в таблицу?") #диалоговое окно да/нет
                    btn1.config(state=NORMAL)
                    if answer:
                        cursor.execute(f"INSERT INTO tools VALUES ({t1},'{t2}')")
                        connection.commit()
                        messagebox.showinfo('Успешно', 'Данные занесены')
                        app2.destroy()
                        show_tools_table()
            else:
                btn1.config(state=DISABLED)
                messagebox.showerror('Отказано', 'Некорректный ввод')
                btn1.config(state=NORMAL)
                          
        #кнопка для добавления данных в таблицу        
        btn1 = Button(app2, text="Добавить",command=add_information_tools)
        btn1.grid(row=0, column=2, padx=5)
          
    def delete_tools_table():
        '''Данная кнопка будет удалять данные из таблицы tools по их id'''

        app2 = Toplevel(app)
        app2.title("Удаление")
        app2.geometry("400x100+100+200")
        app2.grab_set()
        
        #поле с информацией
        Label(app2, text="Удалить средство защиты").grid(column=0, row=0)
        
        #выбираем кого хотим удалить
        tool_values=[]
        cursor.execute("select license_name from tools")
        for row in cursor:
            tool_values.append(row[0])
        tool_values.sort(key=lambda x: x.lower())
        text1 = ttk.Combobox(app2, values=tool_values, state="readonly")
        text1.grid(column=1, row=0) 

        def delete_information_tools():
            '''#функция проверит введеное значение и удалит данные по id из tools'''
            if text1.get()=="":
                btn1.config(state=DISABLED)
                messagebox.showerror('Отказано', 'Выберите средство защиты')
                btn1.config(state=NORMAL)
            else:
                toolid=0
                cursor.execute(f"select id from tools where license_name='{text1.get()}'")
                for row in cursor:
                    toolid = row[0] #здесь хранится id средства защиты

                answer = messagebox.askyesno(title="Вопрос", message="Удалить данные из таблицы?\nВнимание, все дочерние записи из других таблиц тоже удалятся") #вопрос подтверждения
                if answer: #если отвечаем да
                    cursor.execute(f"DELETE FROM tools where ID={toolid}") #удаляем запись из таблицы
                    connection.commit()
                    messagebox.showinfo('Успешно', 'Удалено')
                    app2.destroy()
                    show_tools_table()

        #кнопка удалит данные из таблицы
        btn1 = Button(app2, text="Удалить",command=delete_information_tools)
        btn1.grid(column=2,row=0, padx=5)

    def update_tools_table():
        '''Данная кнопка будет изменять данные в таблице tools'''
        
        app2 = Toplevel(app)
        app2.title("Проверка лицензий")
        app2.geometry("500x100+100+200")
        app2.grab_set()

        #поле с информацией
        Label(app2, text="Выберите заказчика для изменения").grid(column=0, row=0)
        #поле ввода id
        tool_values=[]
        cursor.execute("select license_name from tools")
        for row in cursor:
            tool_values.append(row[0]) #здесь сохраним всех заказчиков
        tool_values.sort(key=lambda x: x.lower())
        text1 = ttk.Combobox(app2, values=tool_values, state="readonly") #здесь сохраним наше имя заказчика
        text1.grid(column=1, row=0)

        def update_tools_check_id():
            '''Данная кнопка будет проверять есть ли такой id в таблице и в дальнейшем изменять содержимое таблицы'''
            if text1.get()=="":
                btn1.config(state=DISABLED)
                messagebox.showerror('Отказано', 'Выберите средство защиты')
                btn1.config(state=NORMAL)
            else:
                btn1.config(state=DISABLED)
                Label(app2, text="Введите новое средство защиты").grid(column=0, row=1)

                #поля ввода
                text2 = Entry(app2, width=30)
                text2.grid(column=1, row=1)
                
                def update_tool():
                    '''Данная функция добавит данные в табличку, если пользователь ввел id, либо имена заказчика'''
                    #получаем два поля ввода
                    t2 = text2.get()
                    k=0
                    if t2=="":
                        btn2.config(state=DISABLED)
                        messagebox.showerror('Отказ', 'Заполните поле')
                        btn2.config(state=NORMAL)
                    elif t2.isalnum():
                        cursor.execute("select license_name from tools order by id asc")
                        for row in cursor:
                            if t2==row[0].lower():
                                k=1
                        if k:
                            messagebox.showerror('Отказано', 'Такое средство защиты уже есть')
                        else:
                            toolid=0
                            cursor.execute(f"select id from tools where license_name='{text1.get()}'")
                            for row in cursor:
                                toolid = row[0] #здесь хранится id заказчика

                            answer = messagebox.askyesno(title="Вопрос", message="Изменить имена заказчиков?")
                            if answer:
                                cursor.execute(f"UPDATE tools SET license_name = '{t2}' WHERE id = {toolid}")
                                connection.commit()
                                messagebox.showinfo('Успешно', 'Данные обновлены')
                                app2.destroy()
                                show_tools_table()
                    else:
                        btn2.config(state=DISABLED)
                        messagebox.showerror('Отказ', 'Некорректный ввод')
                        btn2.config(state=NORMAL)
                #данная кнопка добавит данные в табличку
                btn2 = Button(app2, text="Изменить средство защиты", command=update_tool)
                btn2.grid(column=1,row=3, pady=5)

        #кнопка подтверждения
        btn1 = Button(app2, text="Подтвердить", command=update_tools_check_id)
        btn1.grid(column=2,row=0, padx=5)
        
    
        
    show_tools_table()
    frame2.photo = PhotoImage(file=r"C:\Users\Roman\Desktop\Python new (2)\postgresql\update.png") 
    Button(frame2, image=frame2.photo, command=show_tools_table, width="30", height="30").grid(column=0, row=0)
    #кнопка добавление данных
    Button(frame2, text="Добавить", command=add_tools_table).grid(column=0, row=1)
    #кнопка удаление данных
    Button(frame2, text="Удалить", command=delete_tools_table).grid(column=0,row=2)
    #кнопка изменения данных
    Button(frame2, text="Изменить", command=update_tools_table).grid(column=0,row=3)

def tab3():
    '''Данная кнопка выводит информацию о таблице лицензий из БД'''

    def show_licenses_table():
        cursor.execute(f"select l.id, c.name_short as заказчик, t.license_name as название_лицензии, l.licenses_date_start as дата_начала_лицензии, l.licenses_date_end as дата_окончания_лицензии, l.key_techsupport_name as ключ_техподдержки, l.key_date_end as дата_окончания_ключа from licenses as l join customer as c on c.id = l.customerid join tools as t on t.id = l.toolid order by l.id asc")
        mytable = from_db_cursor(cursor)
    
        #печатаем текст с прокруткой
        txt = Text(frame3, wrap="none", height=12, width=100)
        txt.grid(row=0, column=1) 
        txt.insert(1.0,mytable)
        txt.config(bg='#D9D8D7', state='disabled')

        k=0
        cursor.execute("select id from licenses order by id asc")
        for rows in cursor:
            k+=1

        s=0
        for n in range(1,k+1):
            if n%2==1:
                s=n+3
                txt.tag_add("here",f"{s}.0", f"{s}.end")
                txt.tag_config("here", background="#BEBEBE", foreground="black")
                n+=1

        

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
        app2 = Toplevel(app)
        app2.title("Проверка лицензий")
        app2.geometry("550x170+50+150")
        app2.grab_set()

        #информация по полям ввода
        Label(app2, text="Выберите заказчика").grid(column=0, row=1)
        Label(app2, text="Выберите средство защиты").grid(column=0, row=2)
        Label(app2, text="Введите дату начала лицензии").grid(column=0, row=3); Label(app2, text="(день/месяц/год)").grid(column=2, row=3)
        Label(app2, text="Введите дату окончания лицензии").grid(column=0, row=4); Label(app2, text="(день/месяц/год)").grid(column=2, row=4)
        Label(app2, text="Введите ключ технической поддержки").grid(column=0, row=5)
        Label(app2, text="Введите дату окончания ключа").grid(column=0, row=6); Label(app2, text="(день/месяц/год)").grid(column=2, row=6)

               
        #выбираем заказчика и средство защиты (всплывающее меню)
        customer_values=[]
        cursor.execute("select name_short from customer")
        for row in cursor:
            customer_values.append(row[0])
        text2 = ttk.Combobox(app2, values=customer_values, state="readonly")
        text2.grid(column=1, row=1) 

        tool_values=[]
        cursor.execute("select license_name from tools")
        for row in cursor:
            tool_values.append(row[0])
        text3 = ttk.Combobox(app2, values=tool_values, state="readonly")
        text3.grid(column=1, row=2)

        #вводим даты и ключ поддержки
        text4 = Entry(app2, width=30)
        text4.grid(column=1, row=3)
        text5 = Entry(app2, width=30)
        text5.grid(column=1, row=4)
        text6 = Entry(app2, width=30)
        text6.grid(column=1, row=5)
        text7 = Entry(app2, width=30)
        text7.grid(column=1, row=6)

        def add_information_licenses():
            '''#функция нужна для ввода данных в таблицу лицензий'''
            

            #получаем первое поле, id он выберет автоматически
            cursor.execute("select id from licenses order by id asc")
            
            rows = cursor.fetchall()
            if rows==[]:
                t1=1

            sum=1
            for row in rows:
                if sum!=row[0]: 
                    t1=sum #здесь хранится id в которое запишем
                    break
                else:
                    t1=row[0]+1
                sum+=1


            customerid=0
            cursor.execute(f"select id from customer where name_short='{text2.get()}'")
            for row in cursor:
                customerid = row[0] #здесь хранится id заказчика

            toolid=0
            cursor.execute(f"select id from tools where license_name='{text3.get()}'")
            for row in cursor:
                toolid = row[0] #здесь хранится id средства защиты

            t4 = text4.get() 
            t5 = text5.get()
            t6 = text6.get()
            t7 = text7.get()

            k=0 #если 1 поле это число, то k=1
            n=0 #если есть id, то n=1
            date=0 #если все 3 даты заполнены правильно, то date=1

            if t1=="" or customerid=="" or toolid=="" or t4=="" or t5=="" or t6=="" or t7=="": #если одно из поле пустой, то дальше не пойдем
                btn1.config(state=DISABLED)
                messagebox.showerror('Отказано', 'Вы не заполнили все поля')
                btn1.config(state=NORMAL)
            elif t1.isalnum() and customerid.isalnum() and toolid.isalnum() and t4.isalnum() and t5.isalnum() and t6.isalnum() and t7.isalnum():
                try:
                    d1 = datetime.strptime(t4, "%d/%m/%Y") #преобразуем три поля ввода в дату
                    d2 = datetime.strptime(t5, "%d/%m/%Y")
                    d3 = datetime.strptime(t7, "%d/%m/%Y")
                    date=1
                except:

                    messagebox.showerror('Отказано', 'Дата заполнена не правильно')
                if date: #если все даты в порядке, то пишем в БД
                    btn1.config(state=DISABLED)
                    answer = messagebox.askyesno(title="Вопрос", message="Записать данные в таблицу?") #диалоговое окно да/нет
                    btn1.config(state=NORMAL)
                    if answer:
                        cursor.execute(f"INSERT INTO licenses VALUES ({t1},{customerid},{toolid},'{t4}','{t5}','{t6}','{t7}')")
                        connection.commit()
                        messagebox.showinfo('Успешно', 'Данные занесены')
                        app2.destroy()
                        show_licenses_table()
            else:
                btn1.config(state=DISABLED)
                messagebox.showerror('Отказано', 'Некорректный ввод')
                btn1.config(state=NORMAL)
        #кнопка для добавления данных в таблицу        
        btn1 = Button(app2, text="Добавить",command=add_information_licenses)
        btn1.grid(row=7, column=2,padx=5)

    def delete_licenses_table():
        '''Данная кнопка будет удалять данные из таблицы licenses по их id'''
        app2 = Toplevel(app)
        app2.title("Проверка лицензий")
        app2.geometry("500x50+50+150")
        app2.grab_set()

        #поле с информацией
        Label(app2, text="Выберите идентификатор для удаления").grid(column=0, row=0)
        #поле ввода
        text1 = Entry(app2, width=10)
        text1.grid(column=1, row=0)

        #выбираем кого хотим удалить
        licenses_id=[]
        cursor.execute("select id from licenses")
        for row in cursor:
            licenses_id.append(row[0])
        licenses_id.sort()
        text1 = ttk.Combobox(app2, values=licenses_id, state="readonly")
        text1.grid(column=1, row=0) 

        def delete_information_licenses():
            '''#функция проверит введеное значение и удалит данные по id из licenses'''
            if text1.get()=="":
                btn1.config(state=DISABLED)
                messagebox.showerror('Отказано', 'Выберите идентификатор')
                btn1.config(state=NORMAL)
            else:
                answer = messagebox.askyesno(title="Вопрос", message="Удалить данные из таблицы?\nВнимание, все дочерние записи из других таблиц тоже удалятся") #вопрос подтверждения
                if answer: #если отвечаем да
                    cursor.execute(f"DELETE FROM licenses where ID={text1.get()}") #удаляем запись из таблицы
                    connection.commit()
                    messagebox.showinfo('Успешно', 'Удалено')
                    app2.destroy()
                    show_licenses_table()
           
        #кнопка удалит данные из таблицы
        btn1 = Button(app2, text="Удалить",command=delete_information_licenses)
        btn1.grid(column=2,row=0,padx=5)

    def update_licenses_table():
        '''Данная кнопка будет изменять данные в таблице licenses'''
        app2 = Toplevel(app)
        app2.title("Проверка лицензий")
        app2.geometry("900x200+50+150")
        app2.grab_set()

        #поле с информацией
        Label(app2, text="Выберите идентификатор лицензии для удаления").grid(column=0, row=0)

         #выбираем кого хотим удалить
        licenses_id=[]
        cursor.execute("select id from licenses")
        for row in cursor:
            licenses_id.append(row[0])
        licenses_id.sort()
        text1 = ttk.Combobox(app2, values=licenses_id, state="readonly")
        text1.grid(column=1, row=0) 

        def update_licenses_check_id():
            '''Данная кнопка будет проверять есть ли такой id в таблице и в дальнейшем изменять содержимое таблицы'''
            if text1.get()=="":
                btn1.config(state=DISABLED)
                messagebox.showerror('Отказано', 'Выберите идентификатор')
                btn1.config(state=NORMAL)
            else:
                btn1.config(state=DISABLED)
                Label(app2, text="Выберите другого заказчика").grid(column=0, row=1)
                Label(app2, text="Выберите новое средство защиты").grid(column=0, row=2)

                customer_values=[]
                cursor.execute("select name_short from customer")
                for row in cursor:
                    customer_values.append(row[0]) #здесь сохраним всех заказчиков
                customer_values.sort(key=lambda x: x.lower())
                text2 = ttk.Combobox(app2, values=customer_values, state="readonly") #здесь сохраним наше имя заказчика
                text2.grid(column=1, row=1)

                tool_values=[]
                cursor.execute("select license_name from tools")
                for row in cursor:
                    tool_values.append(row[0]) #здесь сохраним всех заказчиков
                tool_values.sort(key=lambda x: x.lower())
                text3 = ttk.Combobox(app2, values=tool_values, state="readonly") #здесь сохраним наше имя заказчика
                text3.grid(column=1, row=2)

                Label(app2, text="Введите новую дату начала лицензии").grid(column=0, row=3)
                Label(app2, text="Введите новую дату окончания лицензии").grid(column=0, row=4)
                Label(app2, text="Введите новый ключ технической поддержки").grid(column=0, row=5)
                Label(app2, text="Введите новую дату окончания ключа").grid(column=0, row=6)

                #поля ввода
                text4 = Entry(app2, width=30)
                text4.grid(column=1, row=3)
                text5 = Entry(app2, width=30)
                text5.grid(column=1, row=4)
                text6 = Entry(app2, width=30)
                text6.grid(column=1, row=5)
                text7 = Entry(app2, width=30)
                text7.grid(column=1, row=6)
                Label(app2, text="Не обязательно заполнять все поля").grid(column=1, row=7)


                def update_table():
                    count=0 #считаем кол-во добавленных данных
                    error=0 #если есть ошибка ввода

                    t2 = text2.get()
                    t3 = text3.get()
                    t4 = text4.get()
                    t5 = text5.get()
                    t6 = text6.get()
                    t7 = text7.get()

                    check_insert = {"text2":False,"text3":False,"text4":False,"text5":False,"text6":False,"text7":False,}

                    if t2!="":
                        #если все правильно введено, то обновляем id в табличке
                        check_insert["text2"]=True
                        count+=1
                        cursor.execute(f"select id from customer where name_short='{t2}'")
                        for row in cursor:
                            t2 = row[0] #здесь хранится id средства защиты
                    if t3!="":
                        #если все правильно введено, то обновляем id в табличке
                        check_insert["text3"]=True
                        count+=1
                        cursor.execute(f"select id from tools where license_name='{t3}'")
                        for row in cursor:
                            t3 = row[0] #здесь хранится id средства защиты
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
                            check_insert["text4"]=True
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
                            check_insert["text5"]=True
                            count+=1
                    if t6!="":
                        if t6.isalnum():
                            check_insert["text6"]=True
                            count+=1
                        else:
                            btn1.config(state=DISABLED)
                            messagebox.showerror('Отказано', 'Некорректный ввод')
                            btn1.config(state=NORMAL)
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
                            check_insert["text7"]=True
                            count+=1

                    if error>0:
                        messagebox.showerror('Отказ', 'Проврерьте правильность ввода')
                    elif count>0 and error==0:
                        answer = messagebox.askyesno(title="Вопрос", message="Записать данные в таблицу?") #диалоговое окно да/нет
                        if answer:
                            licensesid=0
                            cursor.execute(f"select id from licenses where id='{text1.get()}'")
                            for row in cursor:
                                licensesid = row[0] #новое id, куда запишем

                            if check_insert["text2"]:
                                cursor.execute(f"UPDATE licenses SET customerid = {t2} WHERE id = {licensesid}")
                            if check_insert["text3"]:
                                cursor.execute(f"UPDATE licenses SET toolid = {t3} WHERE id = {licensesid}")
                            if check_insert["text4"]:
                                cursor.execute(f"UPDATE licenses SET licenses_date_start = '{d1}' WHERE id = {licensesid}")
                            if check_insert["text5"]:
                                cursor.execute(f"UPDATE licenses SET licenses_date_end = '{d2}' WHERE id = {licensesid}")
                            if check_insert["text6"]:
                                cursor.execute(f"UPDATE licenses SET key_techsupport_name = '{t6}' WHERE id = {licensesid}")
                            if check_insert["text7"]:
                                cursor.execute(f"UPDATE licenses SET key_date_end = '{d3}' WHERE id = {licensesid}")
                            connection.commit()
                            messagebox.showinfo('Успешно', 'Данные обновлены')
                            show_licenses_table()
                            app2.destroy()
                    else:
                        btn2.config(state=DISABLED)
                        messagebox.showerror('Отказ', 'Введите данные')
                        btn2.config(state=NORMAL)

                btn2 = Button(app2, text="Изменить", command=update_table)
                btn2.grid(column=2,row=6)
            
           
        #кнопка подтверждения
        btn1 = Button(app2, text="Подтвердить", command=update_licenses_check_id)
        btn1.grid(column=2,row=0,padx=5)

    
    
    show_licenses_table()
    frame3.photo = PhotoImage(file=r"C:\Users\Roman\Desktop\Python new (2)\postgresql\update.png") 
    Button(frame3, image=frame3.photo, command=show_licenses_table, width="30", height="30").grid(column=0, row=0)
    #Добавить
    Button(frame3, text="Добавить", command=add_licenses_table).grid(column=0, row=1)
    #Удалить
    Button(frame3, text="Удалить", command=delete_licenses_table).grid(column=0,row=2)
    #Изменить
    Button(frame3, text="Изменить", command=update_licenses_table).grid(column=0,row=3)
    
def tab4():
    
    text1 = ttk.Combobox(frame4, values=[1,3,7,30], state="readonly")
    text1.grid(column=0, row=0)
    text1.current(0)
    
    def choise():
        
        cursor.execute(f"select l.id as ID, c.name_short as заказчик, t.license_name as название_лицензии, l.licenses_date_start as дата_начала, l.licenses_date_end as дата_окончания, l.key_techsupport_name as ключ_техподдержки, l.key_date_end as дата_окончания_ключа_техподдержки from licenses as l join customer as c on c.id = l.customerid join tools as t on t.id = l.toolid where l.licenses_date_end - current_date <= {text1.get()} and l.licenses_date_end - current_date > 0 order by l.id asc")
        mytable = from_db_cursor(cursor)

        #печатаем таблицы с прокруткой     
        txt = Text(frame4, wrap="none", height=10, width=100)
        txt.grid(row=1, column=0)
        txt.config(bg='#D9D8D7')
        txt.insert(1.0,mytable) # вставляем информацию из БД
        
        k=0
        cursor.execute("select id from licenses order by id asc")
        for rows in cursor:
            k+=1

        s=0
        for n in range(1,k+1):
            if n%2==1:
                s=n+3
                txt.tag_add("here",f"{s}.0", f"{s}.end")
                txt.tag_config("here", background="#BEBEBE", foreground="black")
                n+=1

        sb = Scrollbar( frame4, orient=VERTICAL)
        sb.grid(row=1, column=0, sticky=NS+E)
        txt.config(yscrollcommand=sb.set)
        sb.config(command=txt.yview)
            
        sb2 = Scrollbar( frame4, orient=HORIZONTAL)
        sb2.grid(row=1, column=0, sticky=EW+S)
        txt.config(xscrollcommand=sb2.set)
        sb2.config(command=txt.xview)

    #нажав на кнопку, печатаем это все в окне
    Button(frame4, text="Показать",command=choise).grid(column=1, row=0)


#открываем сразу все вкладки
tab1()
tab2()
tab3()
tab4()

notebook.add(frame1, text='Клиенты')
notebook.add(frame2, text='Средства защиты')
notebook.add(frame3, text='Лицензии')
notebook.add(frame4, text='Истекающие лицензии')


app.mainloop()
connection.close()