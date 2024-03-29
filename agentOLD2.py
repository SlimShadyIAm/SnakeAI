from gameobjects import GameObject
from move import Move, Direction
import time


class Node():
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position

        self.f = 0
        self.g = 0
        self.h = 0


def heuristic(start_node, end_node):
    return (((start_node.position[0] - end_node.position[0]) ** 2) +
            ((start_node.position[1] - end_node.position[1]) ** 2)) ** 0.5


def astar(head_position, board, score, turns_alive):
    print("Head position:", head_position)
    start_node = Node(None, head_position)

    end_pos = (0, 0)
    end_node = Node(None, None)

    for x in range(len(board)):
        for y in range(len(board)):
            if board[x][y] == GameObject.FOOD:
                end_pos = (x, y)
                end_node.position = end_pos
                print("Food position: ", end_pos)

    start_node.h = heuristic(start_node, end_node)
    start_node.f = heuristic(start_node, end_node)

    open_list = []
    closed_list = []

    open_list.append(start_node)

    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)
        for closed in closed_list:
            print(closed.position)
        print("---")
        if current_node.position == end_node.position:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        # Adjacent squares

        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:

            # Get node position
            node_position = (
                current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(board) - 1) or node_position[0] < 0 or node_position[1] > (len(board[len(board)-1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if not (board[node_position[0]][node_position[1]] == GameObject.EMPTY or board[node_position[0]][node_position[1]] == GameObject.FOOD):
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)
            visited_list.append(node_position)

        # Loop through children
        for child in children:
            for closed_node in closed_list:
                if child.position == closed_node.position:
                    # Child is on the closed list
                    continue
            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = heuristic(child, end_node)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child.position == open_node.position and child.g > open_node.g:
                    continue
            # Add the child to the open list
            open_list.append(child)
            # time.sleep(0.1)


class Agent:

    def __init__(self):
        """" Constructor of the Agent, can be used to set up variables """

    def get_move(self, board, score, turns_alive, turns_to_starve, direction, head_position, body_parts):
        """This function behaves as the 'brain' of the snake. You only need to change the code in this function for
        the project. Every turn the agent needs to return a move. This move will be executed by the snake. If this
        functions fails to return a valid return (see return), the snake will die (as this confuses its tiny brain
        that much that it will explode). The starting direction of the snake will be North.

        :param board: A two dimensional array representing the current state of the board. The upper left most
        coordinate is equal to (0,0) and each coordinate (x,y) can be accessed by executing board[x][y]. At each
        coordinate a GameObject is present. This can be either GameObject.EMPTY (meaning there is nothing at the
        given coordinate), GameObject.get("f")OOD (meaning there is food at the given coordinate), GameObject.WALL (meaning
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

        # First we need to implement the f = g + h function.
        # f is the total cost of a node,
        # g is the distance between the current node and the start node, use turns_alive
        # h is the heuristic function, which we choose as the diagonal between the current node and the goal node.
        # and use pythagorean theorum for this

        thing = astar(head_position, board, score, turns_alive)
        print(
            "Current position: {0}\nPath: {1}\n-----".format(head_position, thing))

        if thing[1][0] != head_position[0]:
            if thing[1][0] > head_position[0]:
                if direction == Direction.EAST:
                    return Move.STRAIGHT
                elif direction == Direction.NORTH:
                    return Move.RIGHT
                elif direction == Direction.WEST | direction == Direction.SOUTH:
                    return Move.LEFT
            elif thing[1][0] < head_position[0]:
                if direction == Direction.WEST:
                    return Move.STRAIGHT
                elif direction == Direction.NORTH:
                    return Move.LEFT
                elif direction == Direction.EAST | direction == Direction.SOUTH:
                    return Move.LEFT

        if thing[1][1] != head_position[1]:
            if thing[1][1] > head_position[1]:
                if direction == Direction.WEST:
                    return Move.LEFT
                elif direction == Direction.SOUTH:
                    return Move.STRAIGHT
                elif direction == Direction.EAST | direction == Direction.NORTH:
                    return Move.LEFT
            elif thing[1][1] < head_position[1]:
                if direction == Direction.EAST:
                    return Move.LEFT
                elif direction == Direction.NORTH:
                    return Move.STRAIGHT
                elif direction == Direction.WEST | direction == Direction.SOUTH:
                    return Move.RIGHT

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
