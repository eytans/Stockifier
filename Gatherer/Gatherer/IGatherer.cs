using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Gatherers
{
    using UpdateDataType = IDictionary<string, IDictionary<string, string>>;
    public class DataUpdatedArgs : EventArgs
    {
        private SortedDictionary<string, Dictionary<string, string>> result;

        public DataUpdatedArgs(UpdateDataType input) : this()
        {
            foreach (string key in input.Keys)
            {
                if (!Values.ContainsKey(key))
                {
                    Values.Add(key, new Dictionary<string, string>());
                }
                foreach (KeyValuePair<string, string> entry in input[key])
                {
                    Values[key].Add(entry.Key, entry.Value);
                }
            }
        }

        public DataUpdatedArgs()
        {
            Values = new Dictionary<string, IDictionary<string, string>>();
        }

        public UpdateDataType Values { get; }
    }

    public interface IGatherer
    {
        event EventHandler<DataUpdatedArgs> DataUpdated;
    }
}
