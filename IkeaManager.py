from pathlib import Path
import pandas as pd


class IkeaManager:
    WORKING_NUMBER = 4

    EXCEL_PATH = r"C:\Users\Gustaw\Documents\BookTu.xlsx"

    RENAMING_DICT = {"NAME": "name", "How to order": "badge_type", "Product type": "description_1",
                     "MATERIAL": "description_2",
                     "Short product description (like: colour, material: wood, plastic, metal, any additional necessary information": "description_3",
                     "Art. / SPR number": "ikea_id", "(DE) EUR": "eur", "(US) USD": "usd", "(CN) CNY": "cny", '(GB) GBP': "gbp",
                     "PE": "product_id"}

    INPUT_PHOTOS_PATH = Path(r"E:\IKEA_ALL_PICS\Pictures for packshots - per team\\")

    def __init__(self):
        self.SHEET_NAME = self.generate_sheet_name()
        # self.SHEET_NAME = "Celebration"
        self.COLLECTION_NAME = self.generate_collection_name()
        # self.COLLECTION_NAME = "Celebration"
        self.INPUT_PHOTOS_PATH = self.INPUT_PHOTOS_PATH / Path(self.COLLECTION_NAME)

    @classmethod
    def generate_sheet_name(cls):
        return f"{cls.WORKING_NUMBER:02d} PA{cls.WORKING_NUMBER:02d}"

    @classmethod
    def generate_collection_name(cls):
        return f"HFB{cls.WORKING_NUMBER:02d}"

    def prepare_df(self):
        xls = pd.ExcelFile(self.EXCEL_PATH)
        df = pd.read_excel(xls, self.SHEET_NAME)

        df.drop(columns=["PA", "Packshot type"], inplace=True)
        df.drop(df.columns[list(df.columns).index("comment") + 2:], axis=1, inplace=True)

        df.rename(columns=self.RENAMING_DICT, inplace=True)
        return df
