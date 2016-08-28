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
using Stock = System.String;

namespace Gatherer
{
    public abstract class YahooGatherer : IGatherer
    {
        private ICollection<Stock> stocks;
        private Timer timer;

        protected abstract ICollection<string> GetModifiers();

        private string[] data;
        public string[] history_data;
        public string[] CurrentData { get { return data; } }


        public event EventHandler DataUpdated;

        public YahooGatherer(int updatePeriod, IEnumerable<Stock> enumerable, params Stock[] args)
        {
            this.timer = new Timer(updatePeriod);

            stocks = new List<Stock>();
            if (enumerable != null)
                foreach (Stock s in enumerable)
                    stocks.Add(s);

            foreach (Stock s in args)
                stocks.Add(s);

            timer.Elapsed += UpdateStocksData;
            timer.Start();
        }

        public YahooGatherer(IEnumerable<Stock> enumerable, params Stock[] args) : this(100, enumerable, args) { }

        public YahooGatherer(params Stock[] args) : this(null, args) { }

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

    }
}
