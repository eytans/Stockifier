from Classifiers.classifiers import ConnectionStrengthClassifier
from Utilities.clustering import StrengthCalc
from Utilities.orginizers import TrainingData, LearningData
import sklearn
import datetime
import pandas
import shelve
import logging
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import numpy
logging.getLogger().setLevel(logging.ERROR)


# we are dropping kyth as it doesn exist anymore
def run_on_dates(start_date, model, stocks=('SHW', 'MNK', 'BIO', 'KRO'), is_sc=False, is_tree=False):
    ld = LearningData()
    if is_sc:
        sc = StrengthCalc()
    for s in stocks:
        td = TrainingData(s, ld=ld).set_threshold(0.8).add_history(10)
        data, classes = td.get()
        if is_tree:
            best_cut = 22
            data, classes = pandas.get_dummies(data.apply(lambda s: pandas.qcut(s.rank(method='first'), best_cut))), classes

        traind = data.loc[data.index < start_date]
        trainc = classes.iloc[-traind.shape[0]:]
        testd = td.slice_by_date(data, startdate=start_date, enddate=None)
        testd = testd.iloc[:-1]
        true_change = ld.get_future_change_classification(testd, s, 1)
        if is_sc:
            stock_strengths = sc.get_strength_stock(s, 5, 325, 2, 0.1)
            from Utilities import clean_market_name


            all_cols = set(traind.columns)

            cur_cols = []
            cur_strengths = []
            for m in ld.get_market_names():
                cur_cols.append(list(filter(lambda c: clean_market_name(m) in c, all_cols)))
                cur_strengths.append(stock_strengths[m])

        if is_sc:
            model.fit(traind, trainc, strengths=cur_strengths, connection_columns=cur_cols)
        else:
            model.fit(traind, trainc)
        predicted = model.predict(testd)
        start = 100
        for p, c in zip(predicted, true_change):
            if p:
                print(p, c)
                start *= (1+c)
        print(s, start, testd.shape[0], sum(predicted))


if __name__ == '__main__':
    # penalty = 'l2'
    # intercept_scaling = 1.5
    # C = 4
    kernel = 'sigmoid'
    gamma = 0.001626
    # base = LogisticRegression(C=C, penalty=penalty, intercept_scaling=intercept_scaling, n_jobs=-1, class_weight={False: 1, True: 3})
    base = SVC(kernel=kernel, gamma=gamma)
    from sklearn.ensemble import BaggingClassifier

    model = ConnectionStrengthClassifier(base_estimator=base, threshold=0.15, base_strength=0.1, combined_weight=0.9)
    start_date = datetime.datetime(2016, 10, 28)
    run_on_dates(start_date=start_date, model=model, is_sc=True, is_tree=False)