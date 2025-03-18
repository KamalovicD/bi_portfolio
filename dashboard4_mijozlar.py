import psycopg2
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


def update_chart(parent, filters):
    region = filters.get('region', "All")

    query = """
    SELECT c.gender, COUNT(c.customer_id) AS count_customers
    FROM customers c
    """
    params = []
    if region and region != "All":
        query += " WHERE c.location = %s"
        params.append(region)
    query += " GROUP BY c.gender;"

    conn = psycopg2.connect(
        host="localhost",
        database="bi_portfolio",
        user="postgres",
        password="YOUR_PASSWORD"
    )
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    labels = [row[0] for row in results]
    sizes = [row[1] for row in results]

    for widget in parent.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title("Mijozlar Segmentatsiyasi (Gender)")

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)


def create_dashboard(parent):
    filter_frame = tk.Frame(parent)
    filter_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    region_var = tk.StringVar(value="All")
    tk.Label(filter_frame, text="Region:").grid(row=0, column=0, padx=2, pady=2)
    region_options = ["All", "Toshkent", "Samarqand", "Buxoro"]
    tk.OptionMenu(filter_frame, region_var, *region_options).grid(row=0, column=1, padx=2, pady=2)

    chart_frame = tk.Frame(parent)
    chart_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def apply_filters():
        filters = {
            'region': region_var.get()
        }
        update_chart(chart_frame, filters)

    tk.Button(filter_frame, text="Apply Filters", command=apply_filters).grid(row=1, column=0, columnspan=2, pady=5)
    apply_filters()
