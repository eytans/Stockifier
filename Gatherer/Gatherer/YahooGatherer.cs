using CsvHelper;
using Gatherers;
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
        private ICollection<string> stocks;
        private Timer timer;

        protected abstract ICollection<string> GetModifiers();

        private string[] data;
        public string[] CurrentData { get { return data; } }


        public event EventHandler DataUpdated;

        public YahooGatherer(int updatePeriod, IEnumerable<string> enumerable, params string[] args)
        {
            this.timer = new Timer(updatePeriod);

            stocks = new List<string>();
            if (enumerable != null)
                foreach (string s in enumerable)
                    stocks.Add(s);

            foreach (string s in args)
                stocks.Add(s);

            timer.Elapsed += UpdateStocksData;
            timer.Start();
        }

        public YahooGatherer(IEnumerable<string> enumerable, params string[] args) : this(100, enumerable, args) { }

        public YahooGatherer(params string[] args) : this(null, args) { }

        protected void Clear()
        {
            this.DataUpdated = null;
        }

        private string[] GetFromYahoo()
        {
            
            string baseUrl = "http://finance.yahoo.com/d/quotes.csv?s={0}&f={1}";
            // TODO: probably change ToString to GetName or Name
            string stockNames = stocks.Skip(1).Aggregate(stocks.First().ToString(), (s1, s2) => s1 + "+" + s2.ToString());
            string dataFields = GetModifiers().Aggregate("", (s, modifier) => s + modifier);
            string url = String.Format(baseUrl, stockNames, dataFields);
            using (WebResponse response = WebRequest.Create(url).GetResponse())
            using (StreamReader reader = new StreamReader(response.GetResponseStream()))
            {
                CsvParser csv = new CsvParser(reader);
                csv.Configuration.HasHeaderRecord = true;
                return csv.Read();
            }
        }

        private void UpdateStocksData(object sender, ElapsedEventArgs args)
        {
            // TODO: add logs
            try
            {
                // TODO: make this better
                data = GetFromYahoo();
                DataUpdated(this, EventArgs.Empty);
            }
            catch (Exception e)
            {
                Console.WriteLine("Causht exception: " + e.Message + ". at:");
                Console.WriteLine(e.StackTrace);
            }
        }

        protected static ICollection<string> EnumsToString<T>() where T : struct, IConvertible
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
