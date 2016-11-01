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

namespace Classifiers
{
    public class TestingClass
    {
        public TestingClass()
        {
            string dataPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "..", "..", "Samples", "Accident & Health Insurance (Financial)", "AFL.csv");
            CsvReader reader = new CsvReader(dataPath, false);
            var stringTable = reader.ToTable();
            var table = stringTable.Clone();
            for(int i = 2; i < table.Columns.Count; i++)
                table.Columns[i].DataType = typeof(double);

            foreach (DataRow row in stringTable.Rows)
                table.ImportRow(row);

            stringTable.Dispose();

            DecisionTree t = new DecisionTree(null, 2);
            AdaBoost<NaiveBayes> booster;
        }
        
    }
}
