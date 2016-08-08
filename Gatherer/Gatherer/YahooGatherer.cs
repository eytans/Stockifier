using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Net;
using System.Timers;
using Microsoft.VisualBasic.FileIO;
using Stock = System.String;

namespace Gatherers
{

    public class YahooGatherer : IGatherer
    {
        private ICollection<Stock> stocks;
        private Timer timer;

        private string[] data;
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

        private string[] GetFromYahoo(params DataModifiers[] args)
        {
            string baseUrl = "http://finance.yahoo.com/d/quotes.csv?s={0}&f={1}";
            // TODO: probably change ToString to GetName or Name
            string stockNames = stocks.Aggregate("", (s1, s2) => s1 + "+" + s2.ToString());
            string dataFields = args.Aggregate("", (s, modifier) => s + modifier.ToString());
            string url = String.Format(baseUrl, stockNames, dataFields);
            using (WebResponse response = WebRequest.Create(url).GetResponse())
            using (StreamReader reader = new StreamReader(response.GetResponseStream()))
            using (TextFieldParser parser = new TextFieldParser(reader))
            {
                List<string> results = new List<string>();
                parser.Delimiters = new[] { "," };
                parser.HasFieldsEnclosedInQuotes = true;
                return parser.ReadFields();
            }
        }

        private void UpdateStocksData(object sender, ElapsedEventArgs args)
        {
            // TODO: add logs
            try
            {
                // TODO: make this better
                data = GetFromYahoo(new DataModifiers[]{DataModifiers.b2, DataModifiers.b3});
                DataUpdated(this, EventArgs.Empty);
            }
            catch (Exception e)
            {
                // TODO: log error   
            }
        }


        public enum DataModifiers
        {
            [Description("ask")]
            b2,

            [Description("bid")]
            b3,

            [Description("change")]
            c6,

            [Description("holdings gain percent")]
            g5,

            [Description("holdings gain")]
            g6,

            [Description("order book")]
            i5,

            [Description("market cap")]
            j3,

            [Description("last trade")]
            k1,

            [Description("change percent")]
            k2,

            [Description("day's range")]
            m2,

            [Description("p/e ratio")]
            r2,

            [Description("holdings value")]
            v7,

            [Description("day's value change")]
            w4
        }
    }
}
