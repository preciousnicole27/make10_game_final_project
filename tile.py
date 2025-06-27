class Tile:
    def __init__(self, value, canvas):
        self.value = value
        self.canvas = canvas
        self.selected = False
        self.oval_id = None
        self.text_id = None
        self.draw_tile()

    def draw_tile(self):
        # Clear the canvas first
        self.canvas.delete("all")
        # Store IDs so we can modify them later
        self.oval_id = self.canvas.create_oval(10, 10, 70, 70,
                                               fill="orange",
                                               outline="darkorange",
                                               width=4)
        self.text_id = self.canvas.create_text(40, 40,
                                               text=str(self.value),
                                               fill="white",
                                               font=("Arial", 18, "bold"))

    def select(self):
        self.selected = True
        # Add a highlight by changing the border color
        self.canvas.itemconfig(self.oval_id, outline="violet", width=6)

    def deselect(self):
        self.selected = False
        # Reset the original style
        self.canvas.itemconfig(self.oval_id, outline="darkorange", width=4)
