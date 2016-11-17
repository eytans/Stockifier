using Microsoft.VisualStudio.TestTools.UnitTesting;
using Gatherer;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Gatherer.Tests
{
    [TestClass()]
    public class YahooGathererHistoryTests
    {
        [TestMethod()]
        public void YahooGathererHistoryTest()
        {
            YahooGathererHistory history = new YahooGathererHistory(DateTime.Now.AddDays(-2000), DateTime.Now.AddDays(-1970), "AAPL");
            foreach(string[] row in history.data)
            {
                Console.WriteLine(String.Join(",", row));
            }
        }
    }
}