import uuid

def minimax(board, player, depth, alpha=-1, beta=1, graph=None, parent=None):
  score = board.score()
  if score is not None:
    return score

  moves = board.get_possible_moves()
  if player:
    best = -5
    # それ以外の手を試す
    for move in moves:
      node_id = uuid.uuid1()
      if graph is not None:
        graph.add_node(node_id, data=move)
        if parent is not None:
          graph.add_edge(parent, node_id)
      board.make_move(move, player)
      best = max(best, minimax(board, not player, depth + 1, alpha, beta, graph, node_id))
      board.undo_move(move, player)
      alpha = max(alpha, best)
      if alpha >= beta:
        return best
    return best
  else:
    best = 5
    for move in moves:
      node_id = uuid.uuid1()
      if graph is not None:
        graph.add_node(node_id, data=move)
        if parent is not None:
          graph.add_edge(parent, node_id)
      board.make_move(move, player)
      best = min(best, minimax(board, not player, depth + 1, alpha, beta, graph, node_id))
      board.undo_move(move, player)
      beta = min(beta, best)
      if alpha >= beta:
        return best
    return best