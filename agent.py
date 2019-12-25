from gameobjects import GameObject
from move import Move, Direction
import time


# This is the class which will hold a potential state the astar algo considers
# It contains things like the f,g,h values of that state, information about
# the state of the board, and the state of the snake's body
class Node:
    def __init__(self, parent, position, snake_body, board):
        self.parent = parent
        self.position = position

        self.snake_body = snake_body
        self.board = board

        self.f = 0
        self.g = 0
        self.h = 0

        self.neighbors = []

    # make state printable (print(state))
    def __repr__(self):
        return "Item(%s, %s)" % (self.position, self.f)

# method to deepcopy the board list


def copy_board(board):
    copy = [[GameObject.EMPTY for x in range(
        len(board))] for y in range(len(board))]
    for x in range(len(board)):
        for y in range(len(board)):
            copy[x][y] = board[x][y] if board[x][y] is not GameObject.SNAKE_HEAD else GameObject.SNAKE_BODY
    return copy

# method that checks if a Node object is in a list


def nodeInSet(node, set):
    for setNode in set:
        if setNode.position == node.position:
            return True
    return False

# heuristic function. it is the square root of the manhattan distance


def heuristic(start_node, end_node, score):
    return (abs(
        start_node.position[0] - end_node.position[0]) + abs(start_node.position[1] - end_node.position[1])) ** 0.5


def astar(head_position, board, score, snake_body):
    # initialize our variables
    openSet = []  # open list, list of states we're considering
    closedSet = []  # closed list, list of states we're discarding
    startNode = Node(None, head_position, snake_body.copy(),
                     copy_board(board))  # initial state to find path to food from
    endNode = Node(None, None, None, None)  # goal state (food)

    # find the goal position
    for x in range(len(board)):
        for y in range(len(board)):
            if board[x][y] == GameObject.FOOD:
                # found it!
                endPos = (x, y)
                endNode.position = endPos  # set goal state's position

    # our start node needs a cost
    startNode.h = heuristic(startNode, endNode, score)
    startNode.f = startNode.h

    # start the open set with the start node
    openSet.append(startNode)

    while len(openSet) > 0:
        # we can keep going!
        # get the node with the lowest cost from the open set
        current = min(openSet, key=lambda x: x.f)

        # we're done! return the path we need to take...
        if current.position == endNode.position:
            path = []
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        openSet.remove(current)
        closedSet.append(current)

        # generate neighbors of the current state we're considering
        for neighborOffset in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            # Get neighbor position
            neighborPos = (
                current.position[0] + neighborOffset[0], current.position[1] + neighborOffset[1])

            # is this neighbor inside the bounds of the board?
            if (neighborPos[0] < (len(board)) and neighborPos[0] >= 0 and neighborPos[1] < (len(board[len(board)-1])) and neighborPos[1] >= 0):
                # can the snake safely move to this state without dying? (is it empty/food object?)
                if current.board[neighborPos[0]][neighborPos[1]] == GameObject.EMPTY or current.board[neighborPos[0]][neighborPos[1]] == GameObject.FOOD:
                    # make a new node object for this state!
                    boardState = copy_board(current.board)
                    tempSnakeState = current.snake_body.copy()

                    # our new state needs an updated snake body and board state
                    # if our snake body list is not empty (snake has more than just head)
                    if (len(tempSnakeState) > 0):
                        snakeTail = tempSnakeState[len(tempSnakeState) - 1]
                        # update the board state in this node as if the snake has just moved,
                        # so set the old tail position in board to empty
                        boardState[snakeTail[0]
                                   ][snakeTail[1]] = GameObject.EMPTY

                        # the position we're moving to is now the snake head in the board
                        boardState[neighborPos[0]
                                   ][neighborPos[1]] = GameObject.SNAKE_HEAD
                        # our old position we're moving from is now the snake body
                        boardState[current.position[0]
                                   ][current.position[1]] = GameObject.SNAKE_BODY
                        tempSnakeState = tempSnakeState[::1]

                    # our head has moved, so where the head was is now part of the body
                    tempSnakeState.insert(0, current.position)

                    neighborNode = Node(
                        current, neighborPos, tempSnakeState, boardState)
                    current.neighbors.append(neighborNode)

        for neighbor in current.neighbors:
            # do we need to evaluate this neighbor?
            if not nodeInSet(neighbor, closedSet):
                # check if the node already had a better g value...
                tentativeG = current.g + 1
                if nodeInSet(neighbor, openSet):
                    if neighbor.g > tentativeG:
                        # we found a better g value!
                        neighbor.g = tentativeG
                else:
                    neighbor.g = tentativeG
                    openSet.append(neighbor)
                neighbor.h = heuristic(neighbor, endNode, score)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current

