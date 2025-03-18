# main_dashboard.py
import tkinter as tk
from tkinter import ttk
import dashboard1_savdo
import dashboard2_moliya
import dashboard3_inventarizatsiya
import dashboard4_mijozlar
import dashboard5_operatsion


def main():
    root = tk.Tk()
    root.title("BI Portfolio Dashboard")
    root.geometry("1000x700")

    notebook = ttk.Notebook(root)

    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)
    tab4 = ttk.Frame(notebook)
    tab5 = ttk.Frame(notebook)

    notebook.add(tab1, text="Savdo")
    notebook.add(tab2, text="Moliya")
    notebook.add(tab3, text="Inventarizatsiya")
    notebook.add(tab4, text="Mijozlar")
    notebook.add(tab5, text="Operatsion")
    notebook.pack(expand=1, fill='both')

    dashboard1_savdo.create_dashboard(tab1)
    dashboard2_moliya.create_dashboard(tab2)
    dashboard3_inventarizatsiya.create_dashboard(tab3)
    dashboard4_mijozlar.create_dashboard(tab4)
    dashboard5_operatsion.create_dashboard(tab5)

    root.mainloop()


if __name__ == '__main__':
    main()

