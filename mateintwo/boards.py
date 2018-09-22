from __future__ import unicode_literals

import chess
import chess.pgn
import chess.uci
from pathlib import Path

from prompt_toolkit import ANSI
from prompt_toolkit.application.current import get_app
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.filters import has_focus
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.containers import Window, FloatContainer, Float
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import Frame, TextArea

from .completer import CustomCompleter
from .game import show_board, \
     parse_legal_moves, \
     format_legal_moves, \
     get_san_moves, \
     format_engine_out

BASE_DIR = Path('.')


class Boards:
  def __init__(self, first_game, engine):

    self.completer = CustomCompleter(['start'])
    self.elements = {
        'board':
        Window(
            FormattedTextControl(ANSI(show_board(chess.STARTING_BOARD_FEN))),
            width=35,
            height=13),
        'input':
        TextArea(
            height=1,
            prompt='>>> ',
            style='class:input-field',
            width=80,
            completer=self.completer),
        'p1':
        Window(
            FormattedTextControl(ANSI('Games')),
            width=31,
            height=13,
            wrap_lines=True),
        'p2':
        Window(
            FormattedTextControl(ANSI('Legal Moves')),
            width=31,
            height=13,
            wrap_lines=True),
    }

    self.frames = {}
    self.frames['board'] = Float(
        Frame(self.elements['board'], style='bg:#2e2e2e #ffffff'), top=10)
    self.frames['input'] = Float(
        Frame(self.elements['input'], style='bg:#2e2e2e #ffffff'), top=30)
    self.frames['p1'] = Float(
        Frame(self.elements['p1'], style='bg:#1e1e1e #ffffff'),
        top=10,
        left=10)
    self.frames['p2'] = Float(
        Frame(self.elements['p2'], style='bg:#1e1e1e #ffffff'),
        top=10,
        right=10)

    self.body = FloatContainer(
        content=Window(FormattedTextControl('')),
        floats=[v for k, v in self.frames.items()])
    self.kb = KeyBindings()

    self.app = Application(
        layout=Layout(self.body, focused_element=self.elements['input']),
        key_bindings=self.kb,
        full_screen=True)
    self.set_kb()

    self.game = first_game
    self.board = first_game.board()
    self.moves = list(first_game.main_line())
    self.engine = engine

    self.state = 'init'
    self.now = 0
    self.N = len(self.moves)
    self.chain = []
    self.selected = None
    self.quit = False

  def reset(self, game):
    if self.quit:
      pass
    else:
      self.__init__(game, self.engine)

  def set_text(self, item, text):
    self.elements[item].content = FormattedTextControl(text=ANSI(text))

  def add_text(self, item, text):
    self.elements[item].content = FormattedTextControl(text=ANSI(text))

  def make_moves(self, selection):
    legal_moves = get_san_moves(self.board)
    if selection in legal_moves:
      self.board.push_san(selection)
    self.set_text('board', show_board(self.board.fen()))
    legal_moves = get_san_moves(self.board)
    self.completer.words = legal_moves
    self.set_text('p2', format_legal_moves(legal_moves))
    self.engine.position(self.board)
    res = self.engine.go(movetime=1000)
    self.set_text('p1', format_engine_out(res, self.board, self.game))

  def next_move(self, selection):
    move = self.moves[self.now]
    self.now += 1
    if self.now == self.N - 1:
      self.now == 0
    self.board.push(move)
    self.set_text('board', show_board(self.board.fen()))
    legal_moves = get_san_moves(self.board)
    self.completer.words = legal_moves
    self.set_text('p2', format_legal_moves(legal_moves))
    self.engine.position(self.board)
    res = self.engine.go(movetime=1000)
    self.set_text('p1', format_engine_out(res, self.board, self.game))

  def start_game(self):
    self.now = 0
    self.set_text('board', show_board(self.board.fen()))
    legal_moves = get_san_moves(self.board)
    self.completer.words = legal_moves
    self.set_text('p2', format_legal_moves(legal_moves))
    self.engine.position(self.board)
    res = self.engine.go(movetime=1000)
    self.set_text('p1', format_engine_out(res, self.board, self.game))

  def set_kb(self):
    @self.kb.add('c-d')
    def _(event):
      " Pressing Ctrl-D will exit the user interface. "
      event.app.exit()

    @self.kb.add('c-q')
    def _(event):
      " Pressing Ctrl-Q will exit the user interface. "
      self.quit = True
      event.app.exit()

    @self.kb.add('enter', filter=has_focus(self.elements['input']))
    def _(event):
      try:
        selection = self.elements['input'].text
        if selection == 'start':
          self.start_game()
        else:
          self.make_moves(selection)
      except BaseException as e:
        self.set_text('board', str(e))

      self.elements['input'].text = ''


if __name__ == '__main__':

  cfile = 'polgar.pgn'
  PGN = open(str(BASE_DIR / cfile), encoding="latin-1")
  first_game = chess.pgn.read_game(PGN)

  engine = chess.uci.popen_engine("/usr/local/bin/stockfish")

  board = Boards(first_game, engine)
  while not board.quit:

    next_game = chess.pgn.read_game(PGN)

    board.app.run()
    board.reset(next_game)
    board.app.reset()
