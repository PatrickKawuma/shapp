__author__ = "patrick"
import uuid
import datetime
from flask import session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON


db = SQLAlchemy()


class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    '''
    def __repr__(self):

        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })
    
    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }
    '''


class User(BaseModel, db.Model):
    """Model for user table"""
    __tablename__ = 'users'
#    __table_args__ = {"schema":"flask"}

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(25))
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    lists = db.relationship('ShoppingList', backref='user', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.created = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.updated = None

    
    def create_in_db(self):
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    def json_dump(self):
        return dict(username=self.username, password=self.password)


    @classmethod
    def get_user(cls, user_name):
        user = User.query.filter_by(username=user_name).first()
        #if user_object.username == username:
        if user:
            #return user_object
            return user
        return None


    @staticmethod
    def login_valid(username_field, password_field):
        user = User.query.filter_by(username=username_field).first()
            #user_exists = user.get_user(username_field)
        if user:
            #confirm password
            return user.password == password_field
        return False

    @staticmethod
    def login(username):
        session['username'] = username

    @classmethod
    def register(cls, username, password):
        user = cls.get_user(username)
        if user is None:
            new_user = cls(username, password)
            new_user.create_in_db()
            session['username'] = username
            new_user.login(new_user.username)
            return True
        return False

    @staticmethod
    def logout():
        #session.pop('username', None)
        session['email'] = None

    def create_list(self, list_name, budget):
        return ShoppingList(list_name, budget, self.id)


    def serialize_lists(self, list_id=None):
        lists = ShoppingList.query.all()
        if list_id:
            slist = ShoppingList.query.get(list_id)
            if slist:
                return slist.json_dump()
            return None
        return [l.json_dump() for l in lists]


    def add_item(self, item_name, quantity, shopping_list):
        return shopping_list.add_item(item_name, quantity, price)

    def delete_item(self, item_name, shopping_list):
        return shopping_list.remove_item(item_name)

    def edit_item(self, shopping_list, data): #data expected as item_name, quantity and price
        return shopping_list.edit_item_data(**data)


class ShoppingList(BaseModel, db.Model):
    """Model for the shoppings table"""
    __tablename__ = 'lists'
#    __table_args__ = {"schema":"flask"}

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120))
    budget = db.Column(db.Float)
    created = db.Column(db.DateTime, server_default=db.func.now())
    #items = db.relationship('Item', backref='list', lazy='dynamic') ## points to the Item class
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    items = db.relationship('Item', backref='list', lazy='dynamic')


    def __init__(self, name, budget, user): #takes arguments of list_name(str), budget(float) and a user object
        print("initialising")
        print(type(user))
        self.name = name
        self.budget = budget
        self.user_id = user


    def create_in_db(self):
        db.session.add(self)
        db.session.commit()
        return True


    def json_dump(self):
        return dict(id=self.id,
                    name=self.name,
                    budget=self.budget,
                    created=self.created,
                    user_id=self.user_id
                   )


    def get_items(self):
        items = Item.query.filter_by(list_id=self.id)
        return items

    def get_item(self, item_id):
        if item_id:
            item = Item.query.get(item_id)


    def delete_item(self, item_id=None):
        if item_id:
            Item.query.delete(item_id)
            return "Item deleted"
        return "404, Item not found"


    def serialize_items(self):
        items = self.get_items()
        data = [item.json_dump() for item in items]
        return data

    
    def add_item(self, item_name, quantity, price):
        item = Item(item_name, price, self, quantity)
        print(item.list_id)
        item.create_in_db()

    '''
    def remove_item(self, item_name):
        del self.items[item_name]
    '''

    @classmethod
    def get_list(cls, list_id):
        shop_list = cls.query.get(list_id)
        if shop_list:
             return shop_list
        return None


    @staticmethod
    def edit_item_data(item_id, item_name, quantity, price):
        item = Item.query.get(item_id)
        if item:
            item.name = item_name
            item.quantity = quantity
            item.price = price
            return item
        return False


