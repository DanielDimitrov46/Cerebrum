import tkinter as tk
from runCreate import create

# creating a GUI window
window = tk.Tk()
window.geometry('1500x800')
window.title('DB engine')

# creating a canvas
canvas1 = tk.Canvas(window, width=1500, height=800)
canvas1.pack()

# making Heading
l = tk.Label(window, text="Welcome to the DB engine.")
l.config(font=("Arial", 20))
l.place(relx=0.5, rely=0.05, anchor='center')

# making description
l1 = tk.Label(window, text="Choose an option!")
l1.config(font=("Arial", 12))
l1.place(relx=0.5, rely=0.10, anchor='center')


# function to options

def create_new_database():
    def delete_text():# delete widgets after creation or after cancelation
        button1.destroy()
        entry1.destroy()
        button2.destroy()

    def real_create():# logic for creating a database
        label2 = tk.Label(window, text='')
        label2.config(font=('helvetica', 10))
        canvas1.create_window(200, 300, window=label2)
        real_create = create(entry1.get())
        label2.config(text=real_create)
        label2.after(2000, label2.destroy)
        delete_text()
    entry1 = tk.Entry(window)
    canvas1.create_window(200, 140, window=entry1)
    button1 = tk.Button(text='Create the new database', command=real_create, bg='brown', fg='white',font=('helvetica', 9, 'bold'))
    canvas1.create_window(200, 180, window=button1)
    button2 = tk.Button(text='Cancel crating a new DB', command=delete_text, bg='brown', fg='white',
                        font=('helvetica', 9, 'bold'))
    canvas1.create_window(200, 220, window=button2)
def load_databases():  # load all database button to do the logic of loading data
    def delete_text():  # delete widgets after creation or after cancelation
        button1.destroy()
        entry1.destroy()
        button2.destroy()

    def real_create():  # logic for creating a database
        label2 = tk.Label(window, text='')
        label2.config(font=('helvetica', 10))
        canvas1.create_window(200, 300, window=label2)
        real_create = create(entry1.get())
        label2.config(text=real_create)
        label2.after(2000, label2.destroy)
        delete_text()

    entry1 = tk.Entry(window)
    canvas1.create_window(200, 140, window=entry1)
    button1 = tk.Button(text='Create the new database', command=real_create, bg='brown', fg='white',
                        font=('helvetica', 9, 'bold'))
    canvas1.create_window(200, 180, window=button1)
    button2 = tk.Button(text='Cancel crating a new DB', command=delete_text, bg='brown', fg='white',
                        font=('helvetica', 9, 'bold'))
    canvas1.create_window(200, 220, window=button2)


def drop_database():  # delete a database button
    pass



def exit_from_application():  # exit_from_application
    window.destroy()


# making buttons
btn = tk.Button(window, text='Create a new database', bd='3', command=create_new_database, activebackground="red")
btn.place(relx=0.35, rely=0.20, anchor='center')
btn1 = tk.Button(window, text='Show all databases', bd='3', command=load_databases, activebackground="green")
btn1.place(relx=0.45, rely=0.20, anchor='center')
btn2 = tk.Button(window, text='Drop a database', bd='3', command=window.destroy, activebackground="blue")
btn2.place(relx=0.55, rely=0.20, anchor='center')
btn3 = tk.Button(window, text='Exit from the application!', bd='3', command=exit_from_application,
                 activebackground="yellow")
btn3.place(relx=0.65, rely=0.20, anchor='center')

# favicon for application
p1 = tk.PhotoImage(file='../GUI/cerebrum.png')
window.iconphoto(False, p1)
window.mainloop()
