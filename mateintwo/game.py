from pathlib import Path
from yaml import dump
import chess
import chess.pgn
import chess.uci

from termcolor import colored
import ulib.pp as pp

BASE_DIR = Path('../data/chess/mates/')


def game_headers(game):
  hh = game.headers
  out_str = []
  out_str.append(colored(hh['White'], 'grey', 'on_white'))
  out_str.append(colored(hh['Black'], 'white', 'on_grey'))
  out_str = '\n'.join(out_str)
  return out_str


def pad_text(text, *, pads=[5, 5, 1, 1]):
  lines = text.split('\n')
  l, r, t, b = pads
  new_lines = ['\n' * t]
  for l_ in lines:
    ll = ' ' * l + l_ + ' ' * r
    new_lines.append(ll)
  new_lines.append('\n' * b)
  new_lines = '\n'.join(new_lines)
  return new_lines


def color_board(board):
  text = str(board)
  return text


def get_san_moves(board):
  moves = [board.san(m) for m in board.legal_moves]
  return moves


def make_square(p, c, b):
  return colored(' ' + p + ' ', c, 'on_' + b)


def pcol(p):
  if p.isupper():
    return 'red'
  else:
    return 'grey'


def show_board(fen):
  pos = fen.split(' ')[0]
  ranks = pos.split('/')
  out = []
  cols = ['cyan', 'blue']
  new_ranks = []
  for rank in ranks:
    r_ = ''
    for s in rank:
      if s.isdigit():
        r_ += ' ' * int(s)
      else:
        r_ += s
    new_ranks.append(r_)

  for i, rank in enumerate(new_ranks):
    out_r = []
    for j, s in enumerate(rank):
      out_r.append(make_square(s, pcol(s), cols[(j + i) % 2]))
    out.append(''.join(out_r))
  out = '\n'.join(out)

  out = pad_text(out)

  return out


def format_legal_moves(legal_moves):
  out = 'Legal Moves : \n\n'
  for i, l in enumerate(legal_moves):
    out += l + ', '
    if i % 5 == 0:
      out += '\n'
  return out


def parse_legal_moves(board):
  moves = {board.san(m): m for m in board.legal_moves}
  mdict = {k: [] for k in ['K', 'Q', 'R', 'B', 'N', 'P']}
  for m, M in moves.items():
    print(m, M)
    if len(m) >= 3:
      if m[0] in mdict:
        mdict[m[0]].append([m, M])
    if len(m) == 2:
      mdict['P'].append([m, M])
  print(mdict)


def format_engine_out(res, board, game):
  out = '\n' + game_headers(game) + '\n\n'
  out += 'Engine says : \n\n'
  out += colored('best   : ' + board.san(res.bestmove) + '\n\n', 'red')
  out += colored('ponder : ' + board.san(res.ponder) + '\n\n', 'blue')
  return out
