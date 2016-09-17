using NLog;
using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Gatherer
{
    public abstract class StockBase
    {
        protected static Logger logger = LogManager.GetCurrentClassLogger();

        public StockBase(IDictionary<string, string> data)
        {
            foreach (var prop in this.GetType().GetProperties())
            {
                if (prop.Name == "Time") continue;
                    
                try
                {
                    prop.SetValue(this, data[prop.Name]);
                }
                catch(Exception e)
                {
                    logger.Error(e, "Failed to set property " + prop.Name);
                    throw e;
                }
            }
        }
    }

    public class StockDaily : StockBase
    {
        public StockDaily(IDictionary<string, string> data) : base(data) { }

        [System.ComponentModel.DataAnnotations.Key]
        public string Time { get; set; }
        public string a { get; set; }
        public string a2 { get; set; }
        public string a5 { get; set; }
        public string b { get; set; }
        public string b4 { get; set; }
        public string b6 { get; set; }
        public string c { get; set; }
        public string c1 { get; set; }
        public string c3 { get; set; }
        public string d { get; set; }
        public string d1 { get; set; }
        public string d2 { get; set; }
        public string e { get; set; }
        public string e7 { get; set; }
        public string e8 { get; set; }
        public string e9 { get; set; }
        public string f6 { get; set; }
        public string g { get; set; }
        public string h { get; set; }
        public string j { get; set; }
        public string k { get; set; }
        public string g1 { get; set; }
        public string g3 { get; set; }
        public string g4 { get; set; }
        public string i { get; set; }
        public string j1 { get; set; }
        public string j4 { get; set; }
        public string j5 { get; set; }
        public string j6 { get; set; }
        public string k3 { get; set; }
        public string k4 { get; set; }
        public string k5 { get; set; }
        public string l { get; set; }
        public string l1 { get; set; }
        public string l2 { get; set; }
        public string l3 { get; set; }
        public string m { get; set; }
        public string m3 { get; set; }
        public string m4 { get; set; }
        public string m5 { get; set; }
        public string m6 { get; set; }
        public string m7 { get; set; }
        public string m8 { get; set; }
        public string n { get; set; }
        public string n4 { get; set; }
        public string o { get; set; }
        public string p { get; set; }
        public string p1 { get; set; }
        public string p2 { get; set; }
        public string p5 { get; set; }
        public string p6 { get; set; }
        public string q { get; set; }
        public string r { get; set; }
        public string r1 { get; set; }
        public string r5 { get; set; }
        public string r6 { get; set; }
        public string r7 { get; set; }
        public string s { get; set; }
        public string s1 { get; set; }
        public string s7 { get; set; }
        public string t1 { get; set; }
        public string t6 { get; set; }
        public string t7 { get; set; }
        public string t8 { get; set; }
        public string v { get; set; }
        public string v1 { get; set; }
        public string w { get; set; }
        public string w1 { get; set; }
        public string x { get; set; }
        public string y { get; set; }
    }

    public class StockRT : StockBase
    {
        public StockRT(IDictionary<string, string> data) : base(data) { }

        [System.ComponentModel.DataAnnotations.Key]
        public string Time { get; set; }
        public string b2 { get; set; }
        public string b3 { get; set; }
        public string c6 { get; set; }
        public string g5 { get; set; }
        public string g6 { get; set; }
        public string i5 { get; set; }
        public string j3 { get; set; }
        public string k1 { get; set; }
        public string k2 { get; set; }
        public string m2 { get; set; }
        public string r2 { get; set; }
        public string v7 { get; set; }
        public string w4 { get; set; }
    }
    public class StockHistory
    {
        [System.ComponentModel.DataAnnotations.Key]
        public string StockName { get; set; }
        public string Industry { get; set; }
        public string SubIndustry { get; set; }
        //room for more features 
        //public List<DayData> Data { get; set; }
    }
    public class StockTabelsContext : DbContext
    {
         public DbSet<StockDaily> Daily { get; set; }
         public DbSet<StockRT> RT { get; set; }
         //public DbSet<StockHistory> History { get; set; }
    }

    public class StockContext
    {
        public string StockName;
        //TODO: Add more fields for more features;
        public StockTabelsContext Tables { get; set; }
        public StockContext(string StockName) { this.StockName = StockName; }
    }
}

//public class StockGeneralData
//{
//    [System.ComponentModel.DataAnnotations.Key]
//    public int DataId { get; set; }
//    public int Date { get; set; } //Need to consider if to change to Date format for now it's YYYYMMDD
//    public double Open { get; set; }
//    public double High { get; set; }
//    public double Low { get; set; }
//    public double Close { get; set; }
//    public int Volume { get; set; }
//    public double OpenInt { get; set; }

//    public string StockName { get; set; }
//    //public virtual Stock Stock { get; set; }
//}