import unittest
from app.models.models import ShoppingList, User

class TddShoppingList(unittest.TestCase):
    def setUp(self):
        self.shoplist = ShoppingList()
        
    def test_shoppinglist_error_if_item_quantity_not_float(self):
        self.assertRaises(ValueError, self.add_item, 'candles', 'two', '2000')

    def test_shoppinglist_error_if_itemname_not_string(self):
        self.self.assertRaises(ValueError, self.add_item, 20.5, 2, '2000')

    def test_shoppinglist_error_if_item_price_not_float(self):
        self.self.assertRaises(ValueError, self.add_item, 'candles', 2, 'two_thousand')

    def test_shoppinglist_add_item(self):
        '''
        
        '''
        shoplist = ShoppingList()
        result = shoplist.add_item()   
        self.assertIsInstance()


    def test_user_object_is_not_null(self):
        '''
        check for a foreign key constraint
        @ user exists, since every shopping list must belong to someone
        '''
        shoplist = ShoppingList('name', 'budget', 'user')
        self.assertIsInstance( user, User)


    def test_shoppinglist_edit_item(self):
        '''
        cannot edit an item that doesnt exist
        @ item_name
        '''
        shoplist = ShoppingList()
        result = shoplist.edit_item(self.items, item_name)
        self.assertIn(item_name, result.items)


class TddUser(unittest.TestCase):
    def setUp():
        self.user = User()



