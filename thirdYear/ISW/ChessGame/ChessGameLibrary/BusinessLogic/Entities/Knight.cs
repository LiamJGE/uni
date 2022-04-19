using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ChessGameLibrary.BusinessLogic.Entities
{
    public partial class Knight:Piece
    {

        public Knight(Colors color) : base(color)
        {

        }
        public override void draw()
        {
            throw new NotImplementedException();
        }
    }
}