# we have the coordinates we want to move to. now we need to know which direction to move into...
# this mess tries to figure out how.


def resolveMovePath(path, direction, head_position):
    # move in the x direction
    if path[1][0] != head_position[0]:
        if path[1][0] > head_position[0]:
            if direction == Direction.EAST:
                return Move.STRAIGHT
            elif direction == Direction.NORTH:
                return Move.RIGHT
            elif direction == Direction.WEST or direction == Direction.SOUTH:
                return Move.LEFT
        elif path[1][0] < head_position[0]:
            if direction == Direction.WEST:
                return Move.STRAIGHT
            elif direction == Direction.NORTH:
                return Move.LEFT
            elif direction == Direction.EAST or direction == Direction.SOUTH:
                return Move.RIGHT

    # move in y direction
    if path[1][1] != head_position[1]:
        if path[1][1] > head_position[1]:
            if direction == Direction.WEST:
                return Move.LEFT
            elif direction == Direction.SOUTH:
                return Move.STRAIGHT
            elif direction == Direction.EAST or direction == Direction.NORTH:
                return Move.RIGHT
        elif path[1][1] < head_position[1]:
            if direction == Direction.EAST:
                return Move.LEFT
            elif direction == Direction.NORTH:
                return Move.STRAIGHT
            elif direction == Direction.WEST or direction == Direction.SOUTH:
                return Move.RIGHT

# our path is empty, meaning our astar algorithm failed to find a path
# try to stall the snake, so that eventually a path might open up


def resolveMoveNoPath(board, head_position):
    path = []
    path.append(head_position)
    for neighborOffset in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            # generate neighbors of current position
        neighborPos = (
            head_position[0] + neighborOffset[0], head_position[1] + neighborOffset[1])
        if (neighborPos[0] < (len(board)) and neighborPos[0] >= 0 and neighborPos[1] < (len(board[len(board)-1])) and neighborPos[1] >= 0):
            if board[neighborPos[0]][neighborPos[1]] == GameObject.EMPTY or board[neighborPos[0]][neighborPos[1]] == GameObject.FOOD:
                # as long as the neighbor is moveable into, move in that direction
                path.append(neighborPos)
                return path
    # only reach here if the snake has nowhere to move to without dying. gg :(
    print("Goodbye cruel world, i'm stuck :(")
    return path


