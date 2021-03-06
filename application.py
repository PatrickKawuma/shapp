__author__ = 'patrick'
import os


from .models.models import db, User, ShoppingList, Item
#from models.models import db, User, ShoppingList, Item
from flask import Flask, render_template, request, session, url_for, redirect, jsonify, abort, make_response
import json

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
        if '@' not in username:
            return render_template('registration.html')
        password = request.form['password']
        created = User.register(username, password)
        if created:
            return redirect(url_for('shopping_list'))
        return render_template('registration.html')
    return render_template('registration.html')


@app.route('/lists', methods=['GET', 'POST'])
def shopping_list():

    user = User.get_user(session['username'])
    if request.method == "POST":
        name = request.form['listname']
        budget = request.form['budget']
        username = request.form['username']

        shop_list = ShoppingList(name, budget, user)
        shop_list.create_in_db()

        lists = user.view_lists()
        return render_template('shoppinglists.html', result=lists, user=session['username'])

    else:
        lists = user.view_lists()

        search_q = request.args.getlist('searchlist')
        if search_q:
            lists = ShoppingList.query.filter(ShoppingList.name.contains(search_q[0]))

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
    
    #search_q = request.args.getlist('searchitem')
    #if search_q:
    #    items = Item.query.filter(Item.name.contains(search_q))

    return render_template('items.html', items=items, list_id=list_id, list_name=shop_list.name)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['username'] = None
    return redirect(url_for('login_user'))

@app.route('/edit_list/<int:list_id>', methods=['GET', 'POST'])
def edit_list(list_id):
    shoplist = ShoppingList.get_list(list_id)
    if request.method == 'POST':
        name = request.form.getlist('listname')[0]
        budget = request.form.getlist('budget')[0]

        shoplist.name = name
        shoplist.budget = budget
        shoplist.create_in_db()
        return redirect(url_for('shopping_list'))

    else:
        return render_template('edit_list.html', shoplist=shoplist)


@app.route('/delete_list/<list_id>')
def delete_list(list_id=None):
    ShoppingList.delete_list(list_id)
    return redirect(url_for('shopping_list'))


@app.route('/delete_item/<item_id>', methods=['GET', 'DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    list_id = item.list_id
    Item.delete_item(item_id)
    return redirect(url_for('view_list', list_id=list_id))


@app.route('/edit_item/<item_id>', methods = ['GET', 'POST'])
def edit_item(item_id):
    if request.method == 'POST':
        name = request.form.getlist('itemname')[0]
        quantity = request.form.getlist('quantity')[0]
        price = request.form.getlist('price')[0]
        print(name, quantity, price)

        item = Item.query.get(item_id)
        item.edit_data(name, int(quantity), int(price))
#        shop_list = ShoppingList.get_list(list_id)
#        shop_list.edit_item_data(name, quantity, price)
 
        return redirect(url_for('view_list', list_id=item.list_id))

    else:
	#get_items
        #list_id = request.form['list_id']
        print("in get")
        item = Item.query.get(item_id)
        return render_template('edit_item.html', item=item)


###======================================================== APIs =======================================================###

lists = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/auth/register', methods=['POST'])
def api_register():
    pass

@app.route('/auth/login', methods=['POST'])
def api_login():
    pass

@app.route('/auth/logout', methods=['POST'])
def api_logout():
    pass

@app.route('/auth/reset-password', methods=['POST'])
def api_resetpw():
    pass

@app.route('/shoppinglists', methods=['GET'])
def api_get_lists():
    print("in lists")
    user = User.get_user('patrifire@yahoo.com')
    lists = user.serialize_lists()
    return jsonify({'lists': lists})


@app.route('/shoppinglists/<int:list_id>', methods=['GET'])
def api_get_list(list_id):
    user = User.get_user('patrifire@yahoo.com')
    slist = user.serialize_lists(list_id)
    if slist:
        return jsonify({'list': slist})
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/shoppinglists/<int:list_id>/items', methods=['GET'])
def api_get_items(list_id):
    print("in get items for a list")
    user = User.get_user('patrifire@yahoo.com')
    slist = ShoppingList.get_list(list_id)
    if slist:
        return jsonify({'items':slist.serialize_items()}) 
    return make_response(jsonify({'error': 'Not found'}), 400)


@app.route('/shoppinglists', methods=['POST'])
def api_create_list():
    print("in shopping post")
    user = User.get_user('patrifire@yahoo.com')

    name = request.json.get('name')
    budget = request.json.get('budget')
    if name is None or budget is None:
        abort(400)

    new_list = user.create_list(name, int(budget))
    new_list.create_in_db()
    return jsonify({'list': new_list.json_dump()}, 201)


@app.route('/shoppinglists/<int:list_id>', methods=['PUT'])
def api_put_list(list_id):
    shoplist = ShoppingList.get_list(list_id)
    if not shoplist:
        abort(404)
    print(request)
    name = request.json['name']
    budget = request.json['budget']
    
    shoplist.name = name
    shoplist.budget = budget
    shoplist.create_in_db()
    return jsonify({'list': shoplist.json_dump()})


@app.route('/shoppinglists/<int:list_id>', methods=['DELETE'])
def api_delete_list(list_id):
    if not list_id:
        abort(404)
    ShoppingList.delete_list(list_id)
    return jsonify({'result': 'deleted'})


@app.route('/shoppinglists/<int:list_id>/items', methods=['POST'])
def api_post_items(list_id):
    if not request.json or not ('name' and 'quantity' and 'price') in request.json:
        abort(400)
    user = User.get_user('patrifire@yahoo.com')
    slist = ShoppingList.get_list(list_id)
    if slist:
        name = request.json['name']
        quantity = request.json['quantity']
        price = request.json['price']

        slist.add_item(name, quantity, price)
        return jsonify({'items':slist.serialize_items()}) 
    return make_response(jsonify({'error': 'List Not found'}), 400)


@app.route('/shoppinglists/<int:list_id>/items/<int:item_id>', methods=['PUT'])
def api_put_items(list_id, item_id):
    if not request.json or not ('name' or 'quantity' or 'price') in request.json:
        abort(400)
    #user = User.get_user('patrifire@yahoo.com')
    slist = ShoppingList.get_list(list_id)
    if slist:
        item = Item.get_item(item_id)
        if item:
            name = request.json['name']
            quantity = request.json['quantity']
            price = request.json['price']

            item.name = name
            item.quantity = quantity
            item.price = price
            item.create_in_db()

            return make_response(jsonify({'success': 'Item update'}))
        return make_response(jsonify({'error': 'Item not found'}))
    return make_response(jsonify({'error': 'List Not found'}), 400)


@app.route('/shoppinglists/<int:list_id>/items/<int:item_id>', methods=['DELETE'])
def api_delete_item(list_id, item_id):
    slist = ShoppingList.get_list(list_id)
    if not slist:
        abort(404)

    response=Item.delete_item(item_id)
    return make_response(jsonify({'response': response}))
    

'''
def make_public_list(slist):
    new_list = {}
    for field in slist:
        if field == "id":
            new_list['uri'] = url_for('get_list', list_id=slist['id'], _external=True)
        else:
            new_list[field] = slist[field]
    return new_list
'''


POSTGRES = {
    'user': 'postgres',
    'password': '',
    'host': 'localhost',
    'port': '5432',
    'db': 'dev',
}

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "campboot_ladena"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://DB_USER:PASS@HOST/DB'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(**POSTGRES)


db.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9050)

##run like gunicorn --bind 0.0.0.0:9050 wsgi:app


