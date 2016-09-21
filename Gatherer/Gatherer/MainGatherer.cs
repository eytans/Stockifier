using NDesk.Options;
using NLog;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Gatherer
{
    class MainGatherer
    {
        protected static Logger logger = LogManager.GetCurrentClassLogger();

        private IList<StockContext> stocks;

        MainGatherer(IList<string> stocks)
        {
            logger.Info("Connecting to all stocks databases.");
            this.stocks = new List<StockContext>();
            foreach (string s in stocks)
            {
                logger.Debug("Connecting to " + s);
                try
                {
                    var temp = new StockContext(s);
                    this.stocks.Add(temp);
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

        public void Run()
        {
            string[] stockNames = stocks.Select((StockContext sc) => sc.StockName).ToArray();
            int dayInMilliseconds = 1000 * 60 * 60 * 24;
            int fiveMinutesInMilliseconds = 1000 * 5;
            logger.Info("Creating daily gatherer");
            YahooGathererDaily daily = new YahooGathererDaily(dayInMilliseconds, stockNames);
            logger.Info("Creating realtime gatherer which will sample every 5 minutes");
            YahooGathererRT rt = new YahooGathererRT(fiveMinutesInMilliseconds, stockNames);
            // TODO: add a function to DataUpdated event to read all data into database
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
            // TODO: dont return so data will be collected continuesly.
        }
    }
}
