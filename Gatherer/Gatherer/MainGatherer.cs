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
                    logger.Error(e, "Failed to connect to " + s +"'s database. skipping.");
                }
            }
                
            if(this.stocks.Count == 0)
            {
                throw new Exception("Bad environment or args. No stock contexts created.");
            }
            
        }

        public void Run()
        {

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
        }
    }
}
