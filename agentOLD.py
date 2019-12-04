from gameobjects import GameObject
from move import Move, Direction


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
        # and h is the heuristic function, which we choose as the distance between the current node and the goal node.
        # and we choose the Manhattan heuristic for this (i.e x distance + y distance)

        g = turns_alive

        # start and end positions
        start_position = [0, 0]
        food_position = [0, 0]

        # initialize start position
        if turns_alive == 0:
            start_position = head_position

        # find food and set end position
        for x in range(len(board)):
            for y in range(len(board)):
                if board[x][y] == GameObject.FOOD:
                    h = abs(x - head_position[0]) + abs(y - head_position[1])
                    food_position = [x, y]

        f = g + h

        g_of_food = abs(head_position[0] - food_position[0]) + \
            abs(head_position[1] - food_position[1])

        # Node format is an array. Format is as such:
        # [position of current node, f, g, h, parent node]
        # start_node = [start_position, f, g, h, None]
        start_node = {
            "position": start_position,
            "f": f,
            "g": g,
            "h": h,
            "parent": None
        }
        end_node = {
            "position": food_position,
            "f": g_of_food + h,
            "g": g_of_food,
            "h": h,
            "parent": None
        }

        open_list = []
        closed_list = []
        returnPath = []
        open_list.append(start_node)

        while (len(open_list) > 0):
            print(open_list)
            print("-----")
            least_cost = open_list[0].get("f")
            current_node = open_list[0]
            current_index = 0
            for index in range(len(open_list)):
                if open_list[index].get("f") < least_cost:
                    current_node = open_list[0]
                    current_index = index

            open_list.pop(current_index)
            closed_list.append(current_node)

            if current_node == end_node:
                path = []
                temp = current_node
                while temp is not None:
                    path.append(temp["position"])
                    temp = temp.get("parent")
                returnPath = path[::-1]
                break

            children = []
            # Adjacent squares
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                # Get node position
                node_position = (current_node.get("position")[0] + new_position[0],
                                 current_node.get("position")[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(board) - 1) or node_position[0] < 0 or node_position[1] > (len(board[len(board)-1]) - 1) or node_position[1] < 0:
                    continue
                # Make sure walkable terrain
                if board[node_position[0]][node_position[1]] != GameObject.WALL:
                    tempG = abs(node_position[0] - food_position[0]) + \
                        abs(node_position[1] - food_position[1])
                    tempH = abs(
                        food_position[0] - node_position[0]) + abs(food_position[1] - node_position[1])
                    new_node = {
                        "position": node_position,
                        "f": tempG + tempH,
                        "g": tempG,
                        "h": tempH,
                        "parent": current_node
                    }
                    # Append
                    children.append(new_node)

            # Loop through children
            for child in children:
                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child["g"] = current_node.get("g") + 1
                child["h"] = ((child.get("position")[0] - end_node.get("position")[0])
                              ** 2) + ((child.get("position")[1] - end_node.get("position")[1]) ** 2)
                child["f"] = child.get("g") + child.get("h")

                # Child is already in the open list")
                for open_node in open_list:
                    if child == open_node and child.get("g") > open_node.get("g"):
                        continue

                open_list.append(child)
        # for item in returnPath:
        #     print(item)

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
