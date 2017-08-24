from .models import User, Item, ShoppingList
import unittest


class TddUser(unittest.TestCase):
    def setUp():
        self.user = User()

user = User('user@yahoo.com', 'password')
class TddShoppingList(unittest.TestCase):
    def setUp(self):
        self.shoplist = ShoppingList('name', 20000, user)

    def test_is_user_a_User_instance(self):
        self.assertTrue(isinstance(user, User))

    def test_json_dump_method_returns_a_dictionary(self):
        self.assertTrue(isinstance(self.shoplist.json_dump(), dict))

    '''requires integration test with db'''
    #def test_get_list_method_returns_list_object(self):
    #    self.assertTrue(isinstance(self.User.get_list(1), User)) 

shoplist = ShoppingList('name', 20000, user)
class TddItem(unittest.TestCase):
    def setUp(self):
        self.item = Item('name', 3000, shoplist, 2)

    def test_is_shoplist_a_ShoppingList_object(self):
        self.assertTrue(isinstance(shoplist, ShoppingList))

    def test_json_dump_method_returns_a_dictionary(self):
        self.assertTrue(isinstance(self.item.json_dump(), dict))

    '''requires integration test with db connection'''
    #def test_if_edit_method_commits_to_db(self):
    #    self.assertTrue(self.item.edit_data('name', 3, 4000))


class TddUser(unittest.TestCase):
    def setUp(self):
        self.user = User('username', 'password')

    def test_json_dump_method_returns_a_dictionary(self):
        self.assertTrue(isinstance(self.user.json_dump(), dict))
    
    #def test_user_can_logout(self):
    #    self.assertequals(self.user.logout(), None)

    def test_user_can_create_list(self):
        self.assertTrue(isinstance(self.user.create_list('name', 20000), ShoppingList))

    '''requires integration test with db'''
    #def test_user_can_view_lists(self):
    #def test_user_can_add_items_to_list(self):
     

    '''     
    def test_shoppinglist_error_if_item_quantity_not_float(self):
        self.assertRaises(ValueError, self.add_item, 'candles', 'two', '2000')

    def test_shoppinglist_error_if_itemname_not_string(self):
        self.self.assertRaises(ValueError, self.add_item, 'item', 2, 2000)

    def test_shoppinglist_error_if_item_price_not_float(self):
        self.self.assertRaises(ValueError, self.add_item, 'candles', 2, 'two_thousand')
    
    def test_user_object_is_not_null(self):
        
        #check for a foreign key constraint
        #@ user exists, since every shopping list must belong to someone
       
        shoplist = ShoppingList('name', 'budget', 'user')
        self.assertIsInstance( user, User)


    def test_shoppinglist_edit_item(self):
        
        #cannot edit an item that doesnt exist
        #@ item_name

        shoplist = ShoppingList()
        result = shoplist.edit_item(self.items, item_name)
        self.assertIn(item_name, result.items)
    '''    





