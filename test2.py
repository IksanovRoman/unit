import psycopg2
from prettytable import PrettyTable
from prettytable import from_db_cursor
import tkinter
from tkinter import messagebox
from tkinter import *


connection = psycopg2.connect(database="orders", user="postgres", password="123456", host="127.0.0.1", port="5432")
cursor = connection.cursor () 

mytable = PrettyTable()


#���������� ������
#cursor.execute("select customer.name_short, tools.name, licenses.date_end from licenses join customer on customer.id = licenses.customerid join tools on tools.id = licenses.toolid")
#rows = cursor.fetchall()
#for row in rows:
#    mytable.add_row(row)
    #print(row)


#print(mytable)

#app = App()
#app.mainloop()

#��������� ���������� ������

#def gettext():
#    print(text1.get())

def button1():
    '''������ ������ ������� ���������� � ������� �������� �� ��'''
    cursor.execute("select * from customer")
    mytable = from_db_cursor(cursor)
    print(mytable)
    lbl = Label(app, text=mytable)
    lbl.grid(column=1, row=0)
def button1_2():
    '''������ ������ ���� ����������� ��������� ������� �������� � ��, ����� �� ���� �������� �� ���� ������'''
    lbl = Label(app, text="������� �������� ��� ���������")
    lbl.grid(column=1, row=1)
    lbl = Label(app, text="������� ������ ��� ���������")
    lbl.grid(column=1, row=2)
    
    text1 = Entry(app, width=50)
    text1.grid(column=2, row=1)
    text2 = Entry(app, width=50)
    text2.grid(column=2, row=2)

    def gettext():
        print(text1.get(), type(text1.get()), text2.get(), type(text2.get()))
        if text1.get()!="" and text2.get()!="": #�������� ����� ������� ��� ����
            answer = messagebox.askyesno(title="������", message="�������� ������ � �������?")
            if answer:
                cursor.execute(f"INSERT INTO customer (name_short, name_full) VALUES ('{text1.get()}','{text2.get()}')")
                connection.commit()
                messagebox.showinfo('�������', '������ ��������')
        else:
            messagebox.showinfo('��������', '�� �� ��������� ��� ����')
    btn = Button(app, text="��������",command=gettext)
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
    lbl.configure(text="� �� ������...")  


app = Tk()

app.title("�������� ��������")
app.iconbitmap("green.ico")
app.geometry("1000x600")


#������ ������ ����� �������
btn = Button(app, text="�������, ����� ������� ������� customer!", command=button1)
btn.grid(column=0, row=0)
#������ ������ ���������� ������
btn = Button(app, text="�������� ������", command=button1_2)
btn.grid(column=0, row=1)
#������ ������ �������� ������

btn = Button(app, text="�������, ����� ������� ������� tools!", command=button2)
btn.grid(column=0, row=3)
btn = Button(app, text="�������, ����� ������� ������� licenses!", command=button3)
btn.grid(column=0, row=4)
btn = Button(app, text="�������, ����� ������� ����� �������!", command=button4)
btn.grid(column=0, row=5)




app.mainloop()
connection.close()