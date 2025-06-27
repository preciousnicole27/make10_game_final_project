class Tile:
    def __init__(self, value, canvas):
        self.value = value
        self.canvas = canvas  
        self.selected = False

    def select(self):
        self.selected = True
        self.canvas.itemconfig(1, outline="blue", width=6)  # Circle border

    def deselect(self):
        self.selected = False
        self.canvas.itemconfig(1, outline="darkorange", width=4)  # Reset border
