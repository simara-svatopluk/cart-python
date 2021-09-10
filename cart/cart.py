from abc import abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Dict


class Prices:
    @abstractmethod
    def price_for(self, productId: str) -> Decimal: raise NotImplemented()


class Cart:
    def __init__(self):
        self.__items: Dict[str, CartItem] = {}

    def add(self, productId: str) -> None:
        if productId in self.__items:
            self.__items[productId] = self.__items[productId].add(1)
        else:
            self.__items[productId] = CartItem(productId, 1)

    def items(self, prices: Prices) -> list:
        return list(map(lambda i: i.to_item(prices), self.__items.values()))

    def remove(self, productId: str) -> None:
        if productId not in self.__items:
            raise ProductNotInCart

        del self.__items[productId]


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
