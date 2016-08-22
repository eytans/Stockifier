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
        private Gatherers.IGatherer gatherer;
        private List<String[]> results;

        [TestInitialize()]
        public void SetUp()
        {
            results = new List<string[]>();
            gatherer = new YahooGatherer(300, new System.Collections.Generic.LinkedList<string>(), "AAPL", "MSFT", "GOOG");
            gatherer.DataUpdated += Gatherer_DataUpdated;
        }

        [TestCleanup()]
        public void TearDown()
        {
            gatherer.DataUpdated -= Gatherer_DataUpdated;
            gatherer = null;
            results = null;
        }

        private void Gatherer_DataUpdated(object sender, EventArgs e)
        {
            results.Add(((YahooGatherer)sender).CurrentData);
        }

        [TestMethod(),Timeout(10000)]
        public void WebTest()
        {
            while(this.results.Count == 0)
            {
                System.Threading.Thread.Sleep(50);
            }
            Console.WriteLine(results.First().ToString());
        }
    }
}