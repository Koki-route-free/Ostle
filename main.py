# 2人のプレイヤーをそれぞれBLACK,WHITE何もない場所をEMPTY,ブラックホールをHOLLとする

BLACK = +1
WHITE = -1
EMPTY = 0
HOLL = 10


# 初期配置5×5の中心にホール、盤面の外にホールがあると仮定する
board = [
  [HOLL,  HOLL,  HOLL,  HOLL,  HOLL,  HOLL, HOLL],
  [HOLL, WHITE, WHITE, WHITE, WHITE, WHITE, HOLL],
  [HOLL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, HOLL],
  [HOLL, EMPTY, EMPTY,  HOLL, EMPTY, EMPTY, HOLL],
  [HOLL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, HOLL],
  [HOLL, BLACK, BLACK, BLACK, BLACK, BLACK, HOLL],
  [HOLL,  HOLL,  HOLL,  HOLL,  HOLL, HOLL,  HOLL],
]

# 実際に見えている部分
def view_board():
  view = [
    [x for i, x in enumerate(board[1]) if i>0 and i<6],
    [x for i, x in enumerate(board[2]) if i>0 and i<6],
    [x for i, x in enumerate(board[3]) if i>0 and i<6],
    [x for i, x in enumerate(board[4]) if i>0 and i<6],
    [x for i, x in enumerate(board[5]) if i>0 and i<6],
  ]
  return view

# ぞれぞれの表示方法
character = {EMPTY:" - ", BLACK:" B ", WHITE:" W ", HOLL:" ● ", }
player_name = {BLACK: "BLACK : ", WHITE: "WHITE : "}

# 実際に表示させる
def print_board():
  view = view_board()
  print()
  print("  a  b  c  d  e")
  for i, j in enumerate(view):
      board_line = str(i + 1)
      for k in j:
          board_line += character[k]
      print(board_line)
  print()


# 毎ターンプレーヤーが変わるようにする
def another_player(player: int):
  return player * -1

# 動かすコマと動かす方向を取得
def get_place(player: int):
  while True:
      try:
          place = input(player_name[player] + "動かすコマの場所、動かす方向（上0左1下2右3）例) a21 : ")
          assert len(place) == 3  # 3文字で無ければ、再入力
          input_1 = ord(place[0]) - ord("a") + 1
          input_2 = int(place[1])
          input_3 = int(place[2])
          return input_1, input_2, input_3
      except (ValueError, AssertionError):
          pass

# ゲームが終わる条件
def finish_game():
  view = view_board()
  winner = 0
  # 盤面のコマが3個以下になった方が負け
  count_B = 0
  count_W = 0
  for i in range(5):
    count_B += view[i].count(BLACK)
    count_W += view[i].count(WHITE)
  if count_B < 4:
    winner = +1
  elif count_W < 4:
    winner = -1
  return winner

# ゲームが続くかの判定
def continue_game():
  winner = finish_game()
  if winner==0:
      return True
  else:
      return False

# 結果の表示
def print_judgment():
  winner = finish_game()
  if winner == +1:
      print("黒の勝ち〜〜〜！！")
  elif winner == -1:
      print("白の勝ち〜〜〜！！")
  

# 盤面を変える
def change_board(player:int,x:int, y:int, z:int):
  # 動かすコマが自分のコマの時
  if board[y][x] == player:
    new_board = []
    i = 0
    # 動かす方向が上か下の時
    if z == 0 or z == 2:
      while True:
        i += 1
        j = i - 1
        if board[y+i*(z-1)][x] == HOLL:
          break
        elif board[y+i*(z-1)][x] == EMPTY:
          new_board.append(board[y+j*(z-1)][x])
          break
        new_board.append(board[y+j*(z-1)][x])
      for k, l in enumerate(new_board):
        k += 1
        board[y+k*(z-1)][x] = l
    # 動かす方向が左右の時
    elif z == 1 or z == 3:
      while True:
        i += 1
        j = i - 1
        if board[y][x+i*(z-2)] == HOLL:
          break
        elif board[y][x+i*(z-2)] == EMPTY:
          new_board.append(board[y][x+j*(z-2)])
          break
        new_board.append(board[y][x+j*(z-2)])
      for k, l in enumerate(new_board):
        k += 1
        board[y][x+k*(z-2)] = l
    board[y][x] = EMPTY
    return True
  # 動かすコマがブラックホールの時
  elif board[y][x] == HOLL:
    if (z == 0 or z == 2) and (board[y+z-1][x] == EMPTY):
      board[y+z-1][x] = HOLL
    elif (z == 1 or z == 3) and (board[y][x+z-2] == EMPTY):
      board[y][x+z-2] = HOLL
    board[y][x] = EMPTY
    return True
  else:
    return False

# 座標入力を正しくできるまで繰り返す
def get_int(player: int):
  while True:
      x, y, z = get_place(player)
      if change_board(player, x, y, z):
          break

# 実際の実行関数
def main():
  player = BLACK
  print_board()
  while True:
      get_int(player)
      print()
      print("----------------------")
      print_board()
      if continue_game():
          player = another_player(player)
      else:
          break
  print_judgment()
  print()

if __name__ == "__main__":
  main()
  
