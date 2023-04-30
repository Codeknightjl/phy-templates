import tkinter as tk
import tkinter.font
import tkinter.messagebox
import math
import numpy as np
from PIL import ImageTk, Image
import csv
import datetime

class ProjectileApp:
    def __init__(self, master):
        self.master = master
        master.title("Projectile Minimum Speed Calculator")

        img = ImageTk.PhotoImage(Image.open("projectile_image2.png"))
        self.example = tk.Label(master, image=img)
        self.example.image = img
        self.example.grid(row=0, column=0, columnspan=2, padx=10, sticky="nsew")

        # create input fields for x and y
        self.x_label = tk.Label(master, text="Horizontal Distance (m):")
        self.x_label.grid(row=1, column=0, padx=5, pady=5)
        self.x_entry = tk.Entry(master)
        self.x_entry.grid(row=1, column=1, padx=5, pady=5)

        self.y_label = tk.Label(master, text="Vertical Distance (m):")
        self.y_label.grid(row=2, column=0, padx=5, pady=5)
        self.y_entry = tk.Entry(master)
        self.y_entry.grid(row=2, column=1, padx=5, pady=5)

        # create output table for minimum speed and angle
        self.speed_label = tk.Label(master, text="Minimum Speed (m/s)")
        self.speed_label.grid(row=3, column=0, padx=5, pady=5)
        self.angle_label = tk.Label(master, text="Corresponding Angle (degrees)")
        self.angle_label.grid(row=3, column=1, padx=5, pady=5)

        self.speed_listbox = tk.Listbox(master, width=15, height=11)
        self.speed_listbox.grid(row=4, column=0, padx=5, pady=5)

        self.angle_listbox = tk.Listbox(master, width=15, height=11)
        self.angle_listbox.grid(row=4, column=1, padx=5, pady=5)

        self.query_label = tk.Label(master, text="Query Speed:")
        self.query_label.grid(row=5, column=0, padx=5, pady=(5,0))
        self.speed_query = tk.Entry(master, width=15)
        self.speed_query.grid(row=6, column=0, padx=5, pady=(0,10))

        self.angle_query = tk.Label(master, text="N/A")
        self.angle_query.grid(row=5, column=1, padx=5, pady=(20,0))

        # create calculate button
        self.calculate_button = tk.Button(master, text="Calculate", bg="light green", command=self.calculate)
        self.calculate_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)


    def calculate(self):
        # get input values for x and y
        try:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter valid numbers")
            return
        query_speed = None
        if self.speed_query.get() == '':
            pass
        else:
            try:
                query_speed = float(self.speed_query.get())
            except ValueError:
                tk.messagebox.showerror("Error", "Please enter valid numbers")
                return

        # create table of minimum speed and corresponding angle
        g = 9.81  # acceleration due to gravity
        determinant = (2*g*y) ** 2 + (2*g*x) ** 2
        v_min = math.sqrt((2*g*y + math.sqrt(determinant)) / 2)
        speed_list = [v_min]
        speed_list.extend([math.ceil(v_min+i) for i in range(9)])
        # print(speed_list)
        angle_list = []
        for v in speed_list:
            coeff = [1, -(2*(v**2)) / (g*x), 1 + (2*(v**2)*y) / (g*(x**2))]
            angle_tan = np.roots(coeff)
            angle1, angle2 = math.atan(angle_tan[0]), math.atan(angle_tan[1])
            angle_list.append((math.degrees(angle2), math.degrees(angle1)))

        # update output table
        self.speed_listbox.delete(0, tk.END)
        self.angle_listbox.delete(0, tk.END)
        # print(angle_list)
        for i in range(len(speed_list)):
            self.speed_listbox.insert(tk.END, "{:.2f}".format(speed_list[i]))
            self.angle_listbox.insert(tk.END, "{:.2f}, {:.2f}".format(angle_list[i][0], angle_list[i][1]))

        try:
            float(self.speed_query.get())
        except:
            self.angle_query.config(text="N/A")
        else:
            if float(self.speed_query.get()) < v_min:
                tk.messagebox.showwarning("Warning", "Query speed must be at least minimum possible speed")
                self.speed_query.delete(0, tk.END)
                self.speed_query.insert(0, "{:.2f}".format(v_min))
            v = float(self.speed_query.get())
            coeff = [1, -(2 * (v ** 2)) / (g * x), 1+(2 * (v ** 2) * y) / (g * (x ** 2))]
            angle_tan = np.roots(coeff)
            angle1, angle2 = math.atan(angle_tan[0]), math.atan(angle_tan[1])
            self.angle_query.config(text="{:.2f}, {:.2f}".format(math.degrees(angle2), math.degrees(angle1)))

        with open('angles'+datetime.datetime.now().strftime("%H%M%S"), 'w') as f:
            write = csv.writer(f)
            for i in range(len(angle_list)):
                write.writerow([speed_list[i], angle_list[i][0], angle_list[i][1]])


root = tk.Tk()
# root.config(bg="white")
defaultFont = tk.font.nametofont("TkDefaultFont")
defaultFont.configure(size=14)  # Change default font size
app = ProjectileApp(root)
root.mainloop()
