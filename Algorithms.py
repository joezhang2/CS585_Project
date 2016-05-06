'''
This is the meat of the project. The processed data is processed more, where stop words are removed
by removing the most common words. This should provide a better fit than utilizing an existing
corpus of stop words as we can remove some technical words that appear in every report.

Once the data is processed, it is fed into Sklean's Multinomial Naive Bayes estimator. To better
 analyze the performance of this technique, a type of K-fold analysis is performed. As this data is
  time sensitive, the data is broken into K-sections. The n-th evaluation train with the n-th first
  seconds and we test with the n+1th part.
'''

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from DataPrep import DataPrep
import numpy as np
from sklearn import metrics


class NBCombined:
    def __init__(self, file_location, price_no_change_margin=.01 ):
        self.data = []
        self.dates = []
        # 3 is used as there are classifiers for a stocks movement after 1, 3, 5 days
        self.num_classifiers = 3
        self.example_classifiers = [None] * 3

        '''
        The user can specify how much a stocks price has to move before qualifying as a change
        This is a potential place for improvement. Ideally we would like to have a regression
        that gives a number a prediction instead of a class as we could profit even more. But
        that is also harder to predict.
        '''
        self.price_no_change_margin = price_no_change_margin
        self.num_examples = 0
        # calculate data for 3 time periods and so we need 3 classifiers
        self.classifier = [None] * self.num_classifiers
        self.company_name = ['AAPL', 'MSFT', 'GOOG', 'SNDK', 'IBM', 'HPQ' ]

        self.predictions = []*self.num_classifiers
        self.actual = []*self.num_classifiers
        self.sort_data(file_location)

        self.k_fold_train(4)

    '''
    Obtain the data from data structures and load them into our arrays for evaluation
    '''
    def get_data(self, company_name, file_location):
        company = DataPrep(company_name, file_location, self.price_no_change_margin)
        for report in company.reports:
            self.dates.append(report.date)
            self.data.append([report.text, report.one_day, report.three_day, report.five_day])

    '''
    Takes the data and sorts it based on the date of the report it makes no sense to predict data
    in the past with current data. We want to predict the future to profit
    '''
    def sort_data(self, file_location):
        for company in self.company_name:
            self.get_data(company, file_location)

        # merge columns so we can sort them in sequential order
        temp = np.column_stack((np.array(self.dates), np.array(self.data)))
        temp = temp[temp[:, 0].argsort()]

        # stored sorted data
        self.dates = temp.T[0]
        self.data = temp.T[1]
        self.example_classifiers[0] = temp.T[2]
        self.example_classifiers[1] = temp.T[3]
        self.example_classifiers[2] = temp.T[4]

        self.num_examples = np.shape(temp)[0]

    '''
    Performs the K-fold evaluation explained at the top
    '''
    def k_fold_train(self, num_folds):
        # Dividing and casting to an int will leave the potential of throwing away some pieces of data
        # A future update would utilize every piece of data
        #remainder = self.num_examples % num_folds
        num_vals = int(self.num_examples*1.0 / num_folds)

        # Evaluate performance for predicting each time period of 1,3,5 days
        for i in range(self.num_classifiers):
            if i == 0:
                days = 1
            elif i == 1:
                days = 3
            else:
                days = 5
            print("=====================================================")
            print("Predicting net stock movement in: ", days, " days.")

            # counts the frequency of each word
            count_vect = CountVectorizer()
            train_data = self.data
            # transform the data into a vector to use within the Naive Bayes Estimator
            X_train_counts = count_vect.fit_transform(train_data)
            tfidf_transformer = TfidfTransformer()
            X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

            # K-folds evaluation
            for index in range(num_folds-1):

                train_classifier = self.example_classifiers[index][index*num_vals:(index+1)*num_vals]
                '''
                Set an alpha value for Laplace smoothing. Naive bayes runs into issues with having 0
                of a vector/word as it assumes independence for each parameter and multiplies them
                together so a 0 value can mess things up
                '''
                clf = MultinomialNB(alpha=.0001).fit(X_train_tfidf[index*num_vals:(index+1)*num_vals], train_classifier)
                predicted = clf.predict(X_train_tfidf[(index+1)*num_vals: (index+2)*num_vals])

                print("Accuracy", np.mean(predicted == train_classifier))
                print(metrics.classification_report(train_classifier, predicted,
                target_names=["Sell","Hold","Buy"]))

year = str(input("Enter a number (2008, 2009 or 2010) and see the evaluation results."))

test = NBCombined(file_location=year)
