from manim import *
import numpy as np
import scipy


config.frame_height = 18
config.frame_width = 32


from sympy import symbols, Eq, diff



class Gradients(Scene):
    def construct(self):
        self.show_axis()
        # self.show_pendulum_background()
        # self.move_bob_and_draw_curve()
        self.wait()

    def show_axis(self):
        plane_transformed = NumberPlane(x_range=[-20, 20, 1], y_range=[-20, 20, 1],axis_config={"include_numbers": True}).scale(1)
        xLabel = plane_transformed.get_x_axis_label(r"q", edge=RIGHT, direction=RIGHT).scale(0.7)
        yLabel = plane_transformed.get_y_axis_label(r"\dot{q}", edge=UP, direction=UP).scale(0.7)
        
        #plot a circle centered at the origin
        circle = Circle(radius=3, color=RED)

        circle = Ellipse(width=8.0, height=4.0, color=RED)

        #make equation of the circle using sympy and plot it

        # Define the variables and the radius
        q, q_dot = symbols('q q_dot')
        r = symbols('r', real=True, positive=True)

        # Equation of the circle
        circle_eq = Eq(q**2/4**2 + q_dot**2/2**2, 1)
        state = np.array([q,q_dot])
        gradient = self.calculate_gradient(circle_eq, state)

        self.add(VGroup(plane_transformed, xLabel, yLabel))
        self.play(FadeIn(circle))
        #calculate the gradient of the circle at the origin
        #create n points on the circle and plot gradients at those points
        arrows = []
        n=32
        for i in range(n):
            point = circle.point_from_proportion(i/n)
            eval_grad_q = np.float64(gradient[0].subs({q:point[0], q_dot:point[1]}))
            eval_grad_q_dot = np.float64(gradient[1].subs({q:point[0], q_dot:point[1]}))
            gradient_vector = np.array([eval_grad_q, eval_grad_q_dot, 0])
            normalized_vector = gradient_vector / np.linalg.norm(gradient_vector)
            # print(eval_grad_q, eval_grad_q_dot)
            end_point = np.array([point[0] + 1 * normalized_vector[0], point[1] + 1 * normalized_vector[1], 0])
            # print(end_point)
            # print(2*point)
            #arrow without padding
            grad = Arrow(start=point,end= end_point, color=YELLOW_B, buff=0, max_tip_length_to_length_ratio=0.2)
            arrows.append(grad)
            self.play(GrowArrow(grad, run_time=0.1))
           
        self.wait(3)

    def calculate_gradient(self, equation, point):
        #calculate the gradient of the circle at the point
        #plot the gradient
               # Differentiate with respect to q and q_dot
        grad_q = diff(equation.lhs, point[0])
        grad_q_dot = diff(equation.lhs, point[1])

        return np.array([grad_q, grad_q_dot])