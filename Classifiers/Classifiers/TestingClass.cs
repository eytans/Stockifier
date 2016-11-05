using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using Accord.MachineLearning.Boosting;
using Accord.MachineLearning.DecisionTrees;
using Accord.IO;
using Accord.MachineLearning.Bayes;
using System.Data;
using Accord.Statistics.Filters;
using Accord.MachineLearning.DecisionTrees.Learning;
using Accord.MachineLearning.Boosting.Learners;
using NLog;
using System.CodeDom.Compiler;

namespace Classifiers
{
    public class TestingClass
    {
        protected static Logger logger = LogManager.GetCurrentClassLogger();
        Boost<Weak<DecisionTree>> boosted;

        public TestingClass()
        {
            logger.Warn("Memory used is " + GC.GetTotalMemory(false).ToString());
            string dataPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory,
                "..", "..", "..", "Samples", "adult", "Dataset.data");
            //    "..", "..", "..", "Samples", "Accident & Health Insurance (Financial)", "AFL.csv");

            string[] names = {"age", "workclass", "fnlwgt", "education", "educational-num",
                "marital-status", "occupation", "relationship", "race", "gender",
                "capital-gain", "capital-loss", "hours-per-week", "native-country", "income"};
            int[] valuesRange = {Int32.MaxValue, 9, Int32.MaxValue, 17, Int32.MaxValue, 8,
                15, 7, 6, 3, Int32.MaxValue, Int32.MaxValue, 170, 41, 2};

            var csv = from line in File.ReadAllLines(dataPath)
                      select (line.Split(' ')).ToArray();

            ////string[] names = {"ticker", "date", "open", "high", "low",
            ////    "close", "volume", "ex-divider", "split-ratio", "adj-open", "adj-high",
            ////    "adj-low", "adj-close", "adj-volume"};
            ////for (int i = 0; i < tempTable.Columns.Count; i++)
            ////    tempTable.Columns[i].ColumnName = names[i];

            ////foreach (DataRow row in stringTable.Rows)
            ////    tempTable.ImportRow(row);

            //int[] numIndexes = {0, 2, 4, 10, 11, 12};


            IList<DecisionVariable> attributes = new List<DecisionVariable>();
            for (int i = 0; i < names.Count() - 1; i++)
                attributes.Add(DecisionVariable.Discrete(names[i], valuesRange[i]));

            //foreach (string name in names.ToList().GetRange(0, 2))
            //    attributes.Add(DecisionVariable.Discrete(name, 16));
            //foreach (string name in names.ToList().GetRange(2, names.Count() - 2))
            //    attributes.Add(DecisionVariable.Continuous(name));

            int[][] data = Utils.ToIntArray(csv.ToArray()).Take(500).ToArray();
            int[] outputs = data.Select(x => x.Last()).ToArray();

            double[][] inputs = data.Select(x => x.Take(14).ToArray()).ToArray().Select(x => x.Select(y => Convert.ToDouble(y)).ToArray()).ToArray();

            DecisionTree tree = new DecisionTree(attributes, 2);
            C45Learning learning = new C45Learning(tree);
            Weak<DecisionTree> weak = new Weak<DecisionTree>(tree, (t, vector) => t.Decide(vector));

            ModelConstructor<Weak<DecisionTree>> trainer = delegate (double[] weights)
            {
                learning.Learn(inputs, outputs, weights);
                return weak;
            };


            Boost<Weak<DecisionTree>> boosted = new Boost<Weak<DecisionTree>>();
            AdaBoost<Weak<DecisionTree>> booster = new AdaBoost<Weak<DecisionTree>>(boosted, trainer);
            logger.Warn("Memory available is " + GC.GetTotalMemory(false).ToString());
            booster.Run(inputs, outputs);
        }
        
    }
}
