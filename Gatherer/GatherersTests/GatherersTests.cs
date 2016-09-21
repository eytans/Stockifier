using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Gatherer;
using System.Data.Entity;
using NLog;

namespace Gatherer.Tests
{
    [TestClass()]
    public class GatherersTests
    {
        public class Stock1
        {
            [System.ComponentModel.DataAnnotations.Key]
            public int id { get; set; }
            public string name { get; set; }
        }

        public class Stock2
        {
            [System.ComponentModel.DataAnnotations.Key]
            public int id { get; set; }
            public string name { get; set; }
        }

        public class TestContext1 : DbContext
        {
            public DbSet<Stock1> Daily { get; set; }
            public DbSet<Stock2> RT { get; set; }
        }

        public class TestContext2 : DbContext
        {
            public DbSet<Stock1> Daily { get; set; }
            public DbSet<Stock2> RT { get; set; }
        }

        [TestMethod()]
        public void WorkingWithSeveralContexts()
        {
            //Dictionary<string, DbContext> collection = new Dictionary<string, DbContext>();
            //TestContext1 apple = new TestContext1();
            //TestContext2 msft = new TestContext2();
            ////collection.Add("AAPL", apple);
            ////collection.Add("MSFT", msft);

            //Stock1 t = new Stock1();
            //t.id = 1;
            //t.name = "Apple_Daily1";
            //Stock1 a = new Stock1();
            //a.id = 2;
            //a.name = "Apple_Daily2";
            //Stock2 b = new Stock2();
            //b.id = 3;
            //b.name = "Apple_RT1";
            //Stock2 c = new Stock2();
            //c.id = 4;
            //c.name = "Apple_RT2";
            //Stock1 d = new Stock1();
            //d.id = 5;
            //d.name = "MS_Daily1";
            //Stock1 e = new Stock1();
            //e.id = 6;
            //e.name = "MS_Daily2";
            //Stock2 f = new Stock2();
            //f.id = 7;
            //f.name = "MS_RT1";
            //Stock2 g = new Stock2();
            //g.id = 8;
            //g.name = "MS_RT2";
            //Stock2 h = new Stock2();
            //h.id = 9;
            //h.name = "MS_RT3";

            //apple.Daily.Add(t);
            //apple.RT.Add(b);
            //msft.Daily.Add(d);
            //msft.RT.Add(f);

            //apple.SaveChanges();
            //msft.SaveChanges();
            //collection["MSFT"].Daily.Add(d);
            //collection["AAPL"].Daily.Add(t);
            //collection["MSFT"].RT.Add(f);
            //collection["AAPL"].RT.Add(b);
            //collection["AAPL"].Daily.Add(a);
            //collection["MSFT"].Daily.Add(e);
            //collection["AAPL"].RT.Add(c);
            //collection["MSFT"].RT.Add(g);
            //collection["MSFT"].RT.Add(h);

            //foreach (KeyValuePair<string, TestContext> entry in collection)
            //{
            //    entry.Value.SaveChanges();
            //}

            //using(var db = new TestContext())
            //{
            //    Testing t = new Testing();
            //    t.id = 1;
            //    t.name = "Eitan";
            //    db.Daily.Add(t);
            //    db.SaveChanges();
            //}


            //using(var aa = new TestContext())
            //{
            //    Testing d = new Testing();
            //    d.id = 2;
            //    d.name = "Dor";
            //    aa.Daily.Add(d);
            //    aa.SaveChanges();
            //}
        }
    }





    [TestClass()]
    abstract public class YahooGathererTests
    {
        protected static Logger logger = LogManager.GetCurrentClassLogger();

        protected IGatherer gatherer;
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

        [TestMethod(), Timeout(5000)]
        public void WebTest()
        {
            while (this.results.Count == 0)
            {
                System.Threading.Thread.Sleep(50);
            }
            YahooGathererTests.logger.Info(String.Join(",", results.First()));
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

    [TestClass()]
    public class YahooGathererDictEventArgs : YahooGathererTests
    {
        [TestInitialize()]
        override public void SetUp()
        {
            results = new List<string[]>();
            List<string> stockNames = new List<string>(new string[] { "AAPL", "MSFT", "GOOG" });
            gatherer = new YahooGathererDaily(300, stockNames);
            gatherer.DataUpdated += CheckDict;
        }

        [TestCleanup()]
        override public void TearDown()
        {
            gatherer.DataUpdated -= CheckDict;
            gatherer = null;
            results = null;
        }

        protected void CheckDict(object sender, DataUpdatedArgs args)
        {
            Assert.IsTrue(args.Values.Count > 0);
            foreach (var keyVal in args.Values)
                Console.WriteLine("Key = " + keyVal.Key + " Val = " + keyVal.Value);
            results.Add(new string[] { "What ever" });
        }
    }
}