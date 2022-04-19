using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ChessGameLibrary.Persistence.Entities
{
    public partial class ChessGame
    {
        public DateTime ellapsedTime
        {
            get;
            set;
        }

        public virtual Board board
        {
            get;
            set;
        }

        public virtual Person whitePlayer
        {
            get;
            set;
        }

        public virtual Person blackPlayer
        {
            get;
            set;
        }

        public virtual Person activePlayer
        {
            get;
            set;
        }



    }
}
