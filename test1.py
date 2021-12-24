"""������������� ����. ������ ������. ���������� � ��, ����� ������ ������ �� ������� �� ������. ������ ���� ��� �����, ��������� ������ ����� ����� ������������."""

import psycopg2
from prettytable import PrettyTable
from prettytable import from_db_cursor
import tkinter
from tkinter import *



class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        
        #�������� ����
        self.title("�������� ��������")
        self.iconbitmap("green.ico")
        self.geometry("1000x600+800+400")
        self.resizable(False, False)
        
        lbl = Label(self, text=mytable)
        lbl.pack(padx=120, pady=10)

        #self.Label(self, text="dsa")
        #�������� ������
        #��������� ���� �� �������� ��� �����, ������� ��������������� 
        #self.btn = tkinter.Button(self, text="������� ���� � ����������", command=self.open_license)
        #self.btn.pack(padx=120, pady=15)
        #������ ������ � ����� ������ ���������
        self.btn = tkinter.Button(self, text="������� ��� ������", command=self.exit)
        self.btn.pack(padx=120, pady=15)

        #��������� ������� ��� 2 ������
    def open_license(self):
        #file_path = r'License.txt'
        #os.system("start "+file_path)
        #self.destroy()
        print(mytable)
    #def open_key(self):
    #    file_path = r'Key_support.txt'
    #    os.system("start "+file_path)
    #    #self.destroy()
    def exit(self):
        self.destroy()

       



connection = psycopg2.connect(database="orders", user="postgres", password="123456", host="127.0.0.1", port="5432")
cursor = connection.cursor () 

mytable = PrettyTable()
mytable.field_names = ["customer", "tool", "expiration date"]

#������� ������
#cursor.execute("INSERT INTO users (ADMISSION, NAME, AGE, COURSE, DEPARTMENT) VALUES (267, 'James', 23, 'Programming', 'IT')")
#cursor.execute("INSERT INTO users (ADMISSION, NAME, AGE, COURSE, DEPARTMENT) VALUES (203, 'Liza', 18, 'History', 'Historical')")
#cursor.execute("INSERT INTO users (ADMISSION, NAME, AGE, COURSE, DEPARTMENT) VALUES (189, 'John', 27, 'PE', 'Sport')")
#cursor.execute("INSERT INTO users (ADMISSION, NAME, AGE, COURSE, DEPARTMENT) VALUES (23, 'Maria', 20, 'Scients', 'Biology')")
#cursor.execute("INSERT INTO users (ADMISSION, NAME, AGE, COURSE, DEPARTMENT) VALUES (60, 'Nelson', 34, 'Cars', 'Mechanic')")
#cursor.execute("INSERT INTO users (ADMISSION, NAME, AGE, COURSE, DEPARTMENT) VALUES (4003, 'Natalia', 16, 'Literaure', 'Art')")
#connection.commit()

#���������� ������
#cursor.execute("select customer.name_short, tools.name, licenses.date_end from licenses join customer on customer.id = licenses.customerid join tools on tools.id = licenses.toolid")
#rows = cursor.fetchall()
#for row in rows:
#    mytable.add_row(row)

    #print(row)


#mytable.field_names = ["customer", "tool", "expiration date"]

#print(mytable)

#app = App()
#app.mainloop()

#��������� ���������� ������

#def gettext():
#    print(text1.get())

def button1():
    cursor.execute("select * from customer")
    mytable = from_db_cursor(cursor)
    print(mytable)
    lbl = Label(app, text=mytable)
    lbl.grid(column=1, row=0)
def button1_2():
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


btn = Button(app, text="�������, ����� ������� ������� customer!", command=button1)
btn.grid(column=0, row=0)
btn = Button(app, text="�������� ������", command=button1_2)
btn.grid(column=0, row=1)


btn = Button(app, text="�������, ����� ������� ������� tools!", command=button2)
btn.grid(column=0, row=3)
btn = Button(app, text="�������, ����� ������� ������� licenses!", command=button3)
btn.grid(column=0, row=4)
btn = Button(app, text="�������, ����� ������� ����� �������!", command=button4)
btn.grid(column=0, row=5)




app.mainloop()
connection.close()