using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ChessGameLibrary.Persistence.Entities;

namespace ChessGameLibrary.BusinessLogic.Entities
{
    public partial class Cell
    {
        public Cell()
        {
            board = new Board();
            hasPiece = new Piece();
        }

        public Cell(int row, int column, String color):this()
        {
            this.row = row;
            this.column = column;
            this.color = color;
        }
    }
}
