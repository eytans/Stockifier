import sklearn.ensemble
from sklearn.model_selection import cross_val_score


def get_general_classifier(data, classes):
    return cross_val_score(sklearn.ensemble.AdaBoostClassifier(), data, classes)
