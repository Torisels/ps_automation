from json import JSONEncoder
import math


class ItemEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Item:
    def __init__(self, number, product_id, name, description_1, description_2, description_3, ikea_id, eur, usd, cny,
                 scale=70, *args, **kwargs):
        self.id = number
        self.file_name = product_id + ".jpg"
        self.name = ""
        if not math.isnan(name):
            self.name = name
        self.description_1 = description_1
        self.description_2 = description_2
        self.description_3 = description_3
        self.description = ""
        self.ikea_id = ikea_id
        self.eur = self.price_check(eur)
        self.usd = self.price_check(usd)
        self.cny = self.price_check(cny)
        self.scale = scale
        self.more_options = False
        self.special_offer = True
        self.description = self.make_description_doormats(description_1, description_2, description_3)

    @staticmethod
    def make_description_doormats(d1: str, d2: str, d3: str):
        d3 = d3.split(" ")
        final = f"{d1} {d3[0]} cm\r"
        d2 = " ".join(d2.split(" ")[1:])
        final += f"{d2}\r{d3[2]}"
        return final

    @staticmethod
    def price_check(price: float):
        if price.is_integer():
            return int(price)
        return price
