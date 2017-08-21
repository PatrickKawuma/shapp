__author__ = "patrick"
import uuid
import datetime
from flask import session
'''
class Item:
    def __init__(self, name, quantity, price):
         self.name = name
         self.quantity = 1 #default
	 self.price = price
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
    def edit_shoppinglist(self, list_name):
        for list_object in SHOPPING_LISTS:
            if list_object.name == list_name and list_object.user_id == self.user_id:

    '''



