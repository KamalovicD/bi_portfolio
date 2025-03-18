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
    product_category = filters.get('product_category', None)
    sales_channel = filters.get('sales_channel', None)
    credit_status = filters.get('credit_status', None)

    query = """
    SELECT st.store_name, SUM(s.amount) AS total_credit_sales
    FROM sales s
    JOIN stores st ON s.store_id = st.store_id
    WHERE s.sale_type = 'credit'
      AND s.sale_date BETWEEN %s AND %s
    """
    params = [start_date, end_date]
    if store_filter and store_filter != "All":
        query += " AND st.store_name = %s"
        params.append(store_filter)
    if product_category and product_category != "All":
        query += " AND EXISTS (SELECT 1 FROM products p WHERE p.product_id = s.product_id AND p.category = %s)"
        params.append(product_category)
    if sales_channel and sales_channel != "All":
        query += " AND s.sale_type = %s"
        params.append(sales_channel)
    if credit_status and credit_status != "All":
        query += " AND EXISTS (SELECT 1 FROM credit_applications ca WHERE ca.credit_id = s.sale_id AND ca.status = %s)"
        params.append(credit_status)
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
    total_sales = [float(row[1]) for row in results]

    for widget in parent.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(store_names, total_sales, color='skyblue')
    ax.set_xlabel("Do'konlar")
    ax.set_ylabel("Jami Kredit Savdosi")
    ax.set_title("Savdo Dashboard")

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)


def create_dashboard(parent):
    filter_frame = tk.Frame(parent)
    filter_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    start_date_var = tk.StringVar(value="2025-03-01")
    end_date_var = tk.StringVar(value="2025-03-31")
    store_var = tk.StringVar(value="All")
    product_category_var = tk.StringVar(value="All")
    sales_channel_var = tk.StringVar(value="All")
    credit_status_var = tk.StringVar(value="All")

    tk.Label(filter_frame, text="Start Date:").grid(row=0, column=0, padx=2, pady=2)
    tk.Entry(filter_frame, textvariable=start_date_var, width=12).grid(row=0, column=1, padx=2, pady=2)
    tk.Label(filter_frame, text="End Date:").grid(row=0, column=2, padx=2, pady=2)
    tk.Entry(filter_frame, textvariable=end_date_var, width=12).grid(row=0, column=3, padx=2, pady=2)

    tk.Label(filter_frame, text="Store:").grid(row=1, column=0, padx=2, pady=2)
    store_options = ["All", "Ishonch Center", "Ishonch West", "Ishonch East"]
    tk.OptionMenu(filter_frame, store_var, *store_options).grid(row=1, column=1, padx=2, pady=2)

    tk.Label(filter_frame, text="Product Category:").grid(row=1, column=2, padx=2, pady=2)
    product_options = ["All", "Electronics", "Appliance"]
    tk.OptionMenu(filter_frame, product_category_var, *product_options).grid(row=1, column=3, padx=2, pady=2)

    tk.Label(filter_frame, text="Sales Channel:").grid(row=2, column=0, padx=2, pady=2)
    channel_options = ["All", "credit", "cash"]
    tk.OptionMenu(filter_frame, sales_channel_var, *channel_options).grid(row=2, column=1, padx=2, pady=2)

    tk.Label(filter_frame, text="Credit Status:").grid(row=2, column=2, padx=2, pady=2)
    status_options = ["All", "approved", "pending", "rejected"]
    tk.OptionMenu(filter_frame, credit_status_var, *status_options).grid(row=2, column=3, padx=2, pady=2)

    chart_frame = tk.Frame(parent)
    chart_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def apply_filters():
        filters = {
            'start_date': start_date_var.get(),
            'end_date': end_date_var.get(),
            'store': store_var.get(),
            'product_category': product_category_var.get(),
            'sales_channel': sales_channel_var.get(),
            'credit_status': credit_status_var.get()
        }
        update_chart(chart_frame, filters)

    tk.Button(filter_frame, text="Apply Filters", command=apply_filters).grid(row=3, column=0, columnspan=4, pady=5)
    apply_filters()
