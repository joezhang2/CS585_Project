'''
This serves as the main data structure for this project. Each object contains the date of a K-8 report,
the text of the report, 3 classifiers with 3 possible classes each.

The stocks movement over the course of one, three and five days is recorded. Each report can lead
to a stocks price going up, holding at the current price or going down.
'''

class Report:
    def __init__(self, date, text, price_no_change_margin=.01, current_opening=0, first_day_close=0, three_day_close=0, five_day_close=0):
        self.date = date
        self.text = text
        self.price_no_change_margin = price_no_change_margin
        '''
        Classes for a report to indicate status of a stock after the report.
        Classes can be 2 for increase, 1 for no change and 0 for a decrease in price.
        The margin what is considered no change in price can be user-specified, the default is 1%
        '''
        self.one_day = None
        self.three_day = None
        self.five_day = None

        self.current_opening = current_opening
        self.first_day_close = first_day_close
        self.three_day_close = three_day_close
        self.five_day_close = five_day_close

        self.calculate_classifiers()

    def calculate_classifiers(self):
        self.one_day = self.percent_change(self.first_day_close)
        self.three_day = self.percent_change(self.three_day_close)
        self.five_day = self.percent_change(self.five_day_close)

    '''
    Helper method to calculate the class that the data goes into.
    '''
    def percent_change(self, x):
        percentage = (x-self.current_opening)/self.current_opening
        if percentage > self.price_no_change_margin:
            return 2
        elif percentage < -self.price_no_change_margin:
            return 0
        else:
            return 1


