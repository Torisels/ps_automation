from json import JSONEncoder
import math
import re


class ItemEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class Item:
    def __init__(self, number, product_id, name, description_1, description_2, description_3, ikea_id, eur, usd, cny,
                 gbp,
                 badge_type, comment, collection_num, scale=58, *args, **kwargs):
        self.id = number
        self.collection_name = "HFB" + str(collection_num).zfill(2)
        # self.collection_name = str(collection_num).zfill(2)
        self.file_name = str(product_id).strip() + ".jpg"
        self.name = name
        if type(name) == str:
            self.name = name.strip()
        elif not math.isnan(name):
            self.name = name
        else:
            self.name = ""

        self.price_line_count = 0
        self.description_1 = description_1
        self.description_2 = str(description_2)
        self.description_3 = description_3
        self.description = ""
        self.ikea_id = str(ikea_id).strip()
        self.eur = self.price_check(eur)
        self.usd = self.price_check(usd)
        self.cny = self.price_check(cny)
        self.gbp = self.price_check(gbp)
        self.price_string = self.generate_price_string()
        self.scale = scale
        self.more_options = False
        self.lines = 2
        if len(self.name) == 0:
            self.lower = True
        else:
            self.lower = False
        self.psd_name = str(self.id).zfill(2) + '_' + self.name.strip() + '_' + str(self.collection_name).zfill(
            2) + '.psd'
        # self.new_name = str(self.id) + '_' + comment
        # self.ikea_id = comment

        if badge_type == "Special offer":
            self.special_offer = True
        else:
            self.special_offer = False
        self.description = self.make_description_basic1(description_1, description_2, description_3)

    def make_description_hfb133(self, d1: str, d2: str, d3: str):
        d1 = d1.lower()
        d3 = d3.lower()
        d1 = d1.strip()
        d3 = d3.strip()
        d3 = re.sub(r"(\s?\d{1,3}%)", '', d3)
        d2 = re.sub(r"(\s?\d{1,3}%\s?)", '', d2)
        d3 = d3.replace("  ", " ")
        d4 = d3.split(" ")


        final = f"{d1} {d4[0]} cm\r{d2}\r{d4[1]}"
        final = final.replace("\r ", "\r")
        self.lines = final.count("\r") + 1
        return final



    def make_description_hfb15(self, d1: str, d2: str, d3: str):
        d1 = d1.lower()
        d3 = d3.lower()
        d1 = d1.strip()
        d3 = d3.strip()
        d3 = re.sub(r"(\s?\d{1,3}%)", '', d3)
        # d2 = re.sub(r"(\s?\d{1,3}%)", '', d2)
        d3 = d3.replace("  ", " ")
        d4 = d3.split(" ")
        d6 = d4[0].replace("cm", " cm")
        d5 = " ".join(d4[1:])

        final = f"{d1} {d6}\r{d5}"
        final = final.replace("\r ", "\r")
        self.lines = final.count("\r") + 1
        return final


    def make_description_hfb11(self, d1: str, d2: str, d3: str):
        d1 = d1.lower()
        d3 = d3.lower()
        d1 = d1.strip()
        d3 = d3.strip()
        d3 = re.sub(r"(\s?\d{1,3}%)", '', d3)
        d2 = re.sub(r"(\s?\d{1,3}%)", '', d2)
        d3 = d3.replace("  ", " ")

        final = f"{d1}\r{d2}\r{d3}"
        final = final.replace("\r ", "\r")
        self.lines = final.count("\r") + 1
        return final

    def make_description_farmhouse_remove_percent(self, d1: str, d2: str, d3: str):
        d1 = d1.lower()
        d3 = d3.lower()
        d1 = d1.strip()
        d3 = d3.strip()

        d3 = re.sub(r"(\s\d{1,3}\s?%)", '', d3)

        d4 = d3.split(", ")



        d5 = ", ".join(d4[1:])
        d5 = d5.replace("  ", " ")

        final = f"{d1} \r{d4[0]} cm\r{d5}"
        self.lines = final.count("\r") + 1+1
        return final

    def make_description_farmhouse(self, d1: str, d2: str, d3: str):
        d1 = d1.lower()
        d3 = d3.lower()
        d1 = d1.strip()
        d3 = d3.strip()

        # d3 = d3[:-1]
        d4 = d3.split(", ")



        d5 = ", ".join(d4[1:])
        d5 = d5.replace("  ", " ")

        final = f"{d1} {d4[0]} cm\r{d5}"
        self.lines = final.count("\r") + 1
        return final


    def make_description_hfb14(self, d1: str, d2: str, d3: str):
        d1 = d1.lower()
        d3 = d3.lower()
        d1 = d1.strip()
        d3 = d3.strip()

        d3 = d3[:-1]
        d4 = d3.split(",")



        d5 = ", ".join(d4[1:])
        d5 = d5[1:]
        d5 = d5.replace("  ", " ")

        final = f"{d1} {d4[0]} cm\r{d5}"
        self.lines = final.count("\r") + 1
        return final

    # def make_description_hfb15(self, d1: str, d2: str, d3: str):
    #     d1 = d1.lower()
    #     d3 = d3.lower()
    #     d1 = d1.strip()
    #     d3 = d3.strip()
    #
    #     # d3 = d3.replace("cm", " cm")
    #     d3 = d3.replace("cms", " cm")
    #     d3 = d3.replace("100%", "")
    #     d4 = d3.split(", ")
    #
    #     final = f"{d1} {d4[0]}\r{d4[2]}\r{d4[1]}"
    #     self.lines = final.count("\r") + 1
    #     return final

    def make_description_hfb17(self, d1: str, d2: str, d3: str):
        d1 = d1.lower()
        d3 = d3.lower()
        d1 = d1.strip()
        d3 = d3.strip()

        d1 = d1.replace(" eucalyptus", "")

        final = f"{d1}\r{d3}"
        self.lines = final.count("\r") + 1
        return final

    def make_description_splitd3(self, d1: str, d2: str, d3: str):
        d1 = d1.lower()
        d3 = d3.lower()
        d1 = d1.strip()
        d3 = d3.strip()

        d4 = d3.split(" xx ")

        final = f"{d1}\r{d4[0]}\r{d4[1]}"
        self.lines = final.count("\r") + 1
        return final

    def make_description_basic3(self, d1: str, d2: str, d3: str):
        d1 = d1.lower()
        d3 = d3.lower()
        d2 = d2.strip()
        d2 = d2.lower()
        d1 = d1.strip()
        d3 = d3.strip()
        d3 = re.sub(r"(\s\d{1,3}%)", '', d3)
        # d2 = re.sub(r"(\d{1,3}%\s)", '', d2)
        d3 = d3.replace("  ", " ")

        final = f"{d1}\r{d2}\r{d3}"
        self.lines = final.count("\r") + 1
        return final

    def make_description_basic(self, d1: str, d2: str, d3: str):
        # d1 = d1.lower()
        # d3 = d3.lower()
        d3 = d3.replace("cm", " cm")
        d3 = d3.replace("160mm", "")
        # d2 = d2.strip()
        # d2 = d2.lower()
        d1 = d1.strip()
        d3 = d3.strip()
        d3 = re.sub(r"(\s\d{1,3}%)", '', d3)
        # d2 = re.sub(r"(\d{1,3}%\s)", '', d2)
        d3 = d3.replace("  ", " ")

        # final = f"{d1} 320 mm\r{d3}"
        final = f"{d1}"
        self.lines = final.count("\r") + 1
        return final

    def make_description_basic1(self, d1: str, d2: str, d3: str):
        # d1 = d1.lower()
        # d3 = d3.lower()
        self.description_3 = ""
        # d2 = d2.strip()
        # d2 = d2.lower()
        d1 = d1.strip()


        final = f"{d1}"
        self.lines = 2
        return final

    def make_description_hfb18(self, d1: str, d2: str, d3: str):
        d1 = d1.lower()
        d3 = d3.lower()
        d1 = d1.strip()
        d3 = d3.strip()

        d4 = d3.split(" ")
        d3 = " ".join(d4[1:])

        final = f"{d1}\r{d4[0]} cm\r{d3}"

        self.lines = final.count("\r") + 1
        return final

    def make_description_hfb12(self, d1: str, d2: str, d3: str):
        d1 = d1.lower()
        d3 = d3.lower()
        d3 = d3.strip()

        # d4 = d3.split(" cm ")
        # d2 = d2.replace("  ", ' ')
        # d2 = d2.replace("100% ", "")
        # d4[0] = d4[0].replace("x ", "x")

        # d2 = d3.split("100% ")[1]
        # d2 = d2.replace("100% ", "")
        # d2 = d2.replace("  ", " ")
        #
        # d1 = d1.strip()
        # d3 = d3.split("100% ")[0]
        # d4 = d3.split(" ")
        # d2 = d2.lower()
        final = f"{d1}\r{d2}\r{d3}"

        self.lines = final.count("\r") + 1
        return final

    def make_description_centimeters_two_lines(self, d1: str, d2: str, d3: str):
        self.lines = 2
        d1 = d1.lower()
        d2 = d2.lower()
        d3 = d3.lower()
        d3 = d3.strip()
        d1 = d1.strip()

        d3 = d3.split(" ")
        final = f"{d1} \r{d3[0]} cm "
        d2 = " ".join(d3[1:])
        final += f"{d2}"
        # final = f"{d1[0]}\rwith {d1[1]}, {d3}"
        return final

    def make_description_hfb6(self, d1: str, d2: str, d3: str):
        self.lines = 2
        d1 = d1.lower()
        d2 = str(d2)
        d2 = d2.lower()
        d3 = d3.lower()
        self.description_2 = ""
        self.lower = True

        final = f"{d1}\r{d3}"
        return final
        #
        d3 = d3.split(" ")
        final = f"{d1} \r{d3[0]} cm "
        d2 = " ".join(d3[1:])
        final += f"{d2}"
        # final = f"{d1[0]}\rwith {d1[1]}, {d3}"

        return final

    # def make_description_hfb12(self, d1: str, d2: str, d3: str):
    #     self.lines = 3
    #     d1 = d1.lower()
    #     d2 = str(d2)
    #     d2 = d2.lower()
    #     d3 = d3.lower()
    #
    #     final = f"{d1}\r{d3}"
    #     return final
    #     #
    #     d3 = d3.split(" ")
    #     final = f"{d1} \r{d3[0]} cm "
    #     d2 = " ".join(d3[1:])
    #     final += f"{d2}"
    #     # final = f"{d1[0]}\rwith {d1[1]}, {d3}"
    #
    #     return final

    def make_description_toys(self, d1: str, d2: str, d3: str):
        self.lines = 2
        d1 = d1.lower()
        d2 = d2.lower()
        if type(d3) == float:
            d3 = " "
        d3 = d3.lower()
        d3 = d3.replace("cms", " cm")
        d3 = d3.replace("cm", " cm")
        # d3 = d3.split("dia, ")

        final = f"{d1}\r{d3}"

        # d3 = d3.split(" ")
        # final = f"{d1}\r{d3[0]} cm "
        # d2 = " ".join(d3[1:])
        # final += f"{d2}"
        return final

    def make_description_jajpur(self, d1: str, d2: str, d3: str):
        self.lines = 3
        d1 = d1.lower()
        d2 = d2.lower()
        if type(d3) == float:
            d3 = " "
        d3 = d3.lower()
        d3 = d3.replace("cms", " cm")
        d3 = d3.split("dia, ")

        final = f"{d1}\r{d3[0]}dia. \r{d3[1]}"

        # d3 = d3.split(" ")
        # final = f"{d1}\r{d3[0]} cm "
        # d2 = " ".join(d3[1:])
        # final += f"{d2}"
        return final

    def make_description_celebration(self, d1: str, d2: str, d3: str):
        self.lines = 2
        self.description_2 = ""
        d1 = d1.lower()
        d3 = d3.lower()
        d3 = d3.replace("100% ", "")
        d3 = re.sub(r"((\d{1,4})x(\d{1,4}))", r"\1 cm", d3)
        arr = d3.split(", ")
        d3 = ", ".join(arr[1:])
        final = f"{d1} {arr[0]}\r{d3}"
        return final

    def make_description_hfb42(self, d1: str, d2: str, d3: str):
        self.lines = 2
        if type(d3) == str:
            d3 = d3.strip()
            if 'x' in d3:
                d4 = d3.split(" ")
                d4[1] += " cm"

        return d1 + ' ' + d4[1] + "\r" + str(d4[0])

    def make_description_hfb4(self, d1: str, d2: str, d3: str):
        self.lines = 2
        d4 = list()
        d4.append("")
        if type(d3) == str:
            d3 = d3.strip()
            if 'x' in d3:
                d4 = d3.split(" ")
                d4[0] += " cm"
                d3 = " ".join(d4[1:])
        return d1 + '\r' + d4[0] + " " + str(d3)

    def make_description_hfb5(self, d1: str, d2: str, d3: str):
        self.lines = 2
        if type(d3) == str:
            d3 = d3.strip()
            if 'x' in d3:
                d4 = d3.split(" ")
                d4[0] += " cm"
                d3 = " ".join(d4)
        return d1 + '\r' + str(d3)

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
        return str(product_id).strip() + ".jpg"

    @staticmethod
    def price_check(price: float):
        if type(price) == str:
            a = str(price).replace(",.", ".")
            a = str(price).replace(".,", ".")
            return float(a)

        if type(price) == int:
            return price

        if price.is_integer():
            return int(price)

        if math.isnan(price):
            return -1

        return price

    def generate_price_string(self):
        line_counter = 0
        eur = ""
        usd = ""
        cn = ""
        gbp = ""
        if self.eur != -1:
            eur = f"(DE) {self.eur} EUR\r"
            line_counter += 1
        if self.usd != -1:
            usd = f"(US) {self.usd} USD\r"
            line_counter += 1
        if self.cny != -1:
            cn = f"(CN) {self.cny} CNY\r"
            line_counter += 1
        if self.gbp != -1:
            gbp = f"(GB) {self.gbp} GBP\r"
            line_counter += 1

        self.price_line_count = line_counter
        return eur + usd + cn + gbp
