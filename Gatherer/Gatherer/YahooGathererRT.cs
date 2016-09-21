using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Net;
using System.Timers;
using CsvHelper;

namespace Gatherer
{
    public class YahooGathererRT : YahooGatherer
    {
        static YahooGathererRT()
        {
            logger.Info("Yahoo RT gatherers modifiers are: ");
            foreach (string s in EnumsToString<DataModifiers>())
            {
                logger.Info(s);
            }
        }

        public YahooGathererRT(int updatePeriod, IEnumerable<string> enumerable, params string[] args) : base(updatePeriod, enumerable, args)
        {
        }

        protected override IList<string> GetModifiers()
        {
            return EnumsToString<DataModifiers>();
        }

        public enum DataModifiers
        {
            [Description("ask")]
            b2,

            [Description("bid")]
            b3,

            [Description("change")]
            c6,

            [Description("holdings gain percent")]
            g5,

            [Description("holdings gain")]
            g6,

            [Description("order book")]
            i5,

            [Description("market cap")]
            j3,

            [Description("last trade")]
            k1,

            [Description("change percent")]
            k2,

            [Description("day's range")]
            m2,

            [Description("p/e ratio")]
            r2,

            [Description("symbol")]
            s,

            [Description("holdings value")]
            v7,

            [Description("day's value change")]
            w4,

           [Description("name")]
           n
        }
    }  
}
