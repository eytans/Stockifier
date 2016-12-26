
from Utilities.orginizers import LearningData

ld = LearningData()
for sn in ld.get_stock_names():
    data = ld.get_stock_data(sn)
    trues = (data['change'] > 0).value_counts()[True]
    total = data.shape[0]
    print(sn, float(trues)/total)
