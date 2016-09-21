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

        static readonly string dictionaryAppleRTString = @"Key = b2 Val = N/A
Key = b3 Val = N/A
Key = c6 Val = N/A
Key = g5 Val = N/A
Key = g6 Val = N/A
Key = i5 Val = N/A
Key = j3 Val = N/A
Key = k1 Val = N/A
Key = k2 Val = N/A
Key = m2 Val = N/A
Key = r2 Val = N/A
Key = s Val = AAPL
Key = v7 Val = N/A
Key = w4 Val = N/A
Key = n Val = Apple Inc.
Key = Time Val = 636100940967799020";
        static readonly string dictionaryGoogleRTString = @"Key = b2 Val = N/A
Key = b3 Val = N/A
Key = c6 Val = N/A
Key = g5 Val = N/A
Key = g6 Val = N/A
Key = i5 Val = N/A
Key = j3 Val = N/A
Key = k1 Val = N/A
Key = k2 Val = N/A
Key = m2 Val = N/A
Key = r2 Val = N/A
Key = s Val = GOOG
Key = v7 Val = N/A
Key = w4 Val = N/A
Key = n Val = Alphabet Inc.
Key = Time Val = 636100940967799020";
        static readonly string dictionaryMicrosoftRTString = @"Key = b2 Val = N/A
Key = b3 Val = N/A
Key = c6 Val = N/A
Key = g5 Val = N/A
Key = g6 Val = N/A
Key = i5 Val = N/A
Key = j3 Val = N/A
Key = k1 Val = N/A
Key = k2 Val = N/A
Key = m2 Val = N/A
Key = r2 Val = N/A
Key = s Val = MSFT
Key = v7 Val = N/A
Key = w4 Val = N/A
Key = n Val = Microsoft Corporation
Key = Time Val = 636100940967799020";

        static readonly string dictionaryAppleDailyString = @"Key = a Val = 113.53
Key = a2 Val = 36539400
Key = a5 Val = 400
Key = b Val = 113.52
Key = b4 Val = 23.46
Key = b6 Val = 700
Key = c Val = -0.05 - -0.04%
Key = c1 Val = -0.05
Key = c3 Val = N/A
Key = d Val = 2.28
Key = d1 Val = 9/21/2016
Key = d2 Val = N/A
Key = e Val = 8.58
Key = e7 Val = 8.26
Key = e8 Val = 8.94
Key = e9 Val = 3.15
Key = f6 Val = 5369475000
Key = g Val = 112.44
Key = h Val = 113.99
Key = j Val = 89.47
Key = k Val = 123.82
Key = g1 Val = N/A
Key = g3 Val = N/A
Key = g4 Val = N/A
Key = i Val = N/A
Key = j1 Val = 611.70B
Key = j4 Val = 73.96B
Key = j5 Val = 24.05
Key = j6 Val = +26.88%
Key = k3 Val = 100
Key = k4 Val = -10.30
Key = k5 Val = -8.32%
Key = l Val = 3:17pm - <b>113.52</b>
Key = l1 Val = 113.52
Key = l2 Val = N/A
Key = l3 Val = N/A
Key = m Val = 112.44 - 113.99
Key = m3 Val = 108.35
Key = m4 Val = 102.31
Key = m5 Val = 11.21
Key = m6 Val = +10.95%
Key = m7 Val = 5.17
Key = m8 Val = +4.77%
Key = n Val = Apple Inc.
Key = n4 Val = N/A
Key = o Val = 113.82
Key = p Val = 113.57
Key = p1 Val = N/A
Key = p2 Val = -0.04%
Key = p5 Val = 2.78
Key = p6 Val = 4.84
Key = q Val = 8/4/2016
Key = r Val = 13.24
Key = r1 Val = 8/11/2016
Key = r5 Val = 1.76
Key = r6 Val = 13.74
Key = r7 Val = 12.70
Key = s Val = AAPL
Key = s1 Val = N/A
Key = s7 Val = 1.72
Key = t1 Val = 3:17pm
Key = t6 Val = N/A
Key = t7 Val = N/A
Key = t8 Val = 124.91
Key = v Val = 27316943
Key = v1 Val = N/A
Key = w Val = 89.47 - 123.82
Key = w1 Val = N/A
Key = x Val = NMS
Key = y Val = 1.98
Key = Time Val = 636100939241159081";
        static readonly string dictionaryGoogleDailyString = @"Key = a Val = 776.36
