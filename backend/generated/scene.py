from manim import *

class BinarySearchAnimation(Scene):
    def construct(self):
        # 1. Introduction
        title = Text("Binary Search Explained", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        intro_text = Text("Searching for a target value in a sorted array.", font_size=30).next_to(title, DOWN)
        self.play(Write(intro_text))
        self.wait(2)

        # 2. Setup the sorted array
        data = [5, 12, 18, 25, 33, 40, 47, 51, 60, 68, 75, 82, 90, 95]
        target_value = 60
        num_elements = len(data)

        # Create boxes for array elements
        array_elements = VGroup()
        for i, val in enumerate(data):
            rect = Rectangle(width=1.0, height=1.0, color=BLUE, fill_opacity=0.2)
            num = Text(str(val), font_size=24)
            element = VGroup(rect, num)
            array_elements.add(element)

        array_elements.arrange(RIGHT, buff=0.1)
        array_elements.next_to(intro_text, DOWN, buff=1.0)
        array_elements.shift(LEFT * (array_elements.width / 2 - 1.0)) # Center the array more

        # Create index labels
        index_labels = VGroup()
        for i in range(num_elements):
            idx_text = Text(str(i), font_size=20, color=GREY)
            idx_text.next_to(array_elements[i], UP, buff=0.1)
            index_labels.add(idx_text)

        self.play(FadeIn(array_elements, shift=DOWN), FadeIn(index_labels, shift=DOWN))
        self.wait(1)

        target_text = Text(f"Target: {target_value}", font_size=36, color=YELLOW)
        target_text.next_to(array_elements, DOWN, buff=1.0)
        self.play(Write(target_text))
        self.wait(1)

        # 3. Binary Search Algorithm Visualization
        low_pointer = 0
        high_pointer = num_elements - 1
        found_index = -1

        low_label = Text("Low (0)", font_size=24, color=GREEN)
        high_label = Text(f"High ({num_elements - 1})", font_size=24, color=RED)
        mid_label = Text("Mid", font_size=24, color=PURPLE)

        # Initial positions
        low_label.next_to(array_elements[low_pointer], DOWN, buff=0.5)
        high_label.next_to(array_elements[high_pointer], DOWN, buff=0.5)

        self.play(FadeIn(low_label, shift=UP), FadeIn(high_label, shift=UP))
        self.wait(1)

        steps_explanation = VGroup()

        iteration = 1
        while low_pointer <= high_pointer:
            current_low_index = low_pointer
            current_high_index = high_pointer

            # Update pointer positions visually (if moved)
            if iteration > 1:
                self.play(
                    low_label.animate.next_to(array_elements[low_pointer], DOWN, buff=0.5),
                    high_label.animate.next_to(array_elements[high_pointer], DOWN, buff=0.5),
                    run_time=0.7
                )
            else:
                self.wait(1)

            mid_pointer = (low_pointer + high_pointer) // 2
            mid_value = data[mid_pointer]

            # Highlight current search range
            current_range_rects = []
            for i in range(low_pointer, high_pointer + 1):
                rect = array_elements[i][0].copy().set_fill(YELLOW, opacity=0.1).set_stroke(YELLOW, width=2)
                current_range_rects.append(rect)
            current_range_group = VGroup(*current_range_rects)
            self.play(Create(current_range_group))


            step_text = Text(f"Iteration {iteration}: Low={current_low_index}, High={current_high_index}", font_size=24).to_edge(LEFT).shift(UP*1.5)
            steps_explanation.add(step_text)
            self.play(Write(step_text))

            mid_label.set_text(f"Mid ({mid_pointer})")
            mid_label.next_to(array_elements[mid_pointer], UP, buff=0.5)

            self.play(FadeIn(mid_label, shift=DOWN))
            self.play(
                array_elements[mid_pointer][0].animate.set_fill(PURPLE, opacity=0.5),
                array_elements[mid_pointer][1].animate.set_color(WHITE)
            )
            self.wait(1)

            mid_comparison_text = Text(f"Mid value ({mid_value}) vs Target ({target_value})", font_size=24).next_to(step_text, DOWN, buff=0.5)
            self.play(Write(mid_comparison_text))

            if mid_value == target_value:
                found_index = mid_pointer
                result_text = Text(f"Mid value {mid_value} == Target {target_value}", color=GREEN, font_size=28).next_to(mid_comparison_text, DOWN, buff=0.5)
                self.play(Write(result_text))
                self.play(
                    array_elements[mid_pointer][0].animate.set_fill(GREEN, opacity=0.7).set_stroke(GREEN, width=4),
                    array_elements[mid_pointer][1].animate.set_color(WHITE),
                    FadeOut(current_range_group)
                )
                steps_explanation.add(result_text)
                break
            elif mid_value < target_value:
                result_text = Text(f"Mid value {mid_value} < Target {target_value}. Search Right Half.", color=ORANGE, font_size=28).next_to(mid_comparison_text, DOWN, buff=0.5)
                self.play(Write(result_text))
                self.play(array_elements[mid_pointer][0].animate.set_fill(BLUE, opacity=0.2).set_stroke(BLUE, width=2),
                          array_elements[mid_pointer][1].animate.set_color(WHITE))
                low_pointer = mid_pointer + 1
                self.play(FadeOut(current_range_group))
            else: # mid_value > target_value
                result_text = Text(f"Mid value {mid_value} > Target {target_value}. Search Left Half.", color=ORANGE, font_size=28).next_to(mid_comparison_text, DOWN, buff=0.5)
                self.play(Write(result_text))
                self.play(array_elements[mid_pointer][0].animate.set_fill(BLUE, opacity=0.2).set_stroke(BLUE, width=2),
                          array_elements[mid_pointer][1].animate.set_color(WHITE))
                high_pointer = mid_pointer - 1
                self.play(FadeOut(current_range_group))

            steps_explanation.add(mid_comparison_text, result_text)
            self.remove(mid_comparison_text, result_text)
            self.wait(1.5)
            self.play(FadeOut(mid_label))
            iteration += 1

        # 4. Final Result
        self.play(FadeOut(low_label, high_label, mid_label))
        self.wait(1)
        self.play(FadeOut(steps_explanation), FadeOut(target_text))

        final_result_text = Text("")
        if found_index != -1:
            final_result_text = Text(f"Target {target_value} found at index {found_index}!", font_size=40, color=GREEN)
            final_result_text.move_to(title.get_center())
            self.play(Transform(title, final_result_text))
        else:
            final_result_text = Text(f"Target {target_value} not found in the array.", font_size=40, color=RED)
            final_result_text.move_to(title.get_center())
            self.play(Transform(title, final_result_text))

        self.wait(3)
        self.play(FadeOut(title, intro_text, array_elements, index_labels))
        self.wait(1)