import numpy as np

class Board3:
    # 初期状態のボード
    def __init__(self, randomize=False):
        self.randomize = randomize
        # 先手Aのボード
        self.board_a = np.zeros((3, 3, 3), dtype=np.uint8)
        # 後手Bのボード
        self.board_b = np.zeros((3, 3, 3), dtype=np.uint8)
        # 勝ちパターンのリスト
        # 対角線で4, 各軸方向で27, 各面の対角線で18, 全部で49
        self.lines = []
        # 各軸方向の直線
        for i in range(3):
            for j in range(3):
                self.lines.append([(i, j, k) for k in range(3)])  # x-y平面
                self.lines.append([(i, k, j) for k in range(3)])  # x-z平面
                self.lines.append([(k, i, j) for k in range(3)])  # y-z平面
        # 面ではない対角線
        self.lines.extend([
            [(i, i, i) for i in range(3)],
            [(i, i, 2 - i) for i in range(3)],
            [(i, 2 - i, i) for i in range(3)],
            [(2 - i, i, i) for i in range(3)],
        ])
        # 面の上の対角線
        for i in range(3):
            self.lines.extend([
                [(i, j, j) for j in range(3)],
                [(i, j, 2 - j) for j in range(3)],
                [(j, i, j) for j in range(3)],
                [(j, i, 2 - j) for j in range(3)],
                [(j, j, i) for j in range(3)],
                [(j, 2 - j, i) for j in range(3)],
            ])
        if len(self.lines) != 49:
            raise Exception("勝利判定条件が正しくありません。")

    # 現在のボードを返す
    def get_current_board(self):
        return (self.board_a | self.board_b)

    # 次に打てる手を返す
    def get_possible_moves(self):
        possible_moves = []

        board = self.get_current_board()
        empty_spaces = np.argwhere(board == 0)

        for x, y, z in empty_spaces:
            if (x == 0 or board[x-1][y][z] == 1):
                possible_moves.append((x, y, z))

        if self.randomize:
            np.random.shuffle(possible_moves)
        return possible_moves
        
    # 手を打つ
    def make_move(self, pos, player):
      if player:
        self.board_a[pos] = 1
      else:
        self.board_b[pos] = 1
    
    def undo_move(self, pos, player):
      if player:
        self.board_a[pos] = 0
      else:
        self.board_b[pos] = 0
    
    def is_full(self):
        return len(np.argwhere(self.get_current_board() == 0)) == 0
    
    def score(self):
        # プレイヤーAの視点で勝てるかどうかを判定
        # 勝てる場合1 負ける場合-1 引き分け0
        if self.is_full():
            return 0
        for line in self.lines:
            values = [self.board_a[x][y][z] for x, y, z in line]
            if values == [1, 1, 1]:
                return 1
            values = [self.board_b[x][y][z] for x, y, z in line]
            if values == [1, 1, 1]:
                return -1

        # 勝敗がまだ決まっていない場合はNoneを返す
        return None