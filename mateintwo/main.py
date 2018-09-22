from pathlib import Path
import pandas as pd

import chess
import chess.pgn
import chess.uci

from mateintwo.boards import Boards

BASE_DIR = Path('.')

if __name__ == '__main__':

  df = pd.read_pickle(str(BASE_DIR / 'mate_in_two.pkl'))

  engine = chess.uci.popen_engine("/usr/local/bin/stockfish")

  now = 0

  board = Boards(df[now]['game'], engine)
  while not board.quit:

    board.app.run()

    now += 1
    next_game = df[now]['game']

    board.reset(next_game)
    board.app.reset()
