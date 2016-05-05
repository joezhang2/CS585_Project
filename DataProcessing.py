import nltk
import string
import datetime
import Report
from bs4 import BeautifulSoup
import itertools
from nltk.stem.porter import PorterStemmer

class DataProcessor:
    def __init__(self, file_location):
        self.reports = None
        self.file_location = file_location
        self.split_tokenized_reports()

    '''
    Split the reports in a file by date and save tokenize the text in a
        Report object that holds the date and text
    '''
    def split_tokenized_reports(self):
        file = open(self.file_location)
        raw = file.read()
        soup = BeautifulSoup(raw.translate(string.punctuation), "lxml")     # remove html elements
        raw = soup.getText()
        raw_reports = raw.split("TIME:")    # split by a date which appears before each report
        raw_reports.pop(0)      # first element has all the header stuff leading into the first report
        self.reports = [Report.Report()] * len(raw_reports)

        '''
        Separate each report by the date and the text
            Remove numbers and punctuation from the text and make it all lower case.
        '''
        for index, report in enumerate(raw_reports):
            report = report.split("+EVENTS")
            date = datetime.datetime.strptime(report[0], "%Y%m%d%H%M%S").date()
            text = report[1].replace("*", " ")
            text = text.lower()
            tokens = nltk.word_tokenize(text, language='english')
            # remove common stop words.
            # FUTURE UPDATE use TF-IDF to clean up data better in the future for potential performance increases
            words = [w for w in tokens if w.isalpha() and w not in nltk.corpus.stopwords.words('english')]
            words = [PorterStemmer().stem(w) for w in words]   # stem words
            self.reports[index] = Report.Report(date, words)

#test = DataProcessor("reports/ACN.txt")