using NDesk.Options;
using NLog;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Gatherer
{
    class MainGatherer
    {
        protected static Logger logger = LogManager.GetCurrentClassLogger();
        public static ManualResetEvent waitOn = new ManualResetEvent(false);
        private IDictionary<string, StockContext> stocks;

        MainGatherer(ICollection<string> stocks)
        {
            logger.Info("Connecting to all stocks databases.");
            this.stocks = new Dictionary<string, StockContext>();
            foreach (string s in stocks)
            {
                logger.Debug("Connecting to " + s);
                try
                {
                    var temp = new StockContext(s);
                    this.stocks.Add(s, temp);
                }
                catch(Exception e)
                {
                    logger.Warn(e, "Failed to connect to " + s +"'s database. skipping.");
                }
            }
                
            if(this.stocks.Count == 0)
            {
                throw new Exception("Bad environment or args. No stock contexts created.");
            }
            
        }

        private void AddToDb<T>(object sender, DataUpdatedArgs args, Func<IDictionary<string, string>, T> creator)
        {
            var stocksValues = args.Values;
            foreach (var stockAnsiToValues in stocksValues)
            {
                T stock = creator(stockAnsiToValues.Value);
                // TODO: @Dor I need an add function for StockContext with overload for both stock types.
                this.stocks[stockAnsiToValues.Key].Add(stock);
            }
        }

        private void AddRTToDB(object sender, DataUpdatedArgs args)
        {
            AddToDb<StockRT>(sender, args, (IDictionary<string, string> data) => new StockRT(data));
        }

        private void AddDailyToDB(object sender, DataUpdatedArgs args)
        {
            AddToDb<StockDaily>(sender, args, (IDictionary<string, string> data) => new StockDaily(data));
        }

        public void Run()
        {
            string[] stockNames = stocks.Keys.ToArray();
            int dayInMilliseconds = 1000 * 60 * 60 * 24;
            int fiveMinutesInMilliseconds = 1000 * 5;
            logger.Info("Creating daily gatherer");
            YahooGathererDaily daily = new YahooGathererDaily(dayInMilliseconds, stockNames);
            logger.Info("Creating realtime gatherer which will sample every 5 minutes");
            YahooGathererRT rt = new YahooGathererRT(fiveMinutesInMilliseconds, stockNames);
            rt.DataUpdated += AddRTToDB;
            daily.DataUpdated += AddDailyToDB;
        }

        public static void Main(string[] args)
        {
            List<string> stockNames = new List<string>();
            OptionSet p = new OptionSet()
                .Add("s|stock", delegate (string v) { stockNames.Add(v); } );
            var extra = p.Parse(args);

            if(stockNames.Count == 0)
            {
                Console.WriteLine("need stock params");
                return;
            }

            MainGatherer gatherer = new MainGatherer(stockNames);
            waitOn.WaitOne();
        }
    }
}
