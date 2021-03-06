'''
Preprocessing class that cleans up the reports as they contain html elements which do not provide
much in this application. It also strips away punctuation as the reports do not have much emotion.
If analyzing analysts writing, or market sentiment, punctuation may be more useful.
'''

import nltk
import string
import datetime
import Report
import pandas as pd
from bs4 import BeautifulSoup


class DataReducer:
    def __init__(self, company_name, starting_date):
        self.reports = None
        self.company_name = company_name
        self.starting_date = starting_date
        self.last_stock_data = datetime.date(2013, 2, 1)
        self.reduce_reports()
        # Performing initial preprocessing takes some time, this is a more of a sanity check to ensure the program
        # is actually working and not stuck
        print(company_name, " report done")


    '''
    Split the reports in a file by date and save tokenize the text in a Report
        object that holds the date of the report and text
    '''
    def reduce_reports(self):
        file = open("2010ReducedReports/"+self.company_name+".txt")
        raw = file.read()
        # remove html elements
        soup = BeautifulSoup(raw.translate(string.punctuation), "lxml")
        raw = soup.getText()
        # split up reports using a delimiter "TIME:" which appears before each separate report
        raw_reports = raw.split("TIME:")
        # first element has all the header stuff leading into the first report so we can remove it
        raw_reports.pop(0)
        self.reports = []#[Report.Report()] * len(raw_reports)

        '''
        Separate each report by the date and the text
            Remove numbers and punctuation from the text and make it all lower case.
        '''
        for index, report in enumerate(raw_reports):
            report = report.split("+EVENTS")
            date = datetime.datetime.strptime(report[0], "%Y%m%d%H%M%S").date()
            # Skip over dates earlier than the starting time. This shrinks our training/testing size
            # and simplifies the model so things can run faster
            if date < self.starting_date or date > self.last_stock_data:
                continue
            text = report[1].replace("*", " ")
            text = text.lower()
            tokens = nltk.word_tokenize(text, language='english')
            # remove common stop words.
            '''
            FUTURE UPDATE: get word counts across all documents in the corpus to identify stop words
                instead of using NLTK's stop word corpus.
            '''
            words = [w for w in tokens if w.isalpha() ]
            '''
            Removing stop words will be handled by the Sklearn Naive Bayes algorithm
            tried performing stemming here, but the Sklearn estimator did had issues with
            removing stop words after the data was stemmed
            '''
            # 0-8 are the data for the date of the report in this form: "YYYYMMDD"
            cur_report = Report.Report(report[0][:8], " ".join(words))
            '''
            The report here was changed later so for this to run, the calculate_classifiers method must be
            commented out. I tried to add a if statement to check and circumvent this problem
            but I think it would be better to rewrite it with a parent and child class
            '''
            self.reports.append(cur_report)

        # File names have to be changed manually in the future when processing more data
        # Need to update this as well
        cur_file = open('2010ReducedReports/'+self.company_name+'.txt', 'w')
        for report in self.reports:
            cur_file.write(report.date)
            cur_file.write(" REPORT ")
            cur_file.write(report.text)
            cur_file.write(" End_of_report ")
        cur_file.close()


    def reduce_prices(self):
        data = pd.read_csv("prices/"+self.company_name+".csv", header=0)

        date = self.starting_date.strftime('%Y-%m-%d')
        data = data[data['Date'] > date]
        data.to_csv("ReducedPrices/"+self.company_name+".csv", index=False)


# Companies that need to be in the folder to process
companies = ['AAPL', 'MSFT', 'GOOG', 'SNDK', 'IBM', 'HPQ' ]

for company in companies:
    test = DataReducer(company, datetime.date(2010, 1, 1))