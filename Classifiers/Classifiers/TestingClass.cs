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

namespace Classifiers
{
    public class TestingClass
    {
        public TestingClass()
        {
            string dataPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory,
                "..", "..", "..", "Samples", "adult", "Dataset.data");
            //    "..", "..", "..", "Samples", "Accident & Health Insurance (Financial)", "AFL.csv");
            CsvReader reader = new CsvReader(dataPath, false);
            var stringTable = reader.ToTable();
            System.Data.DataTable tempTable = stringTable.Clone();

            //tempTable.Columns[0].DataType = typeof(int);
            //tempTable.Columns[1].DataType = typeof(int);
            //for (int i = 2; i < tempTable.Columns.Count; i++)
            //    tempTable.Columns[i].DataType = typeof(double);

            //string[] names = {"ticker", "date", "open", "high", "low",
            //    "close", "volume", "ex-divider", "split-ratio", "adj-open", "adj-high",
            //    "adj-low", "adj-close", "adj-volume"};
            //for (int i = 0; i < tempTable.Columns.Count; i++)
            //    tempTable.Columns[i].ColumnName = names[i];

            //foreach (DataRow row in stringTable.Rows)
            //    tempTable.ImportRow(row);

            //var filter = new Codification(tempTable, "ticker", "date");
            //var table = filter.Apply(tempTable);

            for (int i = 0; i < tempTable.Columns.Count; i++)
                tempTable.Columns[i].DataType = typeof(int);


            string[] names = {"age", "workclass", "fnlwgt", "education", "educational-num",
                "marital-status", "occupation", "relationship", "race", "gender",
                "capital-gain", "capital-loss", "hours-per-week", "native-country", "income"};
            int[] valuesRange = {Int32.MaxValue, 8, Int32.MaxValue, 16, Int32.MaxValue, 7,
                14, 6, 5, 2, Int32.MaxValue, Int32.MaxValue, 169, 40, 2};

            for (int i = 0; i < tempTable.Columns.Count; i++)
                tempTable.Columns[i].ColumnName = names[i];

            foreach (DataRow row in stringTable.Rows)
                tempTable.ImportRow(row);

            stringTable.Dispose();
            tempTable.Dispose();

            var filter = new Codification(tempTable, "age", "workclass", "fnlwgt", "education", "educational-num",
                "marital-status", "occupation", "relationship", "race", "gender",
                "capital-gain", "capital-loss", "hours-per-week", "native-country", "income");
            var table = filter.Apply(tempTable, "age", "workclass", "fnlwgt", "education", "educational-num",
                "marital-status", "occupation", "relationship", "race", "gender",
                "capital-gain", "capital-loss", "hours-per-week", "native-country", "income");

            IList<DecisionVariable> attributes = new List<DecisionVariable>();
            for(int i = 0; i < names.Count() - 1; i++)
                attributes.Add(DecisionVariable.Discrete(names[i], valuesRange[i]));

            //foreach (string name in names.ToList().GetRange(0, 2))
            //    attributes.Add(DecisionVariable.Discrete(name, 16));
            //foreach (string name in names.ToList().GetRange(2, names.Count() - 2))
            //    attributes.Add(DecisionVariable.Continuous(name));

            DataTable outputs = table.Clone();
            for (int i = 0; i < outputs.Columns.Count; i++)
                outputs.Columns.RemoveAt(i);

            DataTable inputs = table.Clone();
            inputs.Columns.RemoveAt(14);

            inputs.Rows.Cast<DataRow>().Select(r => r.ItemArray).ToArray();

            DecisionTree t = new DecisionTree(attributes, 2);
            ID3Learning id3learning = new ID3Learning(t);
            id3learning.Run(inputs., 
                outputs);
            id3learning.Save("out.tree");

            //AdaBoost<NaiveBayes> booster;
        }
        
    }
}
