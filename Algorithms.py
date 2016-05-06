from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from DataPrep import DataPrep
import numpy as np
from sklearn import metrics

import warnings
#warnings.filterwarnings("ignore", category=UndefinedMetricWarning)

'''
class NB:
    def __init__(self, company_name):
        self.data = []
        self.classifications = []
        # calculate data for 3 time periods and so we need 3 classifiers
        self.classifier = [None] * 3
        self.company_name = company_name

    def get_data(self):
        company_data = DataPrep(self.company_name).reports
        for report in company_data:
            self.data.append(report.text)
            self.classifications.append([report.one_day, report.three_day, report.five_day])



    def train(self):
        self.classifier = MultinomialNB.fit(self.data, self.classifications)

    def predict(self, data):
        self.classifier.predict(data)
'''
class NBCombined:
    def __init__(self, price_no_change_margin=.01):
        self.data = []
        self.dates = []
        self.num_classifiers = 3
        self.example_classifiers = [None] * 3

        self.price_no_change_margin = price_no_change_margin
        self.num_examples = 0
        # calculate data for 3 time periods and so we need 3 classifiers
        self.classifier = [None] * self.num_classifiers
        self.company_name = ['AAPL', 'MSFT', 'GOOG', 'SNDK', 'IBM', 'HPQ' ]

        self.predictions = []*self.num_classifiers
        self.actual = []*self.num_classifiers
        self.sort_data()

        self.k_fold_train(5)

    def get_data(self, company_name):
        company = DataPrep(company_name, self.price_no_change_margin)
        for report in company.reports:
            self.dates.append(report.date)
            self.data.append([report.text, report.one_day, report.three_day, report.five_day])


    def sort_data(self):
        for company in self.company_name:
            self.get_data(company)

        '''
        merge columns so we can sort them in sequential order
            Financial data tends to be time sensitive and as the author's in the attached paper noted,
            the market seems to be most sensitive to these reports in the short term
        '''
        temp = np.column_stack((np.array(self.dates), np.array(self.data)))

        temp = temp[temp[:, 0].argsort()]
        self.dates = temp.T[0]
        self.data = temp.T[1]
        self.example_classifiers[0] = temp.T[2]
        self.example_classifiers[1] = temp.T[3]
        self.example_classifiers[2] = temp.T[4]


        self.num_examples = np.shape(temp)[0]

    def train(self, staring_index, ending_index, classifier_index):

        print(np.shape(train_data))
        print(np.shape(train_classifier))

        train_set = np.column_stack((train_data, train_classifier))

        self.classifier[classifier_index] = NaiveBayesClassifier.train(train_set)

    def predict(self, staring_index, ending_index, classifier_index):
        print("h")

        test_data = self.data[staring_index:ending_index]
        test_classifier = self.example_classifiers[staring_index:ending_index]
        test_set = np.column_stack((test_data,test_classifier))

        self.classifier[classifier_index] = NaiveBayesClassifier.train(test_set)


    def k_fold_train(self, num_folds):
        #remainder = self.num_examples % num_folds
        num_vals = int(self.num_examples / num_folds)
        for i in range(self.num_classifiers):
            if i == 0:
                days = 1
            elif i == 1:
                days = 3
            else:
                days = 5
            print("=====================================================")
            print("Predicting net stock movement in: ", days, " days.")
            count_vect = CountVectorizer()
            train_data = self.data
            X_train_counts = count_vect.fit_transform(train_data)
            tfidf_transformer = TfidfTransformer()
            X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
            for index in range(num_folds-1):

                train_classifier = self.example_classifiers[i][i*num_vals:(i+1)*num_vals]
                clf = MultinomialNB(alpha=.000001).fit(X_train_tfidf[i*num_vals:(i+1)*num_vals], train_classifier)
                predicted = clf.predict(X_train_tfidf[(i+1)*num_vals: (i+2)*num_vals])

                print("Accuracy", np.mean(predicted == train_classifier))
                print(metrics.classification_report(train_classifier, predicted,
                target_names=["Sell","Hold","Buy"]))

                #self.train(i*num_vals, (i+1)*num_vals, i)
#                self.predict((i+1)*num_vals, (i+2)*num_vals, i)

test = NBCombined()