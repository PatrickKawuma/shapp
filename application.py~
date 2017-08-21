print "imported app"

__author__ = 'patrick'

from models.models import User, ShoppingList, SHOPPING_LISTS, USERS
from flask import Flask, render_template, request, session, url_for, redirect


app = Flask(__name__)  # '__main__'


@app.route('/', methods=['GET', 'POST'])
def login_user():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if User.login_valid(username, password):
            User.login(username)
            #return render_template('shoppinglists.html', username=session['username'])
            return redirect(url_for('shopping_list'))

        session['email'] = None
        return "Invalid Login"
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        User.register(username, password)

        #print (list(y.username for y in USERS))   ###check that users are stored until server restart
        return redirect(url_for('shopping_list'))
    return render_template('registration.html')


@app.route('/shoppinglists', methods=['GET', 'POST'])
def shopping_list():

    user = User.get_user(session['username'])

    if request.method == "POST":
        name = request.form['listname']
        budget = request.form['budget']
        username = request.form['username']

        shop_list = ShoppingList(name, budget, user)
        SHOPPING_LISTS.append(shop_list)
        print (list(x.name for x in SHOPPING_LISTS))  #check that my lists are stored until server restart
 
        #result = SHOPPING_LISTS
        lists = user.view_lists()
        for row in lists:
            print(row.id)
        return render_template('shoppinglists.html', result=lists, user=session['username'])

    else:
        lists = user.view_lists()
        for row in lists:
            print("rendering")
        return render_template('shoppinglists.html', result=lists, user=session['username'])


@app.route('/view_list/<list_id>', methods=['GET', 'POST'])
def view_list(list_id=None):    
    items = None
    shop_list = ShoppingList.get_list(list_id)
    if request.method == 'POST':
        itemname = request.form['itemname']
        quantity = request.form['quantity']
        price = request.form['price']
        list_id = request.form['list_id']

        shop_list = ShoppingList.get_list(list_id)
        shop_list.add_item(itemname, int(quantity), price)
        
    items = shop_list.get_items()
    print(items)
    return render_template('items.html', items=items, list_id=list_id)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['username'] = None
    return redirect(url_for('login_user'))


@app.route('/delete_list/<list_id>')
def delete_list(list_id=None):
    for list_object in SHOPPING_LISTS:
        if list_object.id == list_id:
            SHOPPING_LISTS.remove(list_object)
            return redirect(url_for('shopping_list'))


'''
@app.route('delete_item')
def delete_item():
    return render_template('items.html')


@app.route('/edit_item')
def edit_item():
    return render_template('list_details.html')
'''


#app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "campboot_ladena"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://DB_USER:PASS@HOST/DB'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(**POSTGRES)
#POSTGRES = {
#    'user': 'postgres',
#    'password': '',
#    'host': 'localhost',
#    'port': '5432',
#    'db': 'dev',
#}


#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port='5050')

##run like gunicorn --bind 0.0.0.0:9050 wsgi:app


