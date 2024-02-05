from pyglet.window import Window
from pyglet.app import run
from pyglet.shapes import Rectangle
import random
import pyglet

def hex_to_rgb(hex_color):
    return int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16), 255

class Renderer(Window):
    def __init__(self, bar_count):
        super().__init__(1300, 600, "Merge Sort Visualization")

        self.bar_count = bar_count
        self.bar_width = 30
        self.bar_gap = 10

        # Create a list of heights
        heights_range = list(range(60, 500, 10))
        self.bar_heights = random.sample(heights_range * (self.bar_count // len(heights_range) + 1), self.bar_count)
        self.frames = self.generate_frames(self.bar_heights.copy())
        self.current_frame = None
        self.sorting_complete = False  

    def on_draw(self):
        self.clear()
        left_padding = 25
        right_padding = 25

        for i, height in enumerate(self.bar_heights):
            color = hex_to_rgb('#01A6BA')  

            if self.current_frame and self.current_frame[0] <= i < self.current_frame[1]:
                progress = (i - self.current_frame[0]) / (self.current_frame[1] - self.current_frame[0])
                color = hex_to_rgb('#DEB887')

            x = left_padding + i * (self.bar_width + self.bar_gap) + right_padding
            y = 0
            bar = Rectangle(x, y, self.bar_width, height, color=color)
            bar.draw()

        
        if self.sorting_complete:
            for i, height in enumerate(self.bar_heights):
                x = left_padding + i * (self.bar_width + self.bar_gap) + right_padding
                y = 0
                bar = Rectangle(x, y, self.bar_width, height, color=hex_to_rgb('#01A6BA'))
                bar.draw()

    def generate_frames(self, arr):
        frames = []
        self.merge_sort_frames(arr, 0, len(arr), frames)
        return frames

    def merge_sort_frames(self, arr, start, end, frames):
        if end - start > 1:
            mid = (start + end) // 2
            self.merge_sort_frames(arr, start, mid, frames)
            self.merge_sort_frames(arr, mid, end, frames)

            merged_array = self.merge(arr[start:mid], arr[mid:end])
            frames.append((start, end, merged_array.copy()))

            for i in range(len(merged_array)):
                arr[start + i] = merged_array[i]

    def merge(self, left, right):
        merged = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    def update(self, dt):
        if self.frames:
            start, end, merged_array = self.frames.pop(0)
            self.bar_heights[start:end] = merged_array
            self.current_frame = (start, end)
        else:
            self.sorting_complete = True


new_bar_count = 30
renderer = Renderer(new_bar_count)

pyglet.clock.schedule_interval(renderer.update, 0.05)
run()
