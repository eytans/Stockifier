using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Gatherers
{
    public class DataUpdatedArgs : EventArgs
    {
        public DataUpdatedArgs(IDictionary<string, string> input) : this()
        {
            foreach (KeyValuePair<string, string> entry in input)
            {
                Values.Add(entry.Key, entry.Value);
            }
        }

        public DataUpdatedArgs()
        {
            Values = new Dictionary<string, string>();
        }
        public Dictionary<string, string> Values { get; }
    }

    public interface IGatherer
    {
        event EventHandler<DataUpdatedArgs> DataUpdated;
    }
}
