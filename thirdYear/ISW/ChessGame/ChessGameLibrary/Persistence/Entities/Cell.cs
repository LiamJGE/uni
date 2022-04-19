using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ChessGameLibrary.Persistence.Entities
{
    public partial class Cell
    {
        public int row
        {
            get;
            set;
        }

        public int column
        {
            get;
            set;
        }

        public String color
        {
            get;
            set;
        }

        public virtual Piece hasPiece
        {
            get;
            set;
        }
    }
}
