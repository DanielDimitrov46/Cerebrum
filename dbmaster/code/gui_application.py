import os
import tkinter as tk
import dbmaster

# creating a GUI window
window = tk.Tk()
window.geometry('1500x800')
window.title('DB engine')

# creating a canvas
canvas1 = tk.Canvas(window, width=1500, height=800)
canvas1.pack()


def open_back():
    for widgets in window.winfo_children():
        widgets.destroy()
    GUI()


def open():
    for widgets in window.winfo_children():
        widgets.destroy()

    def on_enter_back_to_main(e):
        back_to_main['background'] = 'green'

    def on_leave_back_to_main(e):
        back_to_main['background'] = 'SystemButtonFace'

    open_label = tk.Label(window, text="Choose a database...")
    open_label.config(font=("Arial", 20))
    open_label.place(relx=0.4, y=50)

    databases = dbmaster.getDbs()
    clicked = tk.StringVar()
    clicked.set("Select a database")
    drop_menu = tk.OptionMenu(window, clicked, *databases)
    drop_menu.place(x=200, y=200)

    def insert_to_database():
        entry1 = tk.Entry(window).place(x=700, y=260)
        # canvas1.create_window(700, 260, window=entry1)
        # entry2 = tk.Entry(window)
        # canvas1.create_window(700, 280, window=entry2)
        # entry3 = tk.Entry(window)
        # canvas1.create_window(700, 300, window=entry3)
        # entry4 = tk.Entry(window)
        # canvas1.create_window(700, 320, window=entry4)
        # entry5 = tk.Entry(window)
        # canvas1.create_window(700, 340, window=entry5)
        # entry6 = tk.Entry(window)
        # canvas1.create_window(700, 360, window=entry6)
        # entry7 = tk.Entry(window)
        # canvas1.create_window(700, 380, window=entry7)
        # entry8 = tk.Entry(window)
        # canvas1.create_window(700, 400, window=entry8)

        def real_insert():
            insert_params = {
                'name': entry1.get(),
                # 'family': entry2.get(),
                # 'num': entry3.get(),
                # 'town': entry4.get(),
                # 'gender': entry5.get(),
                # 'room': entry6.get(),
                # 'birthDate': entry7.get(),
                # 'scor': entry8.get()
            }
            obj = dbmaster.open(f'{clicked.get()}')
            obj.insert(insert_params)

        insert_button = tk.Button(window, text="insert", command=real_insert).place(x=700, y=440)

    def select_database():
        if clicked.get() != "Select a database":
            print_database = tk.Button(window, text="Print all\ndata", command="", height=2, width=6).place(x=500,
                                                                                                            y=160)
            select_in_database = tk.Button(window, text="Search in\ndatabase", command="", height=2, width=6).place(
                x=500, y=210)
            insert_database = tk.Button(window, text="Insert to\ndatabase", command=insert_to_database, height=2,
                                        width=6).place(x=500, y=260)
            update_database = tk.Button(window, text="Update\ndata", command="", height=2, width=6).place(x=500, y=310)
            delete_database = tk.Button(window, text="Delete\ndata", command="", height=2, width=6).place(x=500, y=360)

    # def print_data():
    # with dbmaster.open(f'{database_chosen}') as obj:
    #     index_index = 0
    #     text = ""
    #     index,data = obj.get()
    #     for i in data:
    #         text = i[index[index_index]]
    #         print(text)

    select_btn = tk.Button(window, text="select", command=select_database, width=20, activebackground="red").place(
        x=202, y=160)

    back_to_main = tk.Button(window, text='Go back!', height=3, width=10, command=open_back, activebackground="red")
    back_to_main.place(x=1420)
    back_to_main.bind("<Enter>", on_enter_back_to_main)
    back_to_main.bind("<Leave>", on_leave_back_to_main)


def load_databases():  # load all database button to do the logic of loading data
    def delete_text():  # delete widgets after creation or after cancelation
        button1.destroy()
        columns.destroy()
        parameter.destroy()
        button2.destroy()
        name_of_database.destroy()

    def search_function():  # logic for `searching in database
        label2 = tk.Label(window, text='')
        label2.config(font=('helvetica', 10))
        canvas1.create_window(600, 400, window=label2)
        # real_search_by_columns_and_parameters = dbmaster.search(columns.get(), parameter.get(), name_of_database.get())
        # label2.config(text=real_search_by_columns_and_parameters)
        label2.after(2000, label2.destroy)
        delete_text()

    name_of_database = tk.Entry(window)
    canvas1.create_window(555, 250, window=name_of_database)
    columns = tk.Entry(window)
    canvas1.create_window(675, 250, window=columns)
    parameter = tk.Entry(window)
    canvas1.create_window(795, 250, window=parameter)
    button1 = tk.Button(text='Search', command=search_function, bg='brown', fg='white',
                        font=('helvetica', 9, 'bold'))
    canvas1.create_window(675, 280, window=button1)
    button2 = tk.Button(text='Cancel searching', command=delete_text, bg='brown', fg='white',
                        font=('helvetica', 9, 'bold'))


