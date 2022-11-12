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

def GUI():
    def on_enter(e):
        btn['background'] = 'green'
    def on_enter1(e):
        btn1['background'] = 'green'
    def on_enter2(e):
        btn2['background'] = 'green'
    def on_enter3(e):
        btn3['background'] = 'green'

    def on_leave(e):
        btn['background'] = 'SystemButtonFace'
    def on_leave1(e):
        btn1['background'] = 'SystemButtonFace'
    def on_leave2(e):
        btn2['background'] = 'SystemButtonFace'
    def on_leave3(e):
        btn3['background'] = 'SystemButtonFace'


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

        def delete_text():  # delete widgets after creation or after cancelation
            button1.destroy()
            entry1.destroy()
            button2.destroy()

        def real_create():  # logic for creating a database
            params_index = 0
            print(l_params)

            params = {
                'name': "",
                'family': "",
                'num': "",
                'town': "",
                'G': "",
                'rUm': "",
                'birthDate': "",
                'scor': ""
            }
            for key in params.keys():
                params[key] = l_params[params_index]
                params_index += 1

            print(params)
            label2 = tk.Label(window, text='')
            label2.config(font=('helvetica', 10))
            canvas1.create_window(200, 300, window=label2)
            dbmaster.open(f'{entry1.get()}', params, '~')
            label2.config(text=(f"{entry1.get()} was created"))
            label2.after(2000, label2.destroy)
            delete_text()

        params_entry = tk.Entry(window)
        canvas1.create_window(200, 115,window=params_entry)
        l_params = (params_entry.get()).split(",")
        # test = tk.Label(text="null").place(x=200,y=540)
        # tk.Button(text="print params",command=test.config(text=l_params)).place(x=200,y=500)

        entry1 = tk.Entry(window)
        canvas1.create_window(200, 140, window=entry1)
        button1 = tk.Button(text='Create the new database', command=real_create, bg='brown', fg='white',
                            font=('helvetica', 9, 'bold'))
        canvas1.create_window(200, 180, window=button1)
        button2 = tk.Button(text='Cancel crating a new DB', command=delete_text, bg='brown', fg='white',
                            font=('helvetica', 9, 'bold'))
        canvas1.create_window(200, 220, window=button2)

    def open_back():
        for widgets in window.winfo_children():
            widgets.destroy()
        GUI()

    def open():

        def on_enter_back_to_main(e):
            back_to_main['background'] = 'green'

        def on_leave_back_to_main(e):
            back_to_main['background'] = 'SystemButtonFace'


        for widgets in window.winfo_children():
            widgets.destroy()

        back_to_main = tk.Button(text='Go back!',height=3,width=10,command=open_back,activebackground="red")
        back_to_main.place(x=1420)
        back_to_main.bind("<Enter>",on_enter_back_to_main)
        back_to_main.bind("<Leave>",on_leave_back_to_main)


        
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
            real_search_by_columns_and_parameters = dbmaster.search(columns.get(), parameter.get(), name_of_database.get())
            label2.config(text=real_search_by_columns_and_parameters)
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
        
        tk.Button(text='Delete Databse', command=real_delete).place(relx=0.55, rely=0.4,anchor='center')

    # making buttons
    btn = tk.Button(window, text='Create a new database', bd='3', command=create_new_database, activebackground="red")
    btn.place(relx=0.35, rely=0.20, anchor='center')
    btn.bind("<Enter>",on_enter)
    btn.bind("<Leave>",on_leave)
    btn1 = tk.Button(window, text='Open a database', bd='3', command=open, activebackground="red")
    btn1.place(relx=0.45, rely=0.20, anchor='center')
    btn1.bind("<Enter>",on_enter1)
    btn1.bind("<Leave>",on_leave1)
    btn2 = tk.Button(window, text='Drop a database', bd='3', command=drop_database, activebackground="red")
    btn2.place(relx=0.55, rely=0.20, anchor='center')
    btn2.bind("<Enter>",on_enter2)
    btn2.bind("<Leave>",on_leave2)
    btn3 = tk.Button(window, text='Exit from the application!', bd='3', command=window.destroy,activebackground="yellow")
    btn3.place(relx=0.65, rely=0.20, anchor='center')
    btn3.bind("<Enter>",on_enter3)
    btn3.bind("<Leave>",on_leave3)

    # favicon for application
    # p1 = tk.PhotoImage(file='../GUI/cerebrum.png')
    # window.iconphoto(False, p1)

    window.mainloop()
GUI()