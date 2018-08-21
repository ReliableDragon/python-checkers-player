import tkinter as tk
import random


TURN_TIME = 150

    
class Game(tk.Canvas):
    
    height = 800
    width = 800
    red_wins = 0
    blue_wins = 0

    def __init__(self, root):
        tk.Canvas.__init__(self, root, bg='#000000', bd=0, height=self.height, width=self.width, highlightthickness=0)
        self.pack()
        self.reset()

    def reset(self):
        self.squares = [self.create_rectangle(
                            100*(i%8), 100*(i//8), 100*(i%8)+100, 100*(i//8)+100, fill='#000000'
                            if (i % 2 == 0 and (i // 8) % 2 == 0) or (i % 2 == 1 and (i // 8) % 2 == 1) else '#ffffff', width=0)
                        for i in range(0, 64)]
        self.red_kings = []
        self.blue_kings = []
        self.turn_number = 0
        self.active_player = 'blue'
        self.red_pieces = {(i%8, i//8): self.create_oval(
                                *_get_piece_coords(i%8, i//8), fill="red")
                            for i in [0, 2, 4, 6, 9, 11, 13, 15, 16, 18, 20, 22]}
        self.blue_pieces = {(i%8, i//8): self.create_oval(
                                *_get_piece_coords(i%8, i//8), fill="blue")
                            for i in [41, 43, 45, 47, 48, 50, 52, 54, 57, 59, 61, 63]}
        self.after(TURN_TIME, self.move_active_player)

    def move_active_player(self):
        if len(self.blue_pieces) == 0:
            self.red_wins += 1
            self.show_message("Red wins!")
            return
        elif len(self.red_pieces) == 0:
            self.blue_wins += 1
            self.show_message("Blue wins!")
            return
        pieces = self.blue_pieces if self.active_player == 'blue' else self.red_pieces
        kings = self.blue_kings if self.active_player == 'blue' else self.red_kings
        enemy_pieces = self.blue_pieces if self.active_player == 'red' else self.red_pieces
        enemy_kings = self.blue_kings if self.active_player == 'red' else self.red_kings
        default_direction = -1 if self.active_player == 'blue' else 1

        piece_coords = (random.choice(list(pieces.keys())))
        pieces_tried = set(piece_coords)
        moved = False
        while not moved:
            x_directions = [1, -1]
            random.shuffle(x_directions)
            y_directions = [default_direction]
##            if piece_coords in kings:
##                y_directions.append(-default_direction)
##            random.shuffle(y_directions)
            if piece_coords in kings:
                target_piece = min(
                    enemy_pieces.keys(),
                    key=lambda foe: (abs(piece_coords[0] - foe[0]) + abs(piece_coords[1] - foe[1])) ** 0.5)
                x_directions = [1, -1] if target_piece[0] > piece_coords[0] else [-1, 1]
                y_directions = [1, -1] if target_piece[1] > piece_coords[1] else [-1, 1]
            for dir_x in x_directions:
                for dir_y in y_directions:
                    new_x = piece_coords[0] + dir_x
                    new_y = piece_coords[1] + dir_y
                    
                    if (not (new_x, new_y) in pieces
                        and new_x >= 0
                        and new_x < 8
                        and new_y >= 0
                        and new_y < 8):
                        self.coords(pieces[piece_coords], *_get_piece_coords(new_x, new_y))
                        pieces[(new_x, new_y)] = pieces[piece_coords]
                        del pieces[piece_coords]
                        if piece_coords in kings:
                            kings.remove(piece_coords)
                            kings.append((new_x, new_y))
                        
                        if (new_x, new_y) in enemy_pieces:
                            self.delete(enemy_pieces[new_x, new_y])
                            del enemy_pieces[(new_x, new_y)]
                            if (new_x, new_y) in enemy_kings:
                                enemy_kings.remove((new_x, new_y))

                        if new_y == (0 if self.active_player == 'blue' else 7) and not (new_x, new_y) in kings:
                            kings.append((new_x, new_y))
                            self.itemconfig(
                                pieces[new_x, new_y],
                                fill="cyan" if self.active_player == 'blue' else 'magenta')
                            
                        moved = True
                    if moved:
                        break
                if moved:
                    break
            piece_coords = random.choice(list(set(pieces.keys()) - pieces_tried))
            pieces_tried.add(piece_coords)

        self.blue_pieces = pieces if self.active_player == 'blue' else enemy_pieces
        self.red_pieces = pieces if self.active_player == 'red' else enemy_pieces
        self.active_player = 'red' if self.active_player == 'blue' else 'blue'
        if self.turn_number % 100 == 0:
            print("Blue Pieces: " + str(self.blue_pieces) + "\nRed Pieces: " + str(self.red_pieces)
                  + "\nBlue Kings: " + str(self.blue_kings) + "\nRed Kings: " + str(self.red_kings))
        self.turn_number += 1

        self.after(TURN_TIME, self.move_active_player)

    def show_message(self, msg):
        self.text_container = self.create_rectangle(0, 0, self.width, self.height, fill="#ffffff", width=0, stipple="gray50")
        self.victory_text = self.create_text(self.width/2, self.height/2, text=msg, font=("Arial", 36), justify="center")
        self.red_stat_text = self.create_text(
            self.width/2, self.height/2+125, text="Red Wins: " + str(self.red_wins), font=("Arial", 25), justify="center")
        self.blue_stat_text = self.create_text(
            self.width/2, self.height/2+100, text="Blue Wins: " + str(self.blue_wins), font=("Arial", 25), justify="center")
        self.after(max(TURN_TIME * 25, 500), self.hideText)

    
    def hideText(self):
        self.textDisplayed = False
        self.delete(self.victory_text)
        self.delete(self.red_stat_text)
        self.delete(self.blue_stat_text)
        self.delete(self.text_container)
        self.reset()


def _get_piece_coords(x, y):
    return (100*(x)+5, 100*(y)+5, 100*(x)+95, 100*(y)+95)
    

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Game Test")
    root.resizable(0,0)
    game = Game(root)
    root.mainloop()
