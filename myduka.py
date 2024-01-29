import psycopg2


conn=psycopg2.connect(
host='localhost',
database='myduka_db',
user='postgres',
password='jaceomari123',
port='5435',
)
cur=conn.cursor()


def check_email_password(email,password):
    query="SELECT id,name FROM  users WHERE email=%s AND password=%s"
    cur.execute(query,(email,password))
    result=cur.fetchone()
    if result is not None:
        id=result[0]
        name= result[1]
        return id,name
    else:
        return None


def calculate_sales():
    cursor=conn.cursor()
    sales_query="""SELECT products.name,SUM(sales.quantity)as total_sales FROM sales
    JOIN products on products.id=sales.pid
    GROUP BY products.name;"""
    cursor.execute(sales_query)
    list_sales=cursor.fetchall()
    return list_sales
# create_script = '''INSERT INTO public.products(
# 	id, name, buying_price, selling_price, stock_quantity)
# 	VALUES (13, 'laptops', 700, 1000, 10);'''
# cur.execute(create_script)

# create_script='''UPDATE public.products
# 	SET buying_price=400, selling_price=500
# 	WHERE id=2;'''
# cur.execute(create_script)

# cur.execute('''select  products.name,sales.quantity,products.selling_price
#             from sales 
#             join products on products.id=sales.pid
#             limit 1
#             ''')
# # cur.execute('select * from products')
# for records in cur.fetchall():
#   print(records)

# create_table= '''create table suppliers(
# id int, 
# name character varying,
# contacts int
# )
# '''
# cur.execute(create_table)

# cur.execute(
#     ''' select products.name,sum((products.selling_price-products.buying_price)* sales.quantity)
#     as profit from sales join products on products.id=sales.pid group by products.name
#     order by profit limit 1
# '''
# )
# cur.execute('select * from products')
# for records in cur.fetchall():
#     print(records)

# create_script='''INSERT INTO public.suppliers(
# 	id, name, contacts)
# 	VALUES (2009, 'jace', 0723724333);'''
# cur.execute(create_script)

conn.commit()


