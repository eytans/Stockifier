using CsvHelper;
using NLog;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace Gatherer
{
    public class YahooGathererHistory
    {
        protected static Logger logger = LogManager.GetCurrentClassLogger();

        private string stock;
        private DateTime from;
        private DateTime to;
        public List<string[]> data = new List<string[]>();

        public YahooGathererHistory(DateTime from, DateTime to, string stock)
        {
            this.stock = stock;
            this.from = from;
            this.to = to;
            try
            {
                logger.Info("Collecting history data from yahoo between " + from.ToString() + " to " + to.ToString() + ".");
                GetFromYahoo();
            }
            finally
            {
                logger.Info("Got " + data.Count.ToString() + " days of data.");
            }
        }

        // Warning: this is copy pase from YahooGatherer but only for one run
        private void GetFromYahoo()
        {
            string baseUrl = @"http://ichart.finance.yahoo.com/table.csv?s={0}&a={1:00}&b={2}&c={3}&d={4:00}&e={5}&f={6}&g=d&ignore=.csv";
            string url = String.Format(baseUrl, stock, from.Month, from.Day, from.Year, to.Month, to.Day, to.Year);
            using ( WebResponse response = WebRequest.Create(url).GetResponse())
            using (StreamReader reader = new StreamReader(response.GetResponseStream()))
            {
                CsvParser csv = new CsvParser(reader);
                csv.Configuration.HasHeaderRecord = true;
                string[] row = csv.Read();
                while(true)
                {
                    if (row == null)
                        break;
                    data.Add(row);
                    row = csv.Read();
                }
            }
        }

    }
}
