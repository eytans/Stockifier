using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Gatherers
{
    public interface IGatherer
    {
        event EventHandler DataUpdated;
    }
}