class Agent:

    def __init__(self):
        """" Constructor of the Agent, can be used to set up variables """
        self.path = []

    def get_move(self, board, score, turns_alive, turns_to_starve, direction, head_position, body_parts):
        """This function behaves as the 'brain' of the snake. You only need to change the code in this function for
        the project. Every turn the agent needs to return a move. This move will be executed by the snake. If this
        functions fails to return a valid return (see return), the snake will die (as this confuses its tiny brain
        that much that it will explode). The starting direction of the snake will be North.

        :param board: A two dimensional array representing the current state of the board. The upper left most
        coordinate is equal to (0,0) and each coordinate (x,y) can be accessed by executing board[x][y]. At each
        coordinate a GameObject is present. This can be either GameObject.EMPTY (meaning there is nopath at the
        given coordinate), GameObject.FOOD (meaning there is food at the given coordinate), GameObject.WALL (meaning
        there is a wall at the given coordinate. TIP: do not run into them), GameObject.SNAKE_HEAD (meaning the head
        of the snake is located there) and GameObject.SNAKE_BODY (meaning there is a body part of the snake there.
        TIP: also, do not run into these). The snake will also die when it tries to escape the board (moving out of
        the boundaries of the array)

        :param score: The current score as an integer. Whenever the snake eats, the score will be increased by one.
        When the snake tragically dies (i.e. by running its head into a wall) the score will be reset. In ohter
        words, the score describes the score of the current (alive) worm.

        :param turns_alive: The number of turns (as integer) the current snake is alive.

        :param turns_to_starve: The number of turns left alive (as integer) if the snake does not eat. If this number
        reaches 1 and there is not eaten the next turn, the snake dies. If the value is equal to -1, then the option
        is not enabled and the snake can not starve.

        :param direction: The direction the snake is currently facing. This can be either Direction.NORTH,
        Direction.SOUTH, Direction.WEST, Direction.EAST. For instance, when the snake is facing east and a move
        straight is returned, the snake wil move one cell to the right.

        :param head_position: (x,y) of the head of the snake. The following should always hold: board[head_position[
        0]][head_position[1]] == GameObject.SNAKE_HEAD.

        :param body_parts: the array of the locations of the body parts of the snake. The last element of this array
        represents the tail and the first element represents the body part directly following the head of the snake.

        :return: The move of the snake. This can be either Move.LEFT (meaning going left), Move.STRAIGHT (meaning
        going straight ahead) and Move.RIGHT (meaning going right). The moves are made from the viewpoint of the
        snake. This means the snake keeps track of the direction it is facing (North, South, West and East).
        Move.LEFT and Move.RIGHT changes the direction of the snake. In example, if the snake is facing north and the
        move left is made, the snake will go one block to the left and change its direction to west.
        """
        # we don't know where to move to. our path is empty. run astar so we know where to go to
        if len(self.path) <= 1:
            self.path = astar(head_position, board,
                              score, body_parts)

        # print(
        #     "Current position: {0}\nPath: {1}]\nScore: {2}\n-----".format(head_position, self.path, score))

        # was astar able to find a path? (if not, the array would be None)
        if self.path:
            # great, we did. move in that direction
            tempMove = resolveMovePath(self.path, direction, head_position)
            # delete the position we're about to move to before the next move after that
            del self.path[0]
            return
        # astar couldn't find a path, meaning the food isn't accessible, at least right now
        else:
            # try to stall the snake by moving around, maybe a path opens up
            self.path = resolveMoveNoPath(board, head_position)
            # do we have space to move around? (is the snake completely trapped?)
            if self.path:
                # no, we can stall
                if len(self.path) > 1:
                    tempMove = resolveMovePath(
                        self.path, direction, head_position)
                    del self.path[0]
                    return tempMove
                # snake is completely trapped. fuck
                else:
                    return Move.STRAIGHT

    def should_redraw_board(self):
        """
        This function indicates whether the board should be redrawn. Not drawing to the board increases the number of
        games that can be played in a given time. This is especially useful if you want to train you agent. The
        function is called before the get_move function.

        :return: True if the board should be redrawn, False if the board should not be redrawn.
        """
        return True

    def should_grow_on_food_collision(self):
        """
        This function indicates whether the snake should grow when colliding with a food object. This function is
        called whenever the snake collides with a food block.

        :return: True if the snake should grow, False if the snake should not grow
        """
        return True

    def on_die(self, head_position, board, score, body_parts):
        """This function will be called whenever the snake dies. After its dead the snake will be reincarnated into a
        new snake and its life will start over. This means that the next time the get_move function is called,
        it will be called for a fresh snake. Use this function to clean up variables specific to the life of a single
        snake or to host a funeral.

        :param head_position: (x, y) position of the head at the moment of dying.

        :param board: two dimensional array representing the board of the game at the moment of dying. The board
        given does not include information about the snake, only the food position(s) and wall(s) are listed.

        :param score: score at the moment of dying.

        :param body_parts: the array of the locations of the body parts of the snake. The last element of this array
        represents the tail and the first element represents the body part directly following the head of the snake.
        When the snake runs in its own body the following holds: head_position in body_parts.
        """
        print("score:", score)
        self.path = []
