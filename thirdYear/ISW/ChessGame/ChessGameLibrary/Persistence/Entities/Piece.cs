using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ChessGameLibrary.Persistence.Entities
{
    public abstract partial class Piece
    {
        public Color color
        {
            get;
            set;
        }

        public virtual Cell locatedAt
        {
            get;
            set;
        }
    }
}
