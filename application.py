__author__ = 'patrick'


from models.models import db, User, ShoppingList, Item#, SHOPPING_LISTS, USERS
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
        password = request.form['password']
        created = User.register(username, password)
        if created:
            return redirect(url_for('shopping_list'))
        return render_template('registration.html')
    return render_template('registration.html')


@app.route('/shoppinglists', methods=['GET', 'POST'])
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
        if search_q[0]:
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
    
    search_q = request.args.getlist('searchitem')[0]
    if search_q:
        items = Item.query.filter(Item.name.contains(search_q))

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

@app.route('/lists', methods=['GET'])
def get_lists():
    print("in lists api")
    user = User.get_user('patrifire@yahoo.com')
    lists = user.view_lists()
    print(lists)
    
    #list_json = json.dumps([row._asdict() for row in lists])
    return jsonify({'lists': lists})


@app.route('/lists/<int:list_id>', methods=['GET'])
def get_items(list_id):
    print("in unique list")
    user = User.get_user('patrifire@yahoo.com')
    slist = user.view_lists(list_id)
    if slist:
        return jsonify({'list': slist})
    return make_response(jsonify({'error': 'Not found'}), 404)



@app.route('/lists', methods=['POST'])
def create_list():
    print("in Post")
    user = User.get_user('patrifire@yahoo.com')
    print(type(user))
    if not request.json or not ('name' and 'budget') in request.json:
        abort(400)

    slist = {
        #'id': lists[-1]['id'] + 1,
        'name': request.json['name'],
        'budget': request.json.get('budget', ""),
    }
    name = slist['name']
    budget = int(slist['budget'])
    new_list = user.create_list(name, budget)
    new_list.create_in_db()
    return jsonify({'list': new_list.json_dump()}, 201)


@app.route('/lists/<int:list_id>', methods=['PUT'])
def edit_list(list_id):
    print("in put")
    shoplist = [slist for slist in lists if slist['id'] == list_id]
    if len(slist) == 0:
        abort(404)

    if not request.json:
        abort(400)

    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)

    if 'description' in request.json and type(request.json['description']) != unicode:
        abort(400)

    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)

    shoplist[0]['title'] = request.json.get('title', shoplist[0]['title'])
    shoplist[0]['description'] = request.json.get('description', shoplist[0]['description'])
    shoplist[0]['done'] = request.json.get('done', shoplist[0]['done'])
    return jsonify({'task': shoplist[0]})


@app.route('/lists/<int:task_id>', methods=['DELETE'])
def delete_task(list_id):
    shoplist = [slist for slist in lists if slist['id'] == list_id]
    if len(slist) == 0:
        abort(404)
    lists.remove(shoplist[0])
    return jsonify({'result': True})


def make_public_list(slist):
    new_list = {}
    for field in slist:
        if field == "id":
            new_list['uri'] = url_for('get_list', list_id=slist['id'], _external=True)
        else:
            new_list[field] = slist[field]
    return new_list


#print(lists)

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


