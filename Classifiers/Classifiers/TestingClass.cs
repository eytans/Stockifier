using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Accord.MachineLearning.Boosting;
using Accord.MachineLearning.DecisionTrees;
using Accord.MachineLearning.Bayes;

namespace Classifiers
{
    public class TestingClass
    {
        DecisionTree t = new DecisionTree(null, 2);
        AdaBoost<NaiveBayes> booster;
    }
}
