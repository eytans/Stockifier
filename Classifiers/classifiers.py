import sklearn.ensemble
from sklearn.model_selection import cross_val_score


def get_general_classifier(data, classes):
    return sklearn.ensemble.AdaBoostClassifier().fit(data, classes)
