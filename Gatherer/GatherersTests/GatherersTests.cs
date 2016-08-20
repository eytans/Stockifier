using Microsoft.VisualStudio.TestTools.UnitTesting;
using Gatherers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Gatherers.Tests
{
    [TestClass()]
    public class GatherersTests
    {
        [TestMethod()]
        public void WebTest() {
            YahooGatherer yg = new YahooGatherer("AAPL", "MSFT", "GOOG");
            yg.SingleUpdateStocksData();
            Console.WriteLine(yg.history_data.ToString());

        }
    }
}