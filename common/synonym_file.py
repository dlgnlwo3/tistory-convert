if 1 == 1:
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import os
import pandas as pd


class SynonymFile:
    def __init__(self, filepath):
        self.filepath = filepath
        self.initData()

    def one_way_data_type(self):
        return {"before": str, "after": str}

    def two_way_data_type(self):
        return {"data": str}

    def initData(self):
        self.filepath = os.path.normpath(self.filepath)
        self.filename = os.path.basename(self.filepath)

        two_way_columns = self.two_way_data_type()
        try:
            self.df_two_way = pd.read_excel(
                self.filepath, converters=two_way_columns, sheet_name="양방향", keep_default_na=""
            )
            self.df_two_way = self.df_two_way.loc[:, list(two_way_columns.keys())]
        except Exception as e:
            print(e)

        one_way_columns = self.one_way_data_type()
        try:
            self.df_one_way = pd.read_excel(
                self.filepath, converters=one_way_columns, sheet_name="일방향", keep_default_na=""
            )
            self.df_one_way = self.df_one_way.loc[:, list(one_way_columns.keys())]
        except Exception as e:
            print(e)

    def output(self):
        print(self.df_two_way)
        print(self.df_one_way)


if __name__ == "__main__":

    synonym_file = SynonymFile(r"D:\Consolework\tistory-convert\excel\유의어DB.xlsx")
    synonym_file.output()
