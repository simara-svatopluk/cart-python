from abc import abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Dict


class Prices:
    @abstractmethod
    def price_for(self, product_id: str) -> Decimal: raise NotImplemented()


class Cart:
    def __init__(self):
        self.__items: Dict[str, CartItem] = {}

    def add(self, product_id: str) -> None:
        if product_id in self.__items:
            self.__items[product_id] = self.__items[product_id].add(1)
        else:
            self.__items[product_id] = CartItem(product_id, 1)

    def items(self, prices: Prices) -> list:
        return list(map(lambda i: i.to_item(prices), self.__items.values()))

    def remove(self, product_id: str) -> None:
        if product_id not in self.__items:
            raise ProductNotInCart

        del self.__items[product_id]


@dataclass(frozen=True)
class Item:
    id: str
    quantity: int
    price: Decimal


@dataclass(frozen=True)
class CartItem:
    id: str
    quantity: int

    def add(self, quantity) -> 'CartItem':
        return CartItem(
            self.id,
            self.quantity + quantity
        )

    def to_item(self, prices: Prices) -> Item:
        return Item(self.id, self.quantity, prices.price_for(self.id))


class ProductNotInCart(Exception):
    pass
