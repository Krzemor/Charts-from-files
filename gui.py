import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import messagebox
import customtkinter as ctk

from Builder.Director import Director
from Producer import LineGraph, BarGraph, PieGraph


class App:
    def __init__(self, master):
        self.builder = None
        self.path = ''
        self.master = master
        self.master.title("Rysuj wykres")
        self.master.geometry("250x250")

        ctk.set_appearance_mode("dark")

        ctk.CTkLabel(self.master, text="Wybierz plik:").pack()
        ctk.CTkButton(self.master, text="Wybierz", command=self.select_file).pack()

        type_frame = ctk.CTkFrame(self.master, bg_color="black")
        type_frame.pack(fill="both", expand=True)
        ctk.CTkLabel(type_frame, text="Wybierz typ wykresu:").pack()
        self.chart_type = tk.IntVar()

        ctk.CTkRadioButton(type_frame, text="Słupkowy", variable=self.chart_type, value=1,
                       command=self.update_draw_button).pack()
        ctk.CTkRadioButton(type_frame, text="Liniowy", variable=self.chart_type, value=2,
                       command=self.update_draw_button).pack()
        ctk.CTkRadioButton(type_frame, text="Kołowy", variable=self.chart_type, value=3,
                       command=self.update_draw_button).pack()

        self.draw_button = ctk.CTkButton(self.master, text="Rysuj wykres", command=self.draw_chart)
        self.draw_button.pack(side=tk.LEFT)

        self.close_button = ctk.CTkButton(self.master, text="Zamknij", command=self.close, fg_color="#FF6666",
                                          hover_color="red")
        self.close_button.pack(side=tk.LEFT)

        self.update_draw_button()

    def select_file(self):
        self.path = filedialog.askopenfilename()
        print(f"Selected file: {self.path}")

    def draw_chart(self):
        director = Director()
        builder = None

        if self.chart_type.get() == 1:
            builder = BarGraph.BarGraph(self.path, True)

        if self.chart_type.get() == 2:
            builder = LineGraph.LineGraph(self.path, True)

        if self.chart_type.get() == 3:
            builder = PieGraph.PieGraph(self.path, True)

        director.builder = builder
        director.build_graph()

    def update_draw_button(self):
        if self.chart_type.get() == 1 or self.chart_type.get() == 2 or self.chart_type.get() == 3:
            self.draw_button.configure(state=tk.NORMAL)
        else:
            self.draw_button.configure(state=tk.DISABLED)

    def close(self):
        result = messagebox.askquestion("Zamykanie...", "Czy na pewno chcesz zamknąć aplikację?")
        if result == "yes":
            self.master.destroy()


root = ctk.CTk()
app = App(root)
root.mainloop()
