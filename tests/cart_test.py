import unittest
from decimal import Decimal

from cart.cart import Cart, Item, ProductNotInCart, Prices


class StaticPrices(Prices):
    def __init__(self, prices: dict):
        self.__prices = prices

    def price_for(self, productId: str) -> Decimal:
        return self.__prices[productId]

    @staticmethod
    def with_all_prices():
        return StaticPrices({
            "153": Decimal(15),
            "123": Decimal(12),
        })


class MyTestCase(unittest.TestCase):
    def test_empty_cart_has_empty_items(self):
        cart = Cart()

        expected = []
        self.assertEqual(expected, cart.items(StaticPrices.with_all_prices()))

    def test_add_one_product_to_empty_cart_results_in_one_item(self):
        cart = Cart()
        cart.add("153")
        expected = [Item("153", 1, Decimal(15))]
        self.assertEqual(expected, cart.items(StaticPrices.with_all_prices()))

    def test_add_two_different_products_results_in_two_items(self):
        cart = Cart()
        cart.add("153")
        cart.add("123")
        expected = [Item("153", 1, Decimal(15)), Item("123", 1, Decimal(12))]
        self.assertEqual(expected, cart.items(StaticPrices.with_all_prices()))

    def test_add_one_product_twice_results_in_one_item_with_higher_quantity(self):
        cart = Cart()
        cart.add("153")
        cart.add("153")
        expected = [Item("153", 2, Decimal(15))]
        self.assertEqual(expected, cart.items(StaticPrices.with_all_prices()))

    def test_removing_not_existing_results_in_exception(self):
        cart = Cart()
        self.assertRaises(ProductNotInCart, lambda: cart.remove("123"))

    def test_removing_product_results_in_less_items(self):
        cart = Cart()
        cart.add("153")
        cart.add("123")
        cart.remove("153")
        self.assertEqual(1, len(cart.items(StaticPrices.with_all_prices())))


if __name__ == '__main__':
    unittest.main()
