# dashboard5_operatsion.py
import psycopg2
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


def update_chart(parent, filters):
    start_date = filters.get('start_date', '2025-03-01')
    end_date = filters.get('end_date', '2025-03-31')
    credit_status = filters.get('credit_status', "All")

    query = """
    SELECT status, COUNT(*) AS num_applications
    FROM credit_applications
    WHERE application_date BETWEEN %s AND %s
    """
    params = [start_date, end_date]
    if credit_status and credit_status != "All":
        query += " AND status = %s"
        params.append(credit_status)
    query += " GROUP BY status;"

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

    statuses = [row[0] for row in results]
    counts = [row[1] for row in results]

    for widget in parent.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(statuses, counts, color='violet')
    ax.set_xlabel("Kredit Ariza Holati")
    ax.set_ylabel("Ariza Soni")
    ax.set_title("Operatsion Jarayonlar Dashboard")

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)


def create_dashboard(parent):
    filter_frame = tk.Frame(parent)
    filter_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    start_date_var = tk.StringVar(value="2025-03-01")
    end_date_var = tk.StringVar(value="2025-03-31")
    credit_status_var = tk.StringVar(value="All")

    tk.Label(filter_frame, text="Start Date:").grid(row=0, column=0, padx=2, pady=2)
    tk.Entry(filter_frame, textvariable=start_date_var, width=12).grid(row=0, column=1, padx=2, pady=2)
    tk.Label(filter_frame, text="End Date:").grid(row=0, column=2, padx=2, pady=2)
    tk.Entry(filter_frame, textvariable=end_date_var, width=12).grid(row=0, column=3, padx=2, pady=2)
    tk.Label(filter_frame, text="Credit Status:").grid(row=1, column=0, padx=2, pady=2)
    status_options = ["All", "approved", "pending", "rejected"]
    tk.OptionMenu(filter_frame, credit_status_var, *status_options).grid(row=1, column=1, padx=2, pady=2)

    chart_frame = tk.Frame(parent)
    chart_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def apply_filters():
        filters = {
            'start_date': start_date_var.get(),
            'end_date': end_date_var.get(),
            'credit_status': credit_status_var.get()
        }
        update_chart(chart_frame, filters)

    tk.Button(filter_frame, text="Apply Filters", command=apply_filters).grid(row=2, column=0, columnspan=4, pady=5)
    apply_filters()
