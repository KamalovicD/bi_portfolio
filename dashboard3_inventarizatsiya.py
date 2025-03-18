import psycopg2
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


def update_chart(parent, filters):
    store_filter = filters.get('store', None)
    product_category = filters.get('product_category', None)

    query = """
    SELECT st.store_name, p.product_name, i.quantity
    FROM inventory i
    JOIN stores st ON i.store_id = st.store_id
    JOIN products p ON i.product_id = p.product_id
    """
    params = []
    conditions = []
    if store_filter and store_filter != "All":
        conditions.append("st.store_name = %s")
        params.append(store_filter)
    if product_category and product_category != "All":
        conditions.append("p.category = %s")
        params.append(product_category)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY st.store_name;"

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

    
    if results:
        
        store_name = results[0][0]
        data = [(r[1], r[2]) for r in results if r[0] == store_name]
        product_names = [x[0] for x in data]
        quantities = [x[1] for x in data]
    else:
        product_names, quantities = [], []

    for widget in parent.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(product_names, quantities, color='orange')
    ax.set_xlabel("Mahsulotlar")
    ax.set_ylabel("Zaxira Miqdori")
    ax.set_title(f"{store_filter if store_filter != 'All' else 'Barcha do\'konlar'}: Inventarizatsiya")

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)


def create_dashboard(parent):
    filter_frame = tk.Frame(parent)
    filter_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    store_var = tk.StringVar(value="All")
    product_category_var = tk.StringVar(value="All")
    tk.Label(filter_frame, text="Store:").grid(row=0, column=0, padx=2, pady=2)
    store_options = ["All", "Ishonch Center", "Ishonch West", "Ishonch East"]
    tk.OptionMenu(filter_frame, store_var, *store_options).grid(row=0, column=1, padx=2, pady=2)
    tk.Label(filter_frame, text="Product Category:").grid(row=0, column=2, padx=2, pady=2)
    product_options = ["All", "Electronics", "Appliance"]
    tk.OptionMenu(filter_frame, product_category_var, *product_options).grid(row=0, column=3, padx=2, pady=2)

    chart_frame = tk.Frame(parent)
    chart_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def apply_filters():
        filters = {
            'store': store_var.get(),
            'product_category': product_category_var.get()
        }
        update_chart(chart_frame, filters)

    tk.Button(filter_frame, text="Apply Filters", command=apply_filters).grid(row=1, column=0, columnspan=4, pady=5)
    apply_filters()
