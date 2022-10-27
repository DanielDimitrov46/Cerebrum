import tkinter as tk
import dbmaster
# creating a GUI window
window = tk.Tk()
window.geometry('1600x800')
window.title('DB engine')

# making Heading
l = tk.Label(window, text="Welcome to the DB engine.")
l.config(font=("Arial", 20))
l.place(relx=0.5, rely=0.05, anchor='center')

# making description
l1 = tk.Label(window, text="Choose an option!")
l1.config(font=("Arial", 12))
l1.place(relx=0.5, rely=0.10, anchor='center')

# making buttons
btn = tk.Button(window, text='Create a new database', bd='3', command= "runCreate", activebackground="red")
btn.place(relx=0.35, rely=0.20, anchor='center')
btn1 = tk.Button(window, text='Show all databases', bd='3', command=window.destroy, activebackground="green")
btn1.place(relx=0.45, rely=0.20, anchor='center')
btn2 = tk.Button(window, text='Drop a database', bd='3', command=window.destroy, activebackground="blue")
btn2.place(relx=0.55, rely=0.20, anchor='center')
btn3 = tk.Button(window, text='Exit from the application!', bd='3', command=window.destroy, activebackground="yellow")
btn3.place(relx=0.65, rely=0.20, anchor='center')

# function to options
def create_new_database():
    pass
def load_databases():
    pass
def drop_database():
    pass
def exit_from_application():
    pass

# favicon for application
p1 = tk.PhotoImage(file='cerebrum.png')
window.iconphoto(False, p1)
window.mainloop()
