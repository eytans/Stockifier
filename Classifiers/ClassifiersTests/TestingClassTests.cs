using Microsoft.VisualStudio.TestTools.UnitTesting;
using Classifiers;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Classifiers.Tests
{
    [TestClass()]
    public class TestingClassTests
    {
        [TestMethod()]
        public void TestingClassTest()
        {
            TestingClass tc = new TestingClass();
            Assert.IsTrue(true);
        }
    }
}