class Item(BaseModel, db.Model):
    """Model for the items table"""
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120))
    quantity = db.Column(db.Float, )
    price = db.Column(db.Float, )
    added_on = db.Column(db.DateTime, server_default=db.func.now())
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'), nullable=False)

    def __init__(self, name, price, slist, quantity=1):
         self.name = name
         self.quantity = quantity 
         self.price = price
         #self.list_id = slist.id 
         
    def create_in_db(self):
        db.session.add(self)
        db.session.commit()
        return True

    def json_dump(self):
        return dict(id=self.id, 
                    name=self.name, 
                    quantity=self.quantity, 
                    price=self.price,
                    added=self.added_on,
                    list_id=self.list_id
                   )

    @classmethod
    def delete_item(cls, item_id):
        item = Item.query.get(item_id)
        db.session.delete(item)
        db.session.commit()
        return True

    def edit_data(self, name, quantity, price):
        item = Item.query.get(self.id)

        item.name = name
        item.quantity = quantity
        item.price = price
        db.session.commit()
        return True

    @classmethod
    def get_item(cls, item_id):
        item = cls.query.get(item_id)
        if item:
             return item
        return None

'''
class Item:
    def __init__(self, name, quantity, price):
         self.name = name
         self.quantity = 1 #default
	 self.price = price
'''

'''
SHOPPING_LISTS = []
USERS = []


class ShoppingList:
    def __init__(self, list_name, budget, user): #takes arguments of list_name(str), budget(float) and a user object
        self.name = list_name
        self.budget = budget
        self.items = {}
        self.created = datetime.datetime.today().strftime('%Y-%m-%d')
        self.id = uuid.uuid4().hex
        self.user_id = user.id

    def add_item(self, item_name, quantity, price):
        if isinstance(item_name, str) and isinstance(quantity, int):
            self.items.update({item_name : {'quantity' :quantity, 'price': price}})


    def remove_item(self, item_name):
        del self.items[item_name]


    @classmethod
    def get_list(cls, list_id):
        for shop_list in SHOPPING_LISTS:
            if shop_list.id == list_id:
                 return shop_list
        return None


    #@classmethod
    def get_items(self):
        return self.items


    def edit_item_data(self, item_name, quantity, price):
            self.items[item_name]['quantity'] = quantity
            self.items[item_name]['price'] = price


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.created = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.id = uuid.uuid4().hex


    @classmethod
    def get_user(cls, username):
        for user_object in USERS:
            if user_object.username == username:
                return user_object
        return None


    @staticmethod
    def login_valid(username_field, password_field):
        for user in USERS:
            user_exists = user.get_user(username_field)
            if user_exists:
                #confirm password
                return user_exists.password == password_field
        return False

    @staticmethod
    def login(username):
        session['username'] = username

    @classmethod
    def register(cls, username, password):
        user = cls.get_user(username)
        if user is None:
            new_user = cls(username, password)
            USERS.append(new_user)
            session['username'] = username
            new_user.login(new_user.username)

            return True
        return "user already exists"

    @staticmethod
    def logout():
        #session.pop('username', None)
        session['email'] = None

    def create_list(self, list_name, items):
        return ShoppingList(list_name, budget, self.id)

    def view_lists(self):
        return [x for x in SHOPPING_LISTS if x.user_id == self.id]

    def remove_list(self, list_name):
        for list_object in SHOPPING_LISTS:
            if list_object.name == list_name and list_object.user_id == self.user_id:
                SHOPPING_LISTS.remove(list_object)


    def add_item(self, item_name, quantity, shopping_list):
        return shopping_list.add_item(item_name, quantity, price)

    def delete_item(self, item_name, shopping_list):
        return shopping_list.remove_item(item_name)

    def edit_item(self, shopping_list, data): #data expected as item_name, quantity and price
        return shopping_list.edit_item_data(**data)

'''
'''
    def edit_shoppinglist(self, list_name):
        for list_object in SHOPPING_LISTS:
            if list_object.name == list_name and list_object.user_id == self.user_id:

'''



