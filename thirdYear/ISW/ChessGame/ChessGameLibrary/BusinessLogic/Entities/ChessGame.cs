using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ChessGameLibrary.BusinessLogic.Entities
{
    public partial class ChessGame
    {
        public ChessGame()
        {
            board = new Board();
            whitePlayer = new Player();
            blackPLayer = new Player();
            activePlayer = new Player();
        }

        public ChessGame(DateTime ellapsedTime):this()
        {
            ellapsedTime = ellapsedTime;
        }
    }
}
