using CsvHelper;
using NLog;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Timers;

namespace Gatherer
{
    public class YahooGathererDaily : YahooGatherer
    {
        static YahooGathererDaily()
        {
            logger.Info("Yahoo daily gatherers modifiers are: ");
            foreach(string s in EnumsToString<DataModifiers>())
            {
                logger.Info(s);
            }
        }

        public YahooGathererDaily(int updatePeriod, ICollection<string> stockNames) : base(updatePeriod, stockNames)
        {

        }

        protected override IList<string> GetModifiers()
        {
            return EnumsToString<DataModifiers>();
        }

        public enum DataModifiers
        {
            [Description("ask")]
            a,

            [Description("average daily volume")]
            a2,

            [Description("ask size")]
            a5,

            [Description("bid")]
            b,

            [Description("book value")]
            b4,

            [Description("bid size")]
            b6,

            [Description("change & precent change")]
            c,

            [Description("change")]
            c1,

            [Description("commission")]
            c3,

            [Description("divident/share")]
            d,

            [Description("last trade date")]
            d1,

            [Description("trade date")]
            d2,

            [Description("ernings/share")]
            e,

            [Description("eps estimtae current year")]
            e7,

            [Description("eps estimtate next year")]
            e8,

            [Description("eps estimtate next quearter")]
            e9,

            [Description("float shres")]
            f6,

            [Description("day's low")]
            g,

            [Description("day's high")]
            h,

            [Description("52-week low")]
            j,

            [Description("52-week high")]
            k,

            [Description("holdings gain percent")]
            g1,

            [Description("annualized gain")]
            g3,

            [Description("holdings gain")]
            g4,

            [Description("more info")]
            i,

            [Description("market capitalization")]
            j1,

            [Description("ebitda")]
            j4,

            [Description("change from 52-week low")]
            j5,

            [Description("percent change from 52-week low")]
            j6,

            [Description("last trade size")]
            k3,

            [Description("change from 52-week high")]
            k4,

            [Description("precent change from 52-week high")]
            k5,

            [Description("last trade with time")]
            l,

            [Description("last trade (price only)")]
            l1,

            [Description("high limit")]
            l2,

            [Description("low limit")]
            l3,

            [Description("day's range")]
            m,

            [Description("50-day moving average")]
            m3,

            [Description("200-day moving average")]
            m4,

            [Description("change from 200-day moving average")]
            m5,

            [Description("percent change from 200-day moving average")]
            m6,

            [Description("change from 50-day moving average")]
            m7,

            [Description("percent change from 50-day moving average")]
            m8,

            [Description("name")]
            n,

            [Description("notes")]
            n4,

            [Description("open")]
            o,

            [Description("previous close")]
            p,

            [Description("price paid")]
            p1,

            [Description("change in percent")]
            p2,

            [Description("price/sales")]
            p5,

            [Description("price/book")]
            p6,

            [Description("ex-divident date")]
            q,

            [Description("p/e ratio")]
            r,

            [Description("dividend pay date")]
            r1,

            [Description("peg ratio")]
            r5,

            [Description("price/eps estimate current year")]
            r6,

            [Description("price/eps estimate next year")]
            r7,

            [Description("symbol")]
            s,

            [Description("shres owned")]
            s1,

            [Description("short ratio")]
            s7,

            [Description("last trade time")]
            t1,

            [Description("trade links")]
            t6,

            [Description("ticker trend")]
            t7,

            [Description("1 yr target price")]
            t8,

            [Description("volume")]
            v,

            [Description("holdings value")]
            v1,

            [Description("52-week range")]
            w,

            [Description("day's value change")]
            w1,

            [Description("stock exchange")]
            x,

            [Description("dividend yield")]
            y,

        }
    }
}
