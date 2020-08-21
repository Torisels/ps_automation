from json import JSONEncoder
import math


class ItemEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Item:
    def __init__(self, number, product_id, name, description_1, description_2, description_3, ikea_id, eur, usd, cny,
                 badge_type, comment, scale=58, *args, **kwargs):
        self.id = number
        self.file_name = str(product_id) + ".jpg"
        self.name = name
        if type(name) == str:
            self.name = name
        elif not math.isnan(name):
            self.name = name
        else:
            self.name = ""

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
        self.lines = 2
        self.psd_name = str(self.id) + '_' + self.ikea_id + '.psd'
        self.new_name = str(self.id) + '_' + comment
        self.ikea_id = comment

        if badge_type == "Special offer":
            self.special_offer = True
        else:
            self.special_offer = False
        self.description = self.make_description_doormats3(description_1, description_2, description_3)

    @staticmethod
    def make_description_doormats(d1: str, d2: str, d3: str):
        d3 = d3.split(" ")
        final = f"{d1} {d3[0]} cm\r"
        d2 = " ".join(d2.split(" ")[1:])
        final += f"{d2}\r{d3[2]}"
        return final

    def make_description_doormats2(self, d1: str, d2: str, d3: str):
        self.lines = 2
        self.description_2 = ""
        d3 = d3.split(" ")
        final = f"{d1} {d3[0].replace('CM', ' cm')}\r"
        final += f"{' '.join(d3[1:])}"
        return final

    def make_description_doormats3(self, d1: str, d2: str, d3: str):
        self.lines = 3
        self.description_2 = ""
        d3 = d3.split(" ")
        final = f"{d1} {d3[0].replace('CM', ' cm')}\r"
        final += f"{(' '.join(d3[3:])).lower()}\r{(' '.join(d3[1:3])).lower()}"
        return final

    @staticmethod
    def make_description_accessories(d1: str, d2: str, d3: str):
        d3 = d3.replace("cms", "cm")
        d3 = d3.replace("100% ", "")
        d3 = d3.rstrip()
        s = d3.split(" ")
        s[0] += " cm"
        d3 = " ".join(s)
        return d1 + "\r" + d3

    @staticmethod
    def get_file_name(product_id: str, **kwargs):
        return str(product_id) + ".jpg"


    @staticmethod
    def price_check(price: float):
        if type(price) == str:
            return float(price)

        if type(price) == int:
            return price

        if price.is_integer():
            return int(price)
        return price
