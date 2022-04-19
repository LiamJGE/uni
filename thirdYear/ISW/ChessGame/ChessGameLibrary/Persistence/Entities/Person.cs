using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ChessGameLibrary.BusinessLogic.Entities;

namespace ChessGameLibrary.Persistence.Entities
{
    public partial class Person
    {
        public String name
        {
            get;
            set;
        }

        public int age
        {
            get;
            set;
        }

        public virtual ICollection<ChessGame> chessGame
        {
            get;
            set;
        }
    }
}
