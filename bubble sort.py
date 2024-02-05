from pyglet.window import Window
from pyglet.app import run
from pyglet.shapes import Rectangle
import random
import pyglet

def hex_to_rgb(hex_color):
    return int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16), 255

class Renderer(Window):
    def __init__(self, bar_count):
        super().__init__(1300, 600, "Bubble Sort Visualization")

        self.bar_count = bar_count
        self.bar_width = 30
        self.bar_gap = 10

        heights_range = list(range(60, 500, 10))
        self.bar_heights = random.sample(heights_range * (self.bar_count // len(heights_range) + 1), self.bar_count)
        self.bar_color = hex_to_rgb('#01A6BA')

        self.current_comparison = [0, 1]
        self.sorted_bars = set()
        self.sorting_complete = False

    def on_draw(self):
        self.clear()

        left_padding = 25
        right_padding = 25

        for i, height in enumerate(self.bar_heights):
            color = self.bar_color
            if i in self.current_comparison and all(x > 0 for x in self.current_comparison):
                color = hex_to_rgb('#DEB887')
            else :
                color = hex_to_rgb('#01A6BA')  

            x = left_padding + i * (self.bar_width + self.bar_gap) + right_padding
            y = 0
            bar = Rectangle(x, y, self.bar_width, height, color=color)
            bar.draw()

    def bubble_sort(self):
        i, j = self.current_comparison
        if self.bar_heights[i] > self.bar_heights[j]:
            self.bar_heights[i], self.bar_heights[j] = self.bar_heights[j], self.bar_heights[i]

        if j < self.bar_count - 1:
            self.current_comparison = [j, j + 1]
        else:
            self.current_comparison = [0, 1]
            self.bar_count -= 1

            if all(self.bar_heights[i] <= self.bar_heights[i + 1] for i in range(self.bar_count-1)):
                self.sorting_complete = True
                self.sorted_bars = set(range(self.bar_count))  
                
            
        

if __name__ == "__main__":
    bar_count = 30
    renderer = Renderer(bar_count)

    def update(dt):
        renderer.bubble_sort()

    pyglet.clock.schedule_interval(update, 0.05)
    run()

