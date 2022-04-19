using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ChessGameLibrary.BusinessLogic.Entities;

namespace ChessGameLibrary.Persistence.Entities
{
    public partial class Board
    {
        public virtual ChessGame game
        {
            get;
            set;
        }

        public virtual ICollection<Cell> cells
        {
            get;
            set;
        }
    }
}
