# dashboard2_moliya.py
import psycopg2
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


def update_chart(parent, filters):
    start_date = filters.get('start_date', '2025-03-01')
    end_date = filters.get('end_date', '2025-03-31')
    store_filter = filters.get('store', None)
    report_type = filters.get('report_type', 'profit')  # profit, revenue, expenses

    query = """
    SELECT st.store_name, AVG(f.revenue - f.expenses) AS avg_profit, AVG(f.revenue) AS avg_revenue, AVG(f.expenses) AS avg_expenses
    FROM financials f
    JOIN stores st ON f.store_id = st.store_id
    WHERE f.record_date BETWEEN %s AND %s
    """
    params = [start_date, end_date]
    if store_filter and store_filter != "All":
        query += " AND st.store_name = %s"
        params.append(store_filter)
    query += " GROUP BY st.store_name;"

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

    store_names = [row[0] for row in results]
    if report_type == 'revenue':
        values = [float(row[2]) for row in results]
        ylabel = "O'rtacha Daromad"
        title = "Moliya Dashboard: Daromad"
    elif report_type == 'expenses':
        values = [float(row[3]) for row in results]
        ylabel = "O'rtacha Xarajatlar"
        title = "Moliya Dashboard: Xarajatlar"
    else:
        values = [float(row[1]) for row in results]
        ylabel = "O'rtacha Foyda"
        title = "Moliya Dashboard: Foyda"

    for widget in parent.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(store_names, values, color='lightgreen')
    ax.set_xlabel("Do'konlar")
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)


def create_dashboard(parent):
    filter_frame = tk.Frame(parent)
    filter_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    start_date_var = tk.StringVar(value="2025-03-01")
    end_date_var = tk.StringVar(value="2025-03-31")
    store_var = tk.StringVar(value="All")
    report_type_var = tk.StringVar(value="profit")

    tk.Label(filter_frame, text="Start Date:").grid(row=0, column=0, padx=2, pady=2)
    tk.Entry(filter_frame, textvariable=start_date_var, width=12).grid(row=0, column=1, padx=2, pady=2)
    tk.Label(filter_frame, text="End Date:").grid(row=0, column=2, padx=2, pady=2)
    tk.Entry(filter_frame, textvariable=end_date_var, width=12).grid(row=0, column=3, padx=2, pady=2)
    tk.Label(filter_frame, text="Store:").grid(row=1, column=0, padx=2, pady=2)
    store_options = ["All", "Ishonch Center", "Ishonch West", "Ishonch East"]
    tk.OptionMenu(filter_frame, store_var, *store_options).grid(row=1, column=1, padx=2, pady=2)
    tk.Label(filter_frame, text="Report Type:").grid(row=1, column=2, padx=2, pady=2)
    report_options = ["profit", "revenue", "expenses"]
    tk.OptionMenu(filter_frame, report_type_var, *report_options).grid(row=1, column=3, padx=2, pady=2)

    chart_frame = tk.Frame(parent)
    chart_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def apply_filters():
        filters = {
            'start_date': start_date_var.get(),
            'end_date': end_date_var.get(),
            'store': store_var.get(),
            'report_type': report_type_var.get()
        }
        update_chart(chart_frame, filters)

    tk.Button(filter_frame, text="Apply Filters", command=apply_filters).grid(row=2, column=0, columnspan=4, pady=5)
    apply_filters()