def drop_database():  # delete a database button
    entry1 = tk.Entry(window)
    canvas1.create_window(825, 280, window=entry1)

    def real_delete():
        os.remove(f"{entry1.get()}.dbmd")
        os.remove(f"{entry1.get()}.dbmm")

    tk.Button(text='Delete Databse', command=real_delete).place(relx=0.55, rely=0.4, anchor='center')


def create_new_database():
    def real_create():  # logic for creating a database
        params_index = 0
        text = (params_entry.get())
        l_params = text.split(',')
        params = {
            'name': "",
            'family': "",
            'num': "",
            'town': "",
            'gender': "",
            'room': "",
            'birthDate': "",
            'scor': ""
        }

        for key in params.keys():
            params[key] = int(l_params[params_index])
            params_index += 1
        dbmaster.open(f'{entry1.get()}', params, '~')
        label2 = tk.Label(text=(f"{entry1.get()} was created"), font=('helvetica', 10))
        canvas1.create_window(200, 300, window=label2)
        label2.after(2000, label2.destroy)
        delete_text()

    def delete_text():  # delete widgets after creation or after cancelation
        button1.destroy()
        entry1.destroy()
        button2.destroy()
        params_entry.destroy()

    params_entry = tk.Entry(window)
    canvas1.create_window(200, 115, window=params_entry)

    entry1 = tk.Entry(window)
    canvas1.create_window(200, 140, window=entry1)
    button1 = tk.Button(text='Create the new database', command=real_create, bg='brown', fg='white',
                        font=('helvetica', 9, 'bold'))
    canvas1.create_window(200, 180, window=button1)
    button2 = tk.Button(text='Cancel crating a new DB', command=delete_text, bg='brown', fg='white',
                        font=('helvetica', 9, 'bold'))
    canvas1.create_window(200, 220, window=button2)


def GUI():
    def on_enter(e):
        btn['background'] = 'green'

    def on_enter1(e):
        btn1['background'] = 'green'

    # def on_enter2(e):
    #     btn2['background'] = 'green'
    def on_enter3(e):
        btn3['background'] = 'green'

    # def on_enter4(e):
    #     refresh_button['background'] = 'green'

    def on_leave(e):
        btn['background'] = 'SystemButtonFace'

    def on_leave1(e):
        btn1['background'] = 'SystemButtonFace'

    # def on_leave2(e):
    #     btn2['background'] = 'SystemButtonFace'
    def on_leave3(e):
        btn3['background'] = 'SystemButtonFace'

    # def on_leave4(e):
    #     refresh_button['background'] = 'SystemButtonFace'

    # making Heading
    l = tk.Label(window, text="Welcome to the DB engine.")
    l.config(font=("Arial", 20))
    l.place(relx=0.5, rely=0.05, anchor='center')

    # making description
    l1 = tk.Label(window, text="Choose an option!")
    l1.config(font=("Arial", 12))
    l1.place(relx=0.5, rely=0.10, anchor='center')

    # making buttons
    btn = tk.Button(window, text='Create a new database', bd='3', command=create_new_database, activebackground="red")
    btn.place(relx=0.35, rely=0.20, anchor='center')
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn1 = tk.Button(window, text='Open a database', bd='3', command=open, activebackground="red")
    btn1.place(relx=0.5, rely=0.20, anchor='center')
    btn1.bind("<Enter>", on_enter1)
    btn1.bind("<Leave>", on_leave1)
    # btn2 = tk.Button(window, text='Drop a database', bd='3', command=drop_database, activebackground="red")
    # btn2.place(relx=0.55, rely=0.20, anchor='center')
    # btn2.bind("<Enter>",on_enter2)
    # btn2.bind("<Leave>",on_leave2)
    btn3 = tk.Button(window, text='Exit from the application!', bd='3', command=window.destroy,
                     activebackground="yellow")
    btn3.place(relx=0.65, rely=0.20, anchor='center')
    btn3.bind("<Enter>", on_enter3)
    btn3.bind("<Leave>", on_leave3)

    # favicon for application
    p1 = tk.PhotoImage(file='../GUI/cerebrum.png')
    window.iconphoto(False, p1)

    window.mainloop()


GUI()
