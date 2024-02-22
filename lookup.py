import pandas as pd

"""
Wrapper to easily access data from the look up table.
"""
class Lookup():

    DATAPATH = 'data/lookup_code.tsv'

    def __init__(self, index, id, type, name) -> None:
        self.index = index
        self.id = id
        self.type = type
        self.name = name

    def __repr__(self) -> str:
        return self.name
    
    """Static methods"""

    def get_role_codes():
        return Lookup.get_data("Role")

    def get_industry_codes():
        return Lookup.get_data("Industry")

    def get_application_codes():
        return Lookup.get_data("AppSelection")
    
    def get_all_job_codes():
        role_codes = Lookup.get_data("Role")
        industry_codes = Lookup.get_data("Industry")
        job_codes = []
        for industry_code in industry_codes:
            for role_code in role_codes:
                if industry_code.id in role_code.id:
                    job_codes.append([industry_code, role_code])
        return job_codes

    def get_data(search_type : str):
        df = pd.read_csv(Lookup.DATAPATH, sep='\t')

        lookup_data = []
        for i in df.iterrows():
            index = i[0]
            content = i[1]

            id = content.iloc[0]
            type = content.iloc[1]
            name = content.iloc[2]
            if (type == search_type):
                lookup_data.append(Lookup(index, id, type, name))

        return lookup_data
    
def main():
    role_codes = Lookup.get_role_codes()
    application_codes = Lookup.get_application_codes()
    industry_codes = Lookup.get_industry_codes()
    print(role_codes)
    print(application_codes)
    print(industry_codes)

if __name__ == "__main__":
    main()