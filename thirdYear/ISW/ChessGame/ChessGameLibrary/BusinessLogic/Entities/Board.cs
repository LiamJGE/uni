using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ChessGameLibrary.BusinessLogic.Entities
{
    public partial class Board
    {
        public Board()
        {
            cells = new List<Cell>();
        }
    }
}
