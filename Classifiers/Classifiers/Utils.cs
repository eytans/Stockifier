using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Classifiers
{
    public class Utils
    {
        public class Enumirefier
        {
            private IDictionary<string, int> enums;
            private IList<string> names;
            private int cur;

            public Enumirefier()
            {
                enums = new Dictionary<string, int>();
                names = new List<string>();
                cur = 0;
            }

            public int this[string key]
            {
                get
                {
                    if(!enums.ContainsKey(key))
                    {
                        enums[key] = cur;
                        cur += 1;
                    }
                    return enums[key];
                }
            }

            public string this[int key]
            {
                get
                {
                    return names[key];
                }
            }

            public int Count
            {
                get
                {
                    return names.Count;
                }
            }
        }

        static public int[][] ToIntArray(string[][] table)
        {
            Enumirefier[] enums = new Enumirefier[table[0].Count()];
            int[][] result = new int[table.Count()][];
            for(int i = 0; i < table[0].Count(); i++)
                enums[i] = new Enumirefier();

            for(int i = 0; i < table.Count(); i++)
            {
                result[i] = new int[table[0].Count()];

                string[] row = table[i];
                for(int j = 0; j < row.Count(); j++)
                {
                    string val = row[j];
                    int o;
                    if (val.Trim().Equals("?"))
                        o = 0;
                    else if (!Int32.TryParse(val, out o))
                        o = enums[j][val];

                    result[i][j] = o;
                }
            }

            return result;
        }
    }
}
