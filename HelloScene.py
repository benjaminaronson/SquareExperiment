from manim import *
import random

class CircleScene(Scene):
    def construct(self):
        # Create a circle
        self.camera.background_color = ManimColor(rgb_to_color([0.1, 0.1, 0.1]))
        square = Square(4)
        square.shift(LEFT *2)

        animations = []
        animations.append(Create(square, run_time=1.5))
        
        # get an array with the locations of the corners of the square
        corners = square.get_vertices()
        
        # create a tracker for the number of intersections and total squares generated
        intersection_count = 0
        display_intersection_count = Text(str(intersection_count), font_size=60)
        display_intersection_count.shift(RIGHT * 2.5, UP * 0.5)
        animations.append(Write(display_intersection_count, run_time=1.5))
        display_total_count = Text("0", font_size=60)
        display_total_count.shift(RIGHT * 2.5, DOWN * 0.5)
        animations.append(Write(display_total_count, run_time=1.5))

        # create a tracker for the total proportion of squares with intersections
        # put it off the screen until there's a proportion to display
        proportion_tracker = 0
        display_proportion_tracker = Text(str(proportion_tracker))
        display_proportion_tracker.shift(UP*30)
        self.add(display_proportion_tracker)

        # create an equals sign
        equals_sign = Text("=", font_size=60)
        equals_sign.shift(RIGHT*3.75)
        animations.append(Write(equals_sign, run_time=1.5))
        

        # create a line for our fraction
        fraction_line = Line([0, 0, 0], [1.5, 0, 0])
        fraction_line.shift(RIGHT * 1.75)
        animations.append(Create(fraction_line, run_time=1.5))

        self.play(AnimationGroup(*animations, lag_ratio=0))
        self.wait()

        # Generate a ton of random squares
        for i in range(1, 1001):
            # clear the previous counts
            self.remove(display_total_count, display_intersection_count, display_proportion_tracker)
            # get the edges of the square and put them in an array
            edges = [
            Line(corners[0], corners[1]),
            Line(corners[1], corners[2]),
            Line(corners[2], corners[3]),
            Line(corners[3], corners[0]),
        ]
            copy_of_edges = edges # to be used later

            # choose the edge for the first point of our line segment
            side_1 = random.choice(edges)
            edges.remove(side_1)
            # choose the edge for the second point from the set without our first edge choice
            side_2 = random.choice(edges)

            # choose random points on these edges
            point1a = side_1.point_from_proportion(random.random())
            point2a = side_2.point_from_proportion(random.random())
            
            # place visible dots at these points
            dot1a = Dot(point1a, radius=0.05, color=YELLOW)
            dot2a = Dot(point2a, radius=0.05, color=YELLOW)
            self.add(dot1a, dot2a)
            
            
            # choose the edge for the first point of our second line segment
            side_1 = random.choice(copy_of_edges)
            copy_of_edges.remove(side_1)
            # choose the edge for the second point from the set without our first edge choice
            side_2 = random.choice(copy_of_edges)

            # choose random points on these edges
            point1b = side_1.point_from_proportion(random.random())
            point2b = side_2.point_from_proportion(random.random())
            
            # place visible dots at these points
            dot1b = Dot(point1b, radius=0.05, color=ORANGE)
            dot2b = Dot(point2b, radius=0.05, color=ORANGE)
            self.add(dot1b, dot2b)

            # create the line segments
            line1 = Line(point1a, point2a)
            line2 = Line(point1b, point2b)

            # check if the intersection point of our lines lies inside the square
            intersection_point = line_intersection([point1a, point2a], [point1b, point2b])
            if intersection_point[0] > -4 and intersection_point[0] < 0 and intersection_point[1] > -2 and intersection_point[1] < 2:
                # if they intersect, color them yellow and orange
                line1 = Line(point1a, point2a, color=YELLOW)
                line2 = Line(point1b, point2b, color=ORANGE)
                # and update the counter
                intersection_count += 1
            
            self.add(line1, line2)

            # display the updated counts
            display_intersection_count = Text(str(intersection_count), font_size=60)
            display_intersection_count.shift(RIGHT * 2.5, UP * 0.5)
            display_total_count = Text(str(i), font_size=60)
            display_total_count.shift(RIGHT * 2.5, DOWN * 0.5)

            # update the proportion and display it
            proportion_tracker = round(intersection_count / i, 2)
            display_proportion_tracker = Text(str(proportion_tracker), font_size=65)
            display_proportion_tracker.shift(RIGHT*5)
            self.add(display_proportion_tracker)

            self.add(display_total_count, display_intersection_count)

            self.wait(0.02)
            if i != 1001:
                self.remove(dot1a, dot2a, dot1b, dot2b, line1, line2)

        self.wait()
