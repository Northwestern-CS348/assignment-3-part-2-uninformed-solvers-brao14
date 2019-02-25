from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.
        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.
        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.
        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))
        Returns:
            A Tuple of Tuples that represent the game state
        """
        # checks to see if 3 disk or 5 disk game
        # creats disk set accordingly
        if not self.kb.kb_ask(parse_input("fact: (on disk4 ?X")):
            set_of_disks = ["disk1", "disk2", "disk3"]
        else:
            set_of_disks = ["disk1", "disk2", "disk3", "disk4", "disk5"]

        # for each disk, asks whether that disk is on peg
        # returns the game state based on the fact and appends to the peg arrays accordingly
        peg1, peg2, peg3 = [], [], []
        for s_disk in set_of_disks:
            fact = parse_input("fact: (on " + s_disk+ " ?X)")
            state = self.kb.kb_ask(fact)
            if str(state[0]) == "?X : peg1":
                peg1.append(int(s_disk[-1]))
            elif str(state[0]) == "?X : peg2":
                peg2.append(int(s_disk[-1]))
            elif str(state[0]) == "?X : peg3":
                peg3.append(int(s_disk[-1]))

        # returns the game state specified through peg arrays
        return (tuple(peg1), tuple(peg2), tuple(peg3))

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.
        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)
        Args:
            movable_statement: A Statement object that contains one of the currently viable moves
        Returns:
            None
        """
        state = self.getGameState()
        disk = str(movable_statement.terms[0])

        ts = str(movable_statement.terms[2])
        ts_num = int(ts[-1])

        ist = str(movable_statement.terms[1])
        ist_num = int(ist[-1])

        self.kb.kb_add(parse_input("fact: (on " + disk + " " + ts + ")"))
        self.kb.kb_retract(parse_input("fact: (on " + disk + " " + ist + ")"))
        
        if not state[ts_num - 1]:
            self.kb.kb_retract(parse_input("fact: (empty " + ts + ")"))
        else:
            self.kb.kb_retract(
                parse_input("fact: (onTop disk" + str(state[ts_num - 1][0]) + " " + ts + ")"))

        self.kb.kb_add(parse_input("fact: (onTop " + disk + " " + ts + ")"))
        self.kb.kb_retract(parse_input("fact: (onTop " + disk + " " + ist + ")"))
        
        state = self.getGameState()
        if not state[ist_num - 1]:
            self.kb.kb_add(parse_input("fact: (empty " + ist + ")"))
        else:
            self.kb.kb_add(parse_input("fact: (onTop disk" + str(state[ist_num - 1][0]) + " " + ist + ")"))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.
        Args:
            movable_statement: A Statement object that contains one of the previously viable moves
        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.
        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.
        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))
        Returns:
            A Tuple of Tuples that represent the game state
        """
        row1, row2, row3 = [], [], []
        for i in range(0, 3):
            for j in range(0, 3):
                ask = parse_input("fact: (pos ?X pos" + str(i+1) + " pos" + str(j+1) + ")")
                tile = str(self.kb.kb_ask(ask)[0])[-1]
                if tile == "y":
                    tile = -1
                if j == 0:
                    tile = int(tile)
                    row1.append(tile)
                elif j == 1:
                    tile = int(tile)
                    row2.append(tile)
                elif j == 2:
                    tile = int(tile)
                    row3.append(tile)

        return (tuple(row1), tuple(row2), tuple(row3))

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.
        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)
        Args:
            movable_statement: A Statement object that contains one of the currently viable moves
        Returns:
            None
        """
        state = self.getGameState()

        tile = str(movable_statement.terms[0])
        ist_x = str(movable_statement.terms[1])
        ist_y = str(movable_statement.terms[2])
        ts_x = str(movable_statement.terms[3])
        ts_y = str(movable_statement.terms[4])

        self.kb.kb_retract(parse_input("fact: (pos " + tile + " " + ist_x + " " + ist_y + ")"))
        self.kb.kb_retract(parse_input("fact: (pos empty " + ts_x + " " + ts_y + ")"))

        self.kb.kb_add(parse_input("fact: (pos " + tile + " " + ts_x + " " + ts_y + ")"))
        self.kb.kb_add(parse_input("fact: (pos empty " + ist_x + " " + ist_y + ")"))
        
    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.
        Args:
            movable_statement: A Statement object that contains one of the previously viable moves
        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))