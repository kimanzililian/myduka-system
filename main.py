from flask import Flask,render_template,redirect,request
import psycopg2
from myduka import check_email_password,calculate_sales

conn=psycopg2.connect(
host='localhost',
database='myduka_db',
user='postgres',
password='jaceomari123',
port='5435',
)


curr=conn.cursor()

app=Flask(__name__)
@app.route('/')
def hello():
    return render_template ('index.html')

@app.route('/dashboard')
def dashboard():
    product_name=[]
    total_sale=[]
    for i in calculate_sales():
        product_name.append(i[0])
        total_sale.append(i[1])

    return render_template('dashboard.html',product=product_name,total=total_sale)


@app.route('/register', methods=['post','get'])
def register():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        values=(name,email,password)
        insert_users="insert into users(name,email,password)values(%s,%s,%s)"
        curr.execute(insert_users,values)
        conn.commit()
    return render_template('register.html')

@app.route('/products', methods=['post', 'get'])
def products():
    curr.execute('select * from products')
    products=curr.fetchall()
    return render_template('products.html',products=products)


@app.route('/add_products', methods=['post','get'])
def add_products():
        
        name=request.form['name']
        buying_price=request.form['buying_price']
        selling_price=request.form['selling_price']
        stock_quantity=request.form['stock_quantity']
        values=(name,buying_price,selling_price,stock_quantity)
        insert_add_products="insert into products(name,buying_price,selling_price,stock_quantity)values(%s,%s,%s,%s)"
        curr.execute(insert_add_products,values)
        conn.commit()
        return redirect('/products')


@app.route('/sales')
def sales():
    curr.execute('select * from sales')
    sales=curr.fetchall()
    curr.execute('select * from products')
    products=curr.fetchall()
    return render_template('sales.html' , sales=sales, products=products)


@app.route('/add_sales', methods=['post','get'])
def add_sales():
    pid=request.form['pid']
    quantity=request.form['quantity']
    values=(quantity,pid)
    insert_sales='insert into sales (quantity,created_at,pid) values(%s,now(),%s)'
    curr.execute(insert_sales,values)
    conn.commit()
    return redirect('/sales')



    

@app.route('/login', methods=['post','get'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        user=check_email_password(email,password)
        if user:
            return redirect("/dashboard")
        else:
            return redirect('/register')
    return render_template('login.html')


conn.commit()
app.run(debug=True)

