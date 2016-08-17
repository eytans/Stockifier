using System;
using System.IO;
using System.Data.Entity;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace stockDB
{
    class Program
    { 
        static public void LoadDB()
        {
            using (var db = new StockContext())
            {
                //C:\Users\sdshw\Desktop\Stockfier\stockifier\stockDB\stockDB\bin\Debug\
                string workingDir = AppDomain.CurrentDomain.BaseDirectory;
                DirectoryInfo baseDir = new DirectoryInfo(@"..\..\..\..");
                DirectoryInfo dataDir = baseDir.GetDirectories(@"resources\Datenbank\data")[0];
                string[] dirs = Directory.GetDirectories(dataDir.FullName);
                Console.WriteLine(dataDir.Name);
                List<string> stocksNames = new List<string>();
                foreach (string line in dirs.OrderBy(f => Guid.NewGuid()).Distinct().Take(12))
                {
                    stocksNames.Add((new DirectoryInfo(line)).Name);
                }
                foreach (string name in stocksNames)
                {
                    Stock newStock = new Stock
                    {
                        StockName = name,
                        Industry = "NA",
                        SubIndustry = "NA",
                        Data = new List<DayData>()
                    };
                    string path = (dataDir.FullName + name + "\\" + name + ".txt");
                    string[] data = System.IO.File.ReadAllLines(path);
                    foreach (string line in data.Skip(1))
                    {
                        string[] elements = line.Split(',');
                        DayData tmp = new DayData
                        {
                            Date = int.Parse(elements[0]),
                            Open = double.Parse(elements[1]),
                            High = double.Parse(elements[2]),
                            Low = double.Parse(elements[3]),
                            Close = double.Parse(elements[4]),
                            Volume = int.Parse(elements[5]),
                            OpenInt = double.Parse(elements[6]),
                            StockName = name
                        };
                        newStock.Data.Add(tmp);
                        //using (var db = new StockContext())
                        //{
                        //    db.DayDatas.Add(tmp);
                        //}
                    }
                    db.Stocks.Add(newStock);

                }
                db.SaveChanges();
                System.Console.ReadKey();
            }
        }

        static public void clearTables()
        {
            using (var db = new StockContext())
            {
                foreach (Stock tmp in db.Stocks)
                {
                    db.Stocks.Remove(tmp);
                }
                foreach (DayData tmp in db.DayDatas)
                {
                    db.DayDatas.Remove(tmp);
                }
                db.SaveChanges();
            }
        } 
        //C:\Datenbank\data\AAOI
        static void Main(string[] args)
        {
            //clearTables();
            LoadDB();
            //using (var db = new StockContext())
            //{
            //    Stock st = db.Stocks.FirstOrDefault();
            //    Console.WriteLine(st.Data.Count);
            //}
            //string workingDir = AppDomain.CurrentDomain.BaseDirectory;
            //Console.WriteLine(workingDir);
            Console.ReadLine();
        }
    }
    

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
