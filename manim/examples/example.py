from manim import *


class ExampleScene(Scene):
    def construct(self):
        circle = Circle()

        self.play(Create(circle))
        self.wait(1)