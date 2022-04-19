using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ChessGameLibrary.BusinessLogic.Entities
{
    public abstract partial class Piece
    {
        public Piece(Colors color)
        {
            this.color = color;
            isLocated = null;
        }

        public Piece(String color):this()
        {
            color = color;
        }

        public abstract void draw();
    }
}
