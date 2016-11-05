using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Classifiers
{
    public static class ExtensionMethods
    {
        public static int[][] ToIntArray(this DataTable t)
        {
            int[][] results = new int[t.Rows.Count][];
            for(int i = 0; i < t.Rows.Count; i++)
                results[i] = new int[t.Columns.Count];

            for(int i = 0; i < t.Rows.Count; i++)
            {
                for(int j = 0; j < t.Columns.Count; j++)
                {
                    DataRow c = t.Rows[i];
                    object o = c.ItemArray[j];
                    if(o is int)
                    {
                        results[i][j] = (int) o;
                    }
                    else if (o is double)
                    {
                        results[i][j] = (int) Math.Round((double) o);
                    }
                    else
                    {
                        throw new ArgumentException("Cannot receive non int/double objects int input.");
                    }
                }
            }
            return results;
        }

        public static double[][] ToDoubleArray(this DataTable t)
        {
            double[][] results = new double[t.Rows.Count][];
            for (int i = 0; i < t.Rows.Count; i++)
                results[i] = new double[t.Columns.Count];

            for (int i = 0; i < t.Rows.Count; i++)
            {
                for (int j = 0; j < t.Columns.Count; j++)
                {
                    DataRow c = t.Rows[i];
                    object o = c.ItemArray[j];
                    if (o is int || o is double)
                    {
                        results[i][j] = (double) o;
                    }
                    else
                    {
                        throw new ArgumentException("Cannot receive non int/double objects int input.");
                    }
                }
            }
            return results;
        }
    }
}
