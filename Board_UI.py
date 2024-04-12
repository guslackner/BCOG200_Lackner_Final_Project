import tkinter as tk
import math
from Hex_Logic import Gameboard

class Draw:
    def __init__(self, gameboard, size=11, separation=20):
        """
        Initializes the Draw class with a gameboard, size, and separation.
        
        Parameters:
        - gameboard: imported logic class.
        - size: The dimensions of the gameboard. Default is 11x11.
        - separation: The separation between hexagons. Default 20px. Same as 2*radius
        """
        
        #initialize
        self.gameboard = gameboard
        self.size = size
        self.separation = separation
        self.turn = 0
        #we only need the rows and columns for the logic, so the board array is flattened into a tuple
        #this is useful later when a single index is used to know what cell is clicked
        self.flat_board = tuple([item for sublist in self.gameboard.board for item in sublist])
        
        #create Tkinter window
        root = tk.Tk()
        root.geometry('800x600')
        
        #Tkinter canvas
        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack(anchor=tk.CENTER, expand=True)
        
        
        #draw the points
        self.points = self.find_points(size, separation)
        self.points = self.translate_points()
        self.draw_hex(self.canvas, self.points, separation)
        self.draw_buttons(self.canvas, self.points, self.separation, self.size)
        self.canvas.update()
        self.intro_dialogue() #dialogue box summoned after the canvas so that it appears on top
        root.mainloop()
        
        
    def get_board(self):
        """
        Fetches the gamestate from the logic class and flatten it from an array into a tuple so that any entry can be easily found
        """
        
        self.flat_board = tuple([item for sublist in self.gameboard.board for item in sublist])

    def update_board(self):
        """
        Updates the gameboard display with the current game state. Called recursively by make_move()
        """
        self.get_board()
        self.points = self.translate_points()
        self.draw_hex(self.canvas, self.points, self.separation)
        self.draw_buttons(self.canvas, self.points, self.separation, self.size)
        self.canvas.update()

    def draw_hexagon(self, canvas, center_x, center_y, color='grey'):
        """
        Draws a hexagon on the canvas at the specified center coordinates with the given color. Note that the hexagon is balanced on its end by a rotation by pi/6 radians. 
        
        Parameters:
        - canvas: The Tkinter canvas to draw on.
        - center_x: The x-coordinate of the hexagon's center.
        - center_y: The y-coordinate of the hexagon's center.
        - color: The color of the hexagon. Default is 'grey', 'blue', and 'red' are also used
        """
        
        # Calculate the coordinates of the hexagon's vertices with adjusted angles
        points = []
        for i in range(6):
            angle = (i * 2 * math.pi / 6) - (math.pi / 6) # Adjusted angle calculation
            x = center_x + self.separation/2 * math.cos(angle)
            y = center_y + self.separation/2 * math.sin(angle)
            points.append(x)
            points.append(y)

        #draw the hexagon
        canvas.create_polygon(points, fill=color, outline='black')

    def find_points(self, size, separation):
        """
        Calculates and returns the points for drawing hexagons and buttons based on the size (dimension) and separation (two radii between each center point).
        
        Parameters:
        - size: The dimension of the gameboard.
        - separation: The separation between adjacent hexagons' centers.
        
        Returns:
        - A list of points for creating the grid.
        """
        points = []
        for row in range(size):
            #calculate the starting y-coordinate for the current row the root three comes from pythangoreas (2r)^2 = r^2 + x^2 
            y_start = row * separation/2 * math.sqrt(3)
            #calculate the starting x-coordinate for the first point in the current row
            x_start = 0 if row == 0 else row * separation / 2
            for point in range(size):
                #calculate the x and y coordinates for the current point
                x = x_start + point * separation
                y = y_start
                #append the coordinates as a tuple to the list of points
                points.append((x, y))
        return points

    def average_points(self):
        """
        Calculates and returns the average x and y coordinates for all points.
        
        Returns:
        - A tuple of the average x and y coordinates.
        """
        #sum the coordinates
        sum_x = sum(point[0] for point in self.points)
        sum_y = sum(point[1] for point in self.points)

        #divide
        avg_x = sum_x / len(self.points)
        avg_y = sum_y / len(self.points)

        return avg_x, avg_y

    def translate_points(self):
        """
        Translates the points to the center of the canvas.
        
        Returns:
        - centered points.
        """
        #get the average
        avg_x, avg_y = self.average_points()

        #find the center of the canvas
        self.canvas.update()
        canvas_width = int(self.canvas.winfo_width())
        canvas_height = int(self.canvas.winfo_height())
        center_x = canvas_width / 2
        center_y = canvas_height / 2

        #translate each point by adding the center and subtracting the average
        translated_points = [(x - avg_x + center_x, y - avg_y + center_y) for x, y in self.points]

        return translated_points


    def draw_hex(self, canvas, points, separation):
        """
        Draws hexagons on the canvas based on the points and separation.
        
        Parameters:
        - canvas: The Tkinter canvas to draw on.
        - points: The points for drawing hexagons.
        - separation: The separation between adjacent hexagons' centers.
        """
        for i, point in enumerate(points):
            x, y = point
            color='grey'
            if self.flat_board[i] == 1:
                color = 'red'
            elif self.flat_board[i] == 2:
                color = 'blue'
            self.draw_hexagon(canvas, x, y, color)

        
    def draw_buttons(self, canvas, points, separation, size):
        """
        Draws invisible rectangular buttons on top of the hexagons for user interaction.
        
        Parameters:
        - canvas: The Tkinter canvas to draw on.
        - points: The points grid.
        - separation: The separation between adjacent hexagons' centers.
        - size: The dimension of the gameboard.
        """
        #draw invisible rectangular buttons on top of the hexagons
        for i, point in enumerate(points):
            x, y = point
            #make the button button a bit smaller than the radius
            button_size = separation / 3
            #draw the button
            square = canvas.create_rectangle(x - button_size, y - button_size, x + button_size, y + button_size, fill='', outline='')
            #make the button trigger the game logic function
            canvas.tag_bind(square, '<Button-1>', lambda event, i=i: self.make_move(i))

    def make_move(self, i):
        """
        Processes a move based on the index of the clicked hexagon. Reffered to from the buttons in draw_buttons().
        
        Parameters:
        - i: The index of the clicked hexagon. Also requires knowledge of the size, but takes this from the object.
        """
        #given the index, figure out what row and it represents
        self.row_index = i // self.size
        self.col_index = i % self.size
        #game logic, adapted from the original loop
        player = 'red' if self.turn % 2 == 0 else 'blue'
        winner = self.gameboard.play(self.row_index, self.col_index, player)
        if winner:
            print(winner)
            self.winner_dialog()
        else:
            self.turn += 1
            #recursive call so the game continues
            self.update_board()
            
    def winner_dialog(self):
        """
        Displays a dialog box announcing the winner of the game.
        """
        winner = 'Red wins' if self.turn % 2 == 0 else 'Blue wins'
        
        #new top-level window
        winner_dialog = tk.Toplevel(self.canvas)
        winner_dialog.title('Winner')
        
        #bar label
        winner_label = tk.Label(winner_dialog, text=winner)
        winner_label.pack(pady=10)
        
        #button for quit Tkinter Note: sometimes acts up on my machine
        quit_button = tk.Button(winner_dialog, text="Yay!", command=self.canvas.quit)
        quit_button.pack(pady=10)
    
    def intro_dialogue(self):
        """
        Displays an introductory dialog box with game instructions.
        """
        #new top-level window
        rules_dialog = tk.Toplevel(self.canvas, width=150, height=150)
        rules_dialog.title('How to play')
        
        #bar label
        rules_label = tk.Label(rules_dialog, text="Instructions\n Player1 aka 'red' should try to connect the top of the game board with the bottom.\n Player2 aka 'blue' should try to connect the left to the right side.\n You can claim one unoccupied square per turn.\n Good luck!")
        rules_label.pack(pady=10)
        
        #button only closes the dialogue box
        quit_button = tk.Button(rules_dialog, text="Continue", command=rules_dialog.destroy)
        quit_button.pack(pady=10)
        
if __name__ == "__main__":
    gameboard = Gameboard()
    draw = Draw(gameboard)