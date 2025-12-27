import pandas

class Analyzer:
    @staticmethod
    def save_table(filename, table, header=False):
        filename = filename + ".csv"
        data_frame = pandas.read_html(table.prettify(), flavor="bs4")
        data_frame[0].to_csv(filename, header=header)
