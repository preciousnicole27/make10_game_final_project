import tkinter as tk
import random
from tile import Tile
from PIL import Image, ImageTk

class Make10Game:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Make 10 Game")
        self.window.geometry("600x600")

        # Load image
        bg_image = Image.open("background orange.jpg")
        bg_photo = ImageTk.PhotoImage(bg_image)
        self.canvas = tk.Canvas(self.window, width=600, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=bg_photo, anchor="nw")
        self.canvas.bg_image = bg_photo  # Prevent garbage collection

        # Intro frame
        self.intro_frame = tk.Frame(self.canvas, bg="#FFF8DC")
        self.intro_frame_window = self.canvas.create_window(300, 300, window=self.intro_frame)
        self.show_intro()

    def show_intro(self):
        self.title_label = tk.Label(
            self.intro_frame, text="", font=("Impact", 30), fg="orange", bg="#FFF8DC"
        )
        self.title_label.pack(pady=30)

        self.animate_title("Make10")

        instructions = (
            "☆☆ Click two numbers\n"
            "🔟 If they add up to 10, you score!\n"
            "🟠 Tap again to deselect.\n"
            "\n💡 Try to reach the highest score!"
        )

        tk.Label(self.intro_frame, text=instructions, font=("Segoe UI Emoji", 12), bg="#FFF8DC").pack(pady=20)

        tk.Button(self.intro_frame, text="▶ Play", font=("Segoe UI Emoji", 14), command=self.start_game, bg="orange", fg="white").pack(pady=10)
        tk.Button(self.intro_frame, text="❌ Exit", font=("Segoe UI Emoji", 14), command=self.window.quit, bg="gray", fg="white").pack()

    def animate_title(self, text, index=0):
        if index <= len(text):
            self.title_label.config(text=text[:index])
            self.window.after(150, self.animate_title, text, index + 1)

    def start_game(self):
        self.canvas.delete(self.intro_frame_window)
        self.intro_frame.destroy()
        self.score = 0

        self.score_label = tk.Label(self.canvas, text="Score: 0", font=("Arial", 14), bg="white")
        self.score_label_window = self.canvas.create_window(300, 30, window=self.score_label)

        self.time_left = 60
        self.timer_label = tk.Label(self.canvas, text="Time: 60s", font=("Arial", 14), fg="red", bg="white")
        self.timer_label_window = self.canvas.create_window(300, 60, window=self.timer_label)
        self.update_timer()

        self.frame = tk.Frame(self.canvas, bg="", highlightthickness=0)
        self.frame_window = self.canvas.create_window(300, 320, window=self.frame)

        self.tiles = []
        self.selected_tiles = []
        self.generate_board()

    def update_timer(self):
        self.timer_label.config(text=f"Time: {self.time_left}s")
        if self.time_left > 0:
            self.time_left -= 1
            self.window.after(1000, self.update_timer)
        else:
            self.end_game()

    def end_game(self):
        for tile in self.tiles:
            tile.canvas.unbind("<Button-1>")
        self.frame.destroy()
        self.score_label.destroy()
        self.timer_label.destroy()

        end_label = tk.Label(self.canvas, text=f"⏱️ Time's up!\nYour Score: {self.score}", font=("Arial", 18), fg="red", bg="white")
        self.canvas.create_window(300, 300, window=end_label)

        tk.Button(self.canvas, text="🔁 Restart", font=("Arial", 14, "bold"), command=self.restart_game, bg="green", fg="white").pack(pady=5)
        tk.Button(self.canvas, text="❌ Exit", font=("Arial", 14, "bold"), command=self.window.quit, bg="gray", fg="white").pack()

    def restart_game(self):
        self.window.destroy()
        Make10Game().run()

    def generate_board(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.tiles = []
        self.selected_tiles = []

        num1 = random.randint(1, 9)
        num2 = 10 - num1
        valid_pair = [num1, num2]

        rest = []
        while len(rest) < 7:
            r = random.randint(1, 9)
            rest.append(r)

        numbers = valid_pair + rest
        random.shuffle(numbers)

        for i in range(3):
            for j in range(3):
                value = numbers[i * 3 + j]

                canvas = tk.Canvas(self.frame, width=80, height=80, bg=self.frame.cget("bg") or "white", highlightthickness=0)
                canvas.grid(row=i, column=j, padx=10, pady=10)

                canvas.create_oval(10, 10, 70, 70, fill="orange", outline="darkorange", width=4)
                canvas.create_text(40, 40, text=str(value), fill="white", font=("Arial", 18, "bold"))

                tile = Tile(value, canvas)
                self.tiles.append(tile)

                canvas.bind("<Button-1>", lambda e, t=tile: self.handle_click(t))

    def handle_click(self, tile):
        if tile.selected:
            tile.deselect()
            self.selected_tiles.remove(tile)
        else:
            tile.select()
            self.selected_tiles.append(tile)

        if len(self.selected_tiles) == 2:
            self.check_pair()

    def check_pair(self):
        val1 = self.selected_tiles[0].value
        val2 = self.selected_tiles[1].value

        if val1 + val2 == 10:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.generate_board()
        else:
            for tile in self.selected_tiles:
                tile.deselect()
        self.selected_tiles = []

    def run(self):
        self.window.mainloop()
