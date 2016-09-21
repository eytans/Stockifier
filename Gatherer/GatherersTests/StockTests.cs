using Microsoft.VisualStudio.TestTools.UnitTesting;
using Gatherer;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using NLog;

namespace Gatherer.Tests
{
    [TestClass()]
    public class StockTests
    {
        protected static Logger logger = LogManager.GetCurrentClassLogger();

        static readonly string dictionaryRTString = @"Key = b2 Val = N / A
Key = b3 Val = N / A
Key = c6 Val = N / A
Key = g5 Val = N / A
Key = g6 Val = N / A
Key = i5 Val = N / A
Key = j3 Val = N / A
Key = k1 Val = N / A
Key = k2 Val = N / A
Key = m2 Val = N / A
Key = r2 Val = N / A
Key = v7 Val = N / A
Key = w4 Val = N / A";

        static readonly string dictionaryDailyString = @"Key = a Val = 114.95
Key = a2 Val = 33819200
Key = a5 Val = 900
Key = b Val = 114.92
Key = b4 Val = 23.46
Key = b6 Val = 400
Key = c Val = -0.65 - -0.56 %
Key = c1 Val = -0.65
Key = c3 Val = N / A
Key = d Val = 2.28
Key = d1 Val = 9 / 16 / 2016
Key = d2 Val = N / A
Key = e Val = 8.58
Key = e7 Val = 8.26
Key = e8 Val = 8.93
Key = e9 Val = 3.14
Key = f6 Val = 5369475000
Key = g Val = 114.04
Key = g1 Val = N / A
Key = g3 Val = N / A
Key = g4 Val = N / A
Key = h Val = 116.13
Key = i Val = N / A
Key = j Val = 89.47
Key = j1 Val = 619.24B
Key = j4 Val = 73.96B
Key = j5 Val = 25.45
Key = j6 Val = +28.45 %
Key = k Val = 123.82
Key = k3 Val = 9315382
Key = k4 Val = -8.90
Key = k5 Val = -7.19 %
Key = l Val = 4:00pm - <b>114.92</b>
Key = l1 Val = 114.92
Key = l2 Val = N / A
Key = l3 Val = N / A
Key = m Val = 114.04 - 116.13
Key = m3 Val = 106.77
Key = m4 Val = 101.83
Key = m5 Val = 13.09
Key = m6 Val = +12.86 %
Key = m7 Val = 8.15
Key = m8 Val = +7.63 %
Key = n Val = Apple Inc.
Key = n4 Val = N / A
Key = o Val = 115.17
Key = p Val = 115.57
Key = p1 Val = N / A
Key = p2 Val = -0.56 %
Key = p5 Val = 2.83
Key = p6 Val = 4.93
Key = q Val = 8 / 4 / 2016
Key = r Val = 13.40
Key = r1 Val = 8 / 11 / 2016
Key = r5 Val = 1.78
Key = r6 Val = 13.91
Key = r7 Val = 12.87
Key = s Val = AAPL
Key = s1 Val = N / A
Key = s7 Val = 1.51
Key = t1 Val = 4:00pm
Key = t6 Val = N / A
Key = t7 Val = N / A
Key = t8 Val = 125.46
Key = v Val = 79886911
Key = v1 Val = N / A
Key = w Val = 89.47 - 123.82
Key = w1 Val = N / A
Key = x Val = NMS
Key = y Val = 2.04";

        private string[] Split(string source, string sep)
        {
            return source.Split(new string[] { sep }, StringSplitOptions.None);
        }

        IDictionary<string, string> singleData;

        public void SetUp(string dictionaryString)
        {
            singleData = new Dictionary<string, string>();
            foreach(string l in Split(dictionaryString, Environment.NewLine))
            {
                string k = Split(l, "= ")[1];
                k = Split(k, " Val")[0];
                string v = Split(l, "Val = ")[1];
                singleData.Add(k, v);
            }
        }

        [TestMethod()]
        public void StockRTTest()
        {
            SetUp(dictionaryRTString);
            StockRT appleRt = new StockRT(singleData);
            StockRT msRt = new StockRT(singleData);
            using (var db = new StockTabelsContext())
            {
                db.RT.Add(appleRt);
                db.RT.Add(msRt);
                db.SaveChanges();
            }
        }

        [TestMethod()]
        public void StockDailyTest()
        {
            SetUp(dictionaryDailyString);
            StockDaily appleDaily = new StockDaily(singleData);
            StockDaily msDaily = new StockDaily(singleData);
            using (var db = new StockTabelsContext())
            {
                db.Daily.Add(appleDaily);
                db.Daily.Add(msDaily);
                db.SaveChanges();
            }
        }
    }
}