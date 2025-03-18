## This project employs Business Intelligence through the use of Python and SQL within the PyCharm community.

1. Upon downloading the project, kindly install the requisite libraries.

```bash
pip install psycopg2-binary matplotlib
```

2. Initially, execute the SQL files in your terminal or within the PyCharm terminal window.

```bash
psql -d bi_portfolio -f create_tables.sql
psql -d bi_portfolio -f insert_data.sql
```

3. Thereafter, employ this script to consolidate and display all dashboards within a single application.

```bash
python main_dashboard.py
```
