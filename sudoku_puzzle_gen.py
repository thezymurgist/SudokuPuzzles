"""
This program generates sudoku boards based on the user's
selected difficulty and varifies whether or not the user has solved it correctly.
These boards will be stored in a file to be accessed by a program that
allows the user to play the game.

-Zym - January 2018
"""
from random import shuffle
from random import choice

# eventually, this will take arguments that determine the size of the board and its difficulty
regions = {}
size = 0
#difficulty = ""


class Cell:
  def __init__(self, edge, value, coordinates, cell_order):
    self.edge = edge
    self.value = value
    self.coordinates = coordinates
    self.cell_order = cell_order
    self.band = self.coordinates[1]
    self.stack = self.coordinates[0]
    self.region = 0
    
    # Determine cell region
    for key in regions:
      if self.cell_order in regions[key]:
        self.region = int(key)


# Function to generate a dictionary of regions and corresponding cell_order
# Saves from having to chain if statements and dictionary only created once
def region_assign(edge):
  region_dict = {}
  tracker = 1
  
  #holds sqrt of edge length
  n = int(edge ** .5)
  for i in range(1, edge + 1):
    reference_set = [x for x in range(tracker, tracker + (n))]
    order_set = []
    for j in range(n):
      temp_set = [(y + j * edge) for y in reference_set]
      for k in temp_set:
        order_set.append(k)
    region_dict[i] = order_set
    if (tracker + (n - 1)) % edge == 0:
      tracker += n * (edge - n + 1)
    else:
      tracker += n

  return region_dict

    
# Creates the game board object        
class Board:
  def __init__(self, edge, difficulty):
    self.edge = edge
    self.difficulty = difficulty
    self.board = []
    self.board_key = []
    self.cell_dict = {}
    # Consider replacing the board with a list of objects, aka cells, which have
    # certain parameters, such as possible values, actual value, coordinates, etc.
   
   # creating a key used to get the value of cells at various coordinates; these will be used to create a dictionary of objects, or maybe just a dictionary? Or use the coordinates to declare an instance of your Cell object
  def generate_key(self):
    for i in range(1, self.edge + 1):
      temporary = []
      band = 65
      for j in range(self.edge):
        temporary.append((chr(band), i))
        band += 1
      self.board_key.append(temporary)  
  
  # Creates the board by band and stores it in board as an integer
  def generate_board(self):
  
    for i in range(self.edge):
      temporary = []
      
      #Establishes Band1
      if (i == 0):
        a = [x for x in range(1, self.edge + 1)]
        shuffle(a)
        for j in a:
          temporary.append(j)
      
      #deals with the logic for generating the other cells    
      else:    
        for j in range(self.edge):
          temporary.append(0)
          
      self.board.append(temporary)

  
 
      
  # Print statements that can be used for testing
  # Prints the initial board values prior to Cell object creation
  def print_board(self):
    str_board = []
    
    for i in range(self.edge):
      temporary = []
      for j in range(self.edge):
        temporary.append(str(self.board[i][j]))
      str_board.append(temporary)
        
    for i in range(self.edge):
      print (" ".join(str_board[i]))
  
  # Prints the board key to the screen
  def print_board_key(self):
    for i in range(self.edge):
      print (self.board_key[i])
  
  # Prints the completed board post-Cell object creation using class attributes
  def print_board_complete(self):
    str_board = []
    for i in range(self.edge):
      temporary = []
      for j in range(self.edge):
        temporary.append(str(self.cell_dict[self.board_key[i][j]].value))
      str_board.append(temporary)
    
    for i in range(self.edge):
      print (" ". join(str_board[i]))

  # Fills a dictionary that contains the Cell objects representing the board
  def create_cells(self):
    cell_order = 1
    for i in range(self.edge):
      for j in range(self.edge):
        self.cell_dict[self.board_key[i][j]] = Cell(self.edge, self.board[i][j], self.board_key[i][j], cell_order)
        cell_order += 1

  # When this class is created, it needs to do things in this order:
    # generate_board()
    # generate_key()
    # create_cells() based on original board_key
    # cycle through cells; if cell value is 0, then fill it based on rules
    # print the new board
  
  # Once the Cells have been created, this class method assigns the appropriate values
  # from those available for all cells whose value was not set arbitrarily by the
  # create_cells and generate_board methods above
  def complete_cells(self):
    for i in range(self.edge):
      for j in range(self.edge):
        current_key = self.board_key[i][j]
        if self.cell_dict[current_key].value == 0:
          avail = [x for x in range(1, self.edge + 1)]
          unavail = check_cells(self.cell_dict, current_key)
          if len(unavail) == self.edge:
            wipe_random(self.cell_dict, self.board_key, self.edge)
            self.complete_cells()
          else:
            avail = [x for x in avail if x not in unavail]
            self.cell_dict[current_key].value = choice(avail)
        else:
          pass
          
  # Returns a version of the board for writing to file        
  def return_board(self):
    str_board = []
    for i in range(self.edge):
      temporary = []
      for j in range(self.edge):
        temporary.append(str(self.cell_dict[self.board_key[i][j]].value))
      str_board.append(temporary)
    return str_board
          
          
#check cell function that can be used in board generation to create sets of appropriate values for any given cell
def check_cells(cell_dict, cell_key):
  unavailable_vals = []
  for key in cell_dict:
    if key[0] == cell_key[0] or \
       key[1] == cell_key[1] or \
       cell_dict[key].region == cell_dict[cell_key].region:
        if cell_dict[key].value != 0 and \
           cell_dict[key].value not in unavailable_vals:
            unavailable_vals.append(cell_dict[key].value)
    else:
      pass
  return unavailable_vals

# Selects a number of random cells equal to the length of the board and resets their
# values to zero if the puzzle cannot be completed.
def wipe_random(cell_dict, board_key, edge):
  wiped_cells = []
  for i in range(edge):
    wiped_cells.append(choice(board_key[i]))
  for key in wiped_cells:
    cell_dict[key].value = 0;
  

    
  
# Starts the game and calls the necessary class methods to create a new board  
def start_game():
  global size
  while size != 9 and \
        size != 16:
    size = int(input("Please input the size of the board.\n You may choose 9 or 16: "))
  
  difficulty = "Normal" # input("Please select a difficulty.\nYou many choose: Normal")
  quantity = int(input("How many boards do you require? You may select up to 2000: "))
  if quantity < 0:
    quantity = 1
  elif quantity > 2000:
    quantity = 2000
  else:
    pass
  
  global regions
  regions = region_assign(size)
  
  f = open("puzzle_bases", "w")
  
  for i in range(quantity):
    global my_board
    my_board = Board(size, difficulty)
    my_board.generate_board()
    my_board.generate_key()
    my_board.create_cells()
    my_board.complete_cells()
    f.write("\n".join(map(lambda x: str(x), my_board.return_board())))
    f.write(" \n\n")
  f.close()
    

  
  #TESTING
  #print (my_board.cell_dict)
  #print (my_board.cell_dict[("D", 1)].value)
  #print (my_board.cell_dict[("D", 1)].coordinates)
  #print (type(my_board.cell_dict["H2"].coordinates))
  #print (my_board.cell_dict[("G", 1)].band)
  #print (my_board.cell_dict[("F", 9)].stack)
  #print (my_board.cell_dict[("F", 7)].region)
  #print (my_board.cell_dict[("A", 1)].region)
  #print (my_board.cell_dict[("A", 4)].cell_order)
  #print (my_board.cell_dict[("E", 5)].cell_order)

start_game()

#my_board.print_board_complete()
