import sys
sys.path.append('/Users/tahaakbarally/Documents/TNK/tnkai/')

import math
import pandas as pd
from lookup import Lookup
from embeddable import Embeddable, Similarity
from clientWrapper import ClientWrapper

"""
A bunch of nonsense
"""
class Industry(Embeddable):
    
    def __init__(self, name : str, client : ClientWrapper, employed_totals : int = 0, gov_industries : list = None):
        self.employed_totals = employed_totals
        super().__init__(name, client)

        if (gov_industries != None):
            self.industry_matches = Similarity(self, gov_industries, math.inf)

"""
A wrapper to easily access the labour force data
"""
class GovernmentData():

    DATA_FILE = "/Users/tahaakbarally/Documents/TNK/tnkai/data/6291004.xlsx"
    INDEX_SHEET = "Index"; DATA_SHEET = "Data1"; ENQUIRIES_SHEET = "Enquiries"

    def __init__(self):
        self.raw_gov_data = pd.read_excel(self.DATA_FILE, sheet_name=self.DATA_SHEET)
        self.get_gov_data()

    def get_gov_data(self):
        self.gov_data = {}

        for raw_name, raw_values in self.raw_gov_data.items():
            name = GovernmentData.get_name_from_index(raw_name)
            series_type = raw_values.iloc[1]
            last_val = raw_values.iloc[-1]
            if (not name in self.gov_data):
                self.gov_data[name] = {}
            self.gov_data[name][series_type] = last_val

    def get_name_from_index(index):
        return index.split(sep=" ; ")[0]


# Get the TNK industry names.
def get_tnk_industry_names():
    tnk_industry_codes = Lookup.get_industry_codes()
    tnk_industry_names = [code.name for code in tnk_industry_codes]
    return tnk_industry_names

def main():
    client = ClientWrapper(limit=True)
    # gov_industry_names = get_gov_industry_names()
    # tnk_industry_names = get_tnk_industry_names()

    # gov_industries = [Industry(industry, client) for industry in gov_industry_names]
    # tnk_industry = Industry(tnk_industry_names[0], client, gov_industries=gov_industries)
    # print("finished")

if __name__ == "__main__":
    main()
    
