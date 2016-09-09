using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Gatherer
{
    public class Stock
    {
        [System.ComponentModel.DataAnnotations.Key]
        public string StockName { get; set; }
        public string Industry { get; set; }
        public string SubIndustry { get; set; }
        //room for more features 
        public List<DayData> Data { get; set; }
    }

    public class DayData
    {
        [System.ComponentModel.DataAnnotations.Key]
        public int DataId { get; set; }
        public int Date { get; set; } //Need to consider if to change to Date format for now it's YYYYMMDD
        public double Open { get; set; }
        public double High { get; set; }
        public double Low { get; set; }
        public double Close { get; set; }
        public int Volume { get; set; }
        public double OpenInt { get; set; }

        public string StockName { get; set; }
        public virtual Stock Stock { get; set; }
    }

    public class StockContext : DbContext
    {
        public DbSet<Stock> Stocks { get; set; }
        public DbSet<DayData> DayDatas { get; set; }

    }
}
