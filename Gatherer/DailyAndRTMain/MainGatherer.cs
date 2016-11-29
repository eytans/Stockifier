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

        enum StockType { RT, Daily}

        private void AddToDb<T>(object sender, DataUpdatedArgs args, StockType st) where T : StockBase
        {
            logger.Info("Adding to DB with stocktype=" + st.ToString());
            var stocksValues = args.Values;
            foreach (var stockAnsiToValues in stocksValues)
            {
                if (st == StockType.RT)
                {
                    StockRT stock = new StockRT(stockAnsiToValues.Value);
                    logger.Debug("Adding stock with type RT with stockname=" + stockAnsiToValues.Key);
                    this.stocks[stockAnsiToValues.Key].Tables.RT.Add(stock);
                }
                else if (st == StockType.Daily)
                {
                    StockDaily stock = new StockDaily(stockAnsiToValues.Value);
                    logger.Debug("Adding stock with type Daily with stockname=" + stockAnsiToValues.Key);
                    this.stocks[stockAnsiToValues.Key].Tables.Daily.Add(stock);
                }
                else {
                    logger.Error("Unknown stock type while trying to enter data to DB");
                    throw new Exception("Unknown stock type");
                }
                this.stocks[stockAnsiToValues.Key].Tables.SaveChanges();
            }
        }

        private void AddRTToDB(object sender, DataUpdatedArgs args)
        {
            AddToDb<StockRT>(sender, args, StockType.RT);
        }

        private void AddDailyToDB(object sender, DataUpdatedArgs args)
        {
            AddToDb<StockDaily>(sender, args, StockType.Daily);
        }

        public void Run(int rtInterval=-1, int dailyInterval=-1)
        {
            if (rtInterval == -1)
                rtInterval = 5000;
            if (dailyInterval == -1)
                dailyInterval = (1000 * 60 * 60 * 24);
            string[] stockNames = stocks.Keys.ToArray();
            logger.Info("Creating daily gatherer");
            YahooGathererDaily daily = new YahooGathererDaily(dailyInterval, stockNames);
            logger.Info("Creating realtime gatherer which will sample every 5 minutes");
            YahooGathererRT rt = new YahooGathererRT(rtInterval, stockNames);
            rt.DataUpdated += AddRTToDB;
            daily.DataUpdated += AddDailyToDB;
        }

        public static void Main(string[] args)
        {
            List<string> stockNames = new List<string>();
            int rtInterval = -1;
            int dailyInterval = -1;
            OptionSet p = new OptionSet() {
                { "s|stock=", v => stockNames.Add(v) },
                { "r|rt-interval=", "Interval for realtime sampeling", v => rtInterval = Int32.Parse(v)},
                { "d|daily-interval=", "Interval for daily sampeling", v => dailyInterval = Int32.Parse(v)}, };
        var extra = p.Parse(args);

            if(stockNames.Count == 0)
            {
                Console.WriteLine("need stock params");
                return;
            }

            MainGatherer gatherer = new MainGatherer(stockNames);
            gatherer.Run(rtInterval=rtInterval, dailyInterval=dailyInterval);
            waitOn.WaitOne();
        }
    }
}
