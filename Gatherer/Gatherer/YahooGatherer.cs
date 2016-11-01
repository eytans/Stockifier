using CsvHelper;
using NLog;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Timers;


namespace Gatherer
{
    public abstract class YahooGatherer : IGatherer
    {
        protected static Logger logger = LogManager.GetCurrentClassLogger();

        private ICollection<string> stocks;
        private Timer timer;

        protected abstract IList<string> GetModifiers();

        private DataUpdatedArgs data = new DataUpdatedArgs(new SortedDictionary<string, IDictionary<string, string>>());
        public string[] CurrentData { get
            {
                var temp = data.Values;
                return temp.Values
                    .Select((IDictionary<string, string> data) => data.Values.ToList())
                    .SelectMany(x => x).ToArray();
            }
        }

        public event EventHandler<DataUpdatedArgs> DataUpdated;

        public YahooGatherer(int updatePeriod, IEnumerable<string> enumerable, params string[] args)
        {
            this.timer = new Timer(updatePeriod);

            logger.Info("Creating a new YahooGatherer");

            stocks = new List<string>();
            if (enumerable != null)
                foreach (string s in enumerable)
                    stocks.Add(s);

            foreach (string s in args)
                stocks.Add(s);

            logger.Info("Gatherers stocks are: " + stocks.Aggregate((string start, string next) => start + " " + next));

            timer.Elapsed += UpdateStocksData;
            timer.Start();
        }

        public YahooGatherer(IEnumerable<string> enumerable, params string[] args) : this(100, enumerable, args) { }

        public YahooGatherer(params string[] args) : this(null, args) { }

        protected void Clear()
        {
            this.DataUpdated = null;
        }

        private DataUpdatedArgs GetFromYahoo()
        {
            logger.Debug("Getting data from yahoo");

            string baseUrl = "http://download.finance.yahoo.com/d/?s={0}&f={1}&e=.csv";
            // TODO: probably change ToString to GetName or Name
            string stockNames = stocks.Skip(1).Aggregate(stocks.First().ToString().Replace(" ", string.Empty), (s1, s2) => s1 + "," + s2.ToString().Replace(" ", string.Empty));
            IList<string> modifiers = GetModifiers();
            string dataFields = modifiers.Aggregate("", (s, modifier) => s + modifier);
            string url = String.Format(baseUrl, stockNames, dataFields);

            logger.Debug("url is: " + url);

            using (WebResponse response = WebRequest.Create(url).GetResponse())
            using (StreamReader reader = new StreamReader(response.GetResponseStream()))
            {
                DateTime now = DateTime.Now;
                CsvParser csv = new CsvParser(reader);
                csv.Configuration.HasHeaderRecord = true;
                IDictionary<string, IDictionary<string, string>> result = (IDictionary<string, IDictionary<string, string>>) 
                    new SortedDictionary<string, IDictionary<string, string>>();
                foreach(string stockName in stocks)
                {
                    string[] row = csv.Read();
                    if (row == null) continue;
                    if (!result.ContainsKey(stockName))
                    {
                        result.Add(stockName, new Dictionary<string, string>());
                    }

                    for (int i = 0; i < modifiers.Count; i++)
                    {
                        result[stockName].Add(modifiers.ElementAt(i), row[i]);
                    }
                    result[stockName].Add("Time", now.Ticks.ToString());
                }
                logger.Debug("Done receiving data from csv.");
                return new DataUpdatedArgs(result);
            }
        }

        private void UpdateStocksData(object sender, ElapsedEventArgs args)
        {
            try
            {
                // TODO: make this better
                logger.Info("Getting new data from yahoo.");
                data = GetFromYahoo();
                DataUpdated(this, data);
                logger.Info("Done updating data.");
            }
            catch (Exception e)
            {
                logger.Error(e, "Caught exception while updating data. " + e.Message);
                logger.Debug(e.StackTrace);
            }
        }

        protected static IList<string> EnumsToString<T>() where T : struct, IConvertible
        {
            if (!typeof(T).IsEnum)
            {
                throw new ArgumentException("T must be an enumerated type");
            }
            return Enum.GetValues(typeof(T))
                            .Cast<T>()
                            .Select((T dm) => dm.ToString())
                            .ToList<string>();
        }

    }
}
