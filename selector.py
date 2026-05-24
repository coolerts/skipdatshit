import tkinter as tk
import json
import os

CONFIG_FILE = "config.json"

class RegionSelector:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-fullscreen', True)
        self.root.configure(background='black')
        self.root.attributes("-topmost", True)
        self.root.config(cursor="cross")

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.rect = None
        self.start_x = None
        self.start_y = None

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        print("выдели кнопку скипа рекламы, если сделал что то не так то ескейп кликай")

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='yellow', width=3)

    def on_move_press(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x, end_y = (event.x, event.y)
        
        center_x = min(self.start_x, end_x) + abs(self.start_x - end_x) // 2
        center_y = min(self.start_y, end_y) + abs(self.start_y - end_y) // 2

        config = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                try:
                    config = json.load(f)
                except json.JSONDecodeError:
                    pass

        config["click_x"] = center_x
        config["click_y"] = center_y

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)

        print(f"выбрал: X={center_x}, Y={center_y}")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RegionSelector(root)
    root.mainloop()