Key = a2 Val = 1417020
Key = a5 Val = 200
Key = b Val = 776.11
Key = b4 Val = 186.20
Key = b6 Val = 200
Key = c Val = +4.84 - +0.63%
Key = c1 Val = +4.84
Key = c3 Val = N/A
Key = d Val = N/A
Key = d1 Val = 9/21/2016
Key = d2 Val = N/A
Key = e Val = 25.81
Key = e7 Val = 34.29
Key = e8 Val = 40.66
Key = e9 Val = 9.66
Key = f6 Val = 591660000
Key = g Val = 768.30
Key = h Val = 776.40
Key = j Val = 589.38
Key = k Val = 789.87
Key = g1 Val = N/A
Key = g3 Val = N/A
Key = g4 Val = N/A
Key = i Val = N/A
Key = j1 Val = 533.50B
Key = j4 Val = 26.90B
Key = j5 Val = 186.87
Key = j6 Val = +31.71%
Key = k3 Val = 100
Key = k4 Val = -13.62
Key = k5 Val = -1.72%
Key = l Val = 3:16pm - <b>776.25</b>
Key = l1 Val = 776.25
Key = l2 Val = N/A
Key = l3 Val = N/A
Key = m Val = 768.30 - 776.40
Key = m3 Val = 773.57
Key = m4 Val = 735.28
Key = m5 Val = 40.97
Key = m6 Val = +5.57%
Key = m7 Val = 2.68
Key = m8 Val = +0.35%
Key = n Val = Alphabet Inc.
Key = n4 Val = N/A
Key = o Val = 772.66
Key = p Val = 771.41
Key = p1 Val = N/A
Key = p2 Val = +0.63%
Key = p5 Val = 6.48
Key = p6 Val = 4.14
Key = q Val = N/A
Key = r Val = 30.08
Key = r1 Val = N/A
Key = r5 Val = 1.24
Key = r6 Val = 22.64
Key = r7 Val = 19.09
Key = s Val = GOOG
Key = s1 Val = N/A
Key = s7 Val = 1.62
Key = t1 Val = 3:16pm
Key = t6 Val = N/A
Key = t7 Val = N/A
Key = t8 Val = 921.08
Key = v Val = 848568
Key = v1 Val = N/A
Key = w Val = 589.38 - 789.87
Key = w1 Val = N/A
Key = x Val = NMS
Key = y Val = N/A";
        static readonly string dictionaryMicrosoftDailyString = @"Key = Time Val = 636100939241159081
Key = a Val = 57.6700
Key = a2 Val = 28361400
Key = a5 Val = 5100
Key = b Val = 57.6600
Key = b4 Val = 9.2210
Key = b6 Val = 4100
Key = c Val = +0.8592 - +1.5124%
Key = c1 Val = +0.8592
Key = c3 Val = N/A
Key = d Val = 1.4400
Key = d1 Val = 9/21/2016
Key = d2 Val = N/A
Key = e Val = 2.1000
Key = e7 Val = 2.9000
Key = e8 Val = 3.2200
Key = e9 Val = 0.7900
Key = f6 Val = 7264105000
Key = g Val = 57.0800
Key = h Val = 57.6750
Key = j Val = 43.0500
Key = k Val = 58.7000
Key = g1 Val = N/A
Key = g3 Val = N/A
Key = g4 Val = N/A
Key = i Val = N/A
Key = j1 Val = 449.39B
Key = j4 Val = 27.17B
Key = j5 Val = 14.6192
Key = j6 Val = +33.9587%
Key = k3 Val = 1195
Key = k4 Val = -1.0308
Key = k5 Val = -1.7560%
Key = l Val = 3:17pm - <b>57.6692</b>
Key = l1 Val = 57.6692
Key = l2 Val = N/A
Key = l3 Val = N/A
Key = m Val = 57.0800 - 57.6750
Key = m3 Val = 57.5174
Key = m4 Val = 53.9276
Key = m5 Val = 3.7416
Key = m6 Val = +6.9382%
Key = m7 Val = 0.1518
Key = m8 Val = +0.2639%
Key = n Val = Microsoft Corporation
Key = n4 Val = N/A
Key = o Val = 57.5100
Key = p Val = 56.8100
Key = p1 Val = N/A
Key = p2 Val = +1.5124%
Key = p5 Val = 5.1886
Key = p6 Val = 6.1609
Key = q Val = 8/16/2016
Key = r Val = 27.4615
Key = r1 Val = 9/8/2016
Key = r5 Val = 2.3000
Key = r6 Val = 19.8859
Key = r7 Val = 17.9097
Key = s Val = MSFT
Key = s1 Val = N/A
Key = s7 Val = 2.1900
Key = t1 Val = 3:17pm
Key = t6 Val = N/A
Key = t7 Val = N/A
Key = t8 Val = 59.8700
Key = v Val = 25042156
Key = v1 Val = N/A
Key = w Val = 43.0500 - 58.7000
Key = w1 Val = N/A
Key = x Val = NMS
Key = y Val = 2.5200
Key = Time Val = 636100939241159081";



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
                string k = Split(l, " = ")[1];
                k = Split(k, " Val")[0];
                string v = Split(l, "Val = ")[1];
                singleData.Add(k, v);
            }
        }

        [TestMethod()]
        public void StockRTTest()
        {
            logger.Info("started RT test");
            SetUp(dictionaryAppleRTString);
            StockRT appleRt = new StockRT(singleData);
            SetUp(dictionaryMicrosoftRTString);
            StockRT msRt = new StockRT(singleData);
            using (var db = new StockTabelsContext())
            {
                db.Database.Delete();
                db.SaveChanges();
                db.RT.Add(appleRt);
                db.RT.Add(msRt);
                db.SaveChanges();
            }
        }

        [TestMethod()]
        public void StockDailyTest()
        {
            SetUp(dictionaryAppleDailyString);
            StockDaily appleDaily = new StockDaily(singleData);
            SetUp(dictionaryMicrosoftDailyString);
            StockDaily msDaily = new StockDaily(singleData);
            using (var db = new StockTabelsContext())
            {
                db.Database.Delete();
                db.SaveChanges();
                db.Daily.Add(appleDaily);
                db.Daily.Add(msDaily);
                db.SaveChanges();
            }
        }
    }
}