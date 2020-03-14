from tkinter import *
from PIL import Image, ImageTk
    
def OnButtonClick(button_id):
    new_piece_name = None
    if button_id == 1:
        new_piece_name = 'Queen'

    elif button_id == 2:
        new_piece_name = 'Rook'

    elif button_id == 3:
        new_piece_name = 'Bishop'
    
    elif button_id == 4:
        new_piece_name = 'Knight'

    print(new_piece_name)
    exit()

def init_Window(root, colour):

    ####################
    # Create a button for the queen.

    queen = Image.open(f'./{colour}_queen.png')
    queen = queen.resize((100, 100))
    queen_render = ImageTk.PhotoImage(queen)

    b1 = Button(root, command = lambda : OnButtonClick(1))
    b1.config(image = queen_render, width = "110", height = "100")
    b1.place(x = 20, y = 20)
    
    #################### 
    # Create a button for the rook.

    rook = Image.open(f'./{colour}_rook.png')
    rook = rook.resize((100, 100))
    rook_render = ImageTk.PhotoImage(rook)

    b2 = Button(root, command = lambda : OnButtonClick(2))
    b2.config(image = rook_render, width = "110", height = "100")
    b2.place(x = 140, y = 20)

    #################### 
    # Create a button for the bishop.

    bishop = Image.open(f'./{colour}_bishop.png')
    bishop = bishop.resize((100, 100))
    bishop_render = ImageTk.PhotoImage(bishop)

    b3 = Button(root, command = lambda : OnButtonClick(3))
    b3.config(image = bishop_render, width = "110", height = "100")
    b3.place(x = 260, y = 20)

    #################### 
    # Create a button for the knight.

    knight = Image.open(f'./{colour}_knight.png')
    knight = knight.resize((100, 100))
    knight_render = ImageTk.PhotoImage(knight)

    b4 = Button(root, command = lambda : OnButtonClick(4))
    b4.config(image = knight_render, width = "110", height = "100")
    b4.place(x = 380, y = 20)

    root.mainloop()

    #################### 

def main():
    colour = sys.argv[1]
    
    root = Tk()
    root.geometry("500x140")

    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    root.title('Choose a piece to promote to.')
    init_Window(root, colour)

    root.mainloop()

if __name__ == "__main__":
    main()