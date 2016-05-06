import datetime
import pandas as pd
from Report import Report

class DataPrep:
    def __init__(self, company_name, file_location, price_no_change_margin=.01):
        self.reports = []
        self.company_name = company_name
        self.file_location = file_location
        self.price_no_change_margin = price_no_change_margin
        self.data = pd.read_csv("ReducedPrices/"+self.company_name+".csv", header=0)
        self.get_report_dates()


    '''
    Store separated reports in individual Report objects
        that hold the date of the report and text and price changes
    '''
    def get_report_dates(self):
        file = open(self.file_location+"ReducedReports/"+self.company_name+".txt")
        raw = file.read()
        file.close()
        raw = raw.strip()
        raw_reports = raw.split("End_of_report")

        # Split up reports
        for index, report in enumerate(raw_reports):
            # split reports by date and text

            # getting a empty string from the last split. This seemed like the least hacky way to handle it
            if report is "":
                continue
            report = report.split("REPORT")
            date = datetime.datetime.strptime(report[0].strip(), "%Y%m%d")
            text = report[1]
            self.reports.append(Report(date, text, self.price_no_change_margin, *self.get_prices(date)))


    def get_prices(self, date):
        # convert from a date into a string to check with the array of dates/prices
        str_date = date.strftime('%Y-%m-%d')
        index = self.data[self.data['Date'] == str_date].index.tolist()

        # if there is no associated price on that day, go to the next day
        while not index:
            # convert back into a date
            str_date = datetime.datetime.strptime(str_date, '%Y-%m-%d')
            # increment to the next day
            str_date += datetime.timedelta(days=1)
            # convert back into a string to look up for a corresponding price for this new date
            str_date = str_date.strftime('%Y-%m-%d')
            index = self.data[self.data['Date'] == str_date].index.tolist()

        opening = self.data.at[index[0], 'Open']
        day1_closing = self.data.at[index[0], 'Close']
        day3_closing = self.data.at[index[0]-2, 'Open']
        day5_closing = self.data.at[index[0]-4, 'Open']

        return opening, day1_closing, day3_closing, day5_closing

#test = DataPrep('AAPL')


