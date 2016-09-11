using Microsoft.VisualStudio.TestTools.UnitTesting;
using Gatherers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Gatherer;
using System.Data.Entity;

namespace Gatherers.Tests
{
    [TestClass()]
    public class GatherersTests
    {
        public class Testing
        {
            [System.ComponentModel.DataAnnotations.Key]
            public int id { get; set; }
            public Dictionary<string, int> dicty  { get; set; }
            public Testing()
            {
                dicty = new Dictionary<string, int>();
            }
        }

        public class TestContext : DbContext
        {
            public DbSet<Testing> Daily { get; set; }
        }

        [TestMethod()]
        public void WebTestNotRealTime()
        {
            using(var db = new TestContext())
            {
                Testing t = new Testing();
                t.id = 3;
                t.dicty.Add("key", 0);
                db.Daily.Add(t);
                db.SaveChanges();
            }
        }
    }

    [TestClass()]
    abstract public class YahooGathererTests
    {
        protected Gatherers.IGatherer gatherer;
        protected List<String[]> results;

        abstract public void SetUp();
        abstract public void TearDown();

        public void ReadyData(Func<int, ICollection<string>, IGatherer> creator)
        {
            List<string> stockNames = new List<string>(new string[] { "AAPL", "MSFT", "GOOG" });
            results = new List<string[]>();
            gatherer = creator(300, stockNames);
            gatherer.DataUpdated += Gatherer_DataUpdated;
        }
        
    
        public void RemoveData()
        {
            gatherer.DataUpdated -= Gatherer_DataUpdated;
            gatherer = null;
            results = null;
        }

        protected void Gatherer_DataUpdated(object sender, EventArgs e)
        {
            results.Add(((YahooGatherer)sender).CurrentData);
        }

        [TestMethod(), Timeout(60000)]
        public void WebTest()
        {
            while (this.results.Count == 0)
            {
                System.Threading.Thread.Sleep(50);
            }
            Console.WriteLine(String.Join(",", results.First()));
        }
    }

    [TestClass()]
    public class YahooGathererRTTests : YahooGathererTests
    {
        [TestInitialize()]
        override public void SetUp()
        {
            ReadyData((int i, ICollection<string> c) => new YahooGathererRT(i, c));
        }

        [TestCleanup()]
        override public void TearDown()
        {
            RemoveData();
        }
    }

    [TestClass()]
    public class YahooGathererDailyTests : YahooGathererTests
    {
        [TestInitialize()]
        override public void SetUp()
        {
            ReadyData((int i, ICollection<string> c) => new YahooGathererDaily(i, c));
        }

        [TestCleanup()]
        override public void TearDown()
        {
            RemoveData();
        }
    }
}