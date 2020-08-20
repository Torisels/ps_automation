from pathlib import Path
import pandas as pd


class IkeaManager:
    WORKING_NUMBER = 13
    SHEET_NAME = "02 PA02"
    COLLECTION_NAME = "HFB13"
    EXCEL_PATH = r"C:\Users\Gustaw\Documents\Book3-final.xlsx"

    RENAMING_DICT = {"NAME": "name", "How to order": "badge_type", "Product type": "description_1",
                     "MATERIAL": "description_2",
                     "Short product description (like: colour, material: wood, plastic, metal, any additional necessary information": "description_3",
                     "Art. / SPR number": "ikea_id", "(DE) EUR": "eur", "(US) USD": "usd", "(CN) CNY": "cny",
                     "PE": "product_id"}

    INPUT_PHOTOS_PATH = Path("E:/Ikea_Projekt/input_photos/")

    def __init__(self):
        self.SHEET_NAME = self.generate_sheet_name()
        self.COLLECTION_NAME = self.generate_collection_name()
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

        df.drop(columns=["PA", "\"colorswatch\"", "Packshot type"], inplace=True)
        df.drop(df.columns[list(df.columns).index("comment") + 1:], axis=1, inplace=True)

        df.rename(columns=self.RENAMING_DICT, inplace=True)
        return df
