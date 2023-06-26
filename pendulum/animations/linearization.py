from manim import *
import scipy
import numpy as np

config.frame_height = 18
config.frame_width = 32
class WhyLinearize(Scene):
    def construct(self):
        self.show_axis()
        self.move_dot_and_draw_curve()
        self.wait()
        # self.initial_value = 2.3*UP + 3.6*RIGHT
        # self.final_value = self.initial_value
        # self.move_dot_and_draw_curve()
        # self.wait()

    def show_axis(self):
        plane = NumberPlane(x_range=[-10, 10, 1], y_range=[-10, 10, 1], axis_config={"include_numbers": True}).scale(1)
        plane_transformed = NumberPlane(x_range=[-20, 20, 1], y_range=[-20, 20, 1],axis_config={"include_numbers": True}).scale(1)
        xLabel = plane_transformed.get_x_axis_label(r"\theta", edge=RIGHT, direction=RIGHT).scale(0.7)
        yLabel = plane_transformed.get_y_axis_label(r"\dot{\theta}", edge=UP, direction=UP).scale(0.7)
        g = 9.8132
        b = 0.1
        m = 1
        l = 3
        mu = b/m*l**2
        func = lambda pos: (-(g/l)*np.sin(pos[0]) - (mu)*pos[1])*UP + pos[1]*RIGHT #up =Y unit vec and down=X unit vec
        vectorField = ArrowVectorField(func, x_range=[-10, 10, 0.5], y_range=[-10,10,0.5]).scale(1)
        vectorField_transform = ArrowVectorField(func,x_range=[-20, 20, 1], y_range=[-20,20,1]).scale(1)

        self.play(FadeIn(VGroup(plane_transformed, xLabel, yLabel)))
        self.play(*[GrowArrow(vec) for vec in vectorField_transform], run_time=5)
        self.wait(3)

    def move_dot_and_draw_curve(self):
        self.initial_value = 7.3*UP + 0*RIGHT
        self.final_value = self.initial_value
        dot = Dot(radius=0.08, color=YELLOW)
        dot.move_to(self.initial_value)
        self.t_offset = 0
        def fx(t,y):
            y = np.zeros_like(self.final_value,dtype=float)
            g = 9.8132
            b = 0.1
            m = 1
            l = 3
            mu = b/m*l**2
            y[1] = (-(g/l)*np.sin(self.final_value[0]) - mu*self.final_value[1])
            y[0] = self.final_value[1]
            y[2] = 0
            return y


        def go_around_circle(mob, dt):
            self.t_offset += (dt)
            #print(self.t_offset)
            # g = 9.8132
            # b = 0.1
            # m = 1
            # l = 3
            # mu = b/m*l**2
            # self.final_value[1] += (-(g/l)*np.sin(self.final_value[0]) - mu*self.final_value[1])*dt
            # self.final_value[0] += self.final_value[1]*dt
            sol=scipy.integrate.solve_ivp(fx,(self.t_offset-dt, self.t_offset),self.final_value)
            # print(sol.y[:,-1])
            self.final_value = sol.y[:,-1]
            mob.move_to(self.final_value)

        curve = VGroup()
        curve.add(Line(self.initial_value,self.initial_value))
        def get_curve():
            last_line = curve[-1]
            new_line = Line(last_line.get_end(),self.final_value, color=YELLOW_D)
            curve.add(new_line)

            return curve

        dot.add_updater(go_around_circle).update(dt=0.0000001)

        
        trajectory_line = always_redraw(get_curve)

        self.add(dot)
        self.add(trajectory_line)
        self.wait(20)

        dot.remove_updater(go_around_circle)

class WhyLinearize2(Scene):
    def construct(self):
        self.show_axis()
        self.move_dot_and_draw_curve()
        self.wait()

    def show_axis(self):
        plane_transformed = NumberPlane(x_range=[-20, 20, 1], y_range=[-20, 20, 1],axis_config={"include_numbers": True}).scale(1)
        xLabel = plane_transformed.get_x_axis_label(r"\theta", edge=RIGHT, direction=RIGHT).scale(0.7)
        yLabel = plane_transformed.get_y_axis_label(r"\dot{\theta}", edge=UP, direction=UP).scale(0.7)
        g = 9.8132
        b = 0.1
        m = 1
        l = 3
        mu = b/m*l**2
        func = lambda pos: (-(g/l)*np.sin(pos[0]) - (mu)*pos[1])*UP + pos[1]*RIGHT #up =Y unit vec and down=X unit vec
        vectorField = ArrowVectorField(func, x_range=[-10, 10, 0.5], y_range=[-10,10,0.5]).scale(1)
        vectorField_transform = ArrowVectorField(func,x_range=[-20, 20, 1], y_range=[-20,20,1]).scale(1)

        self.add(VGroup(plane_transformed, xLabel, yLabel))
        self.play(*[GrowArrow(vec) for vec in vectorField_transform], run_time=1)
        self.wait(3)


    def move_dot_and_draw_curve(self):
        self.initial_value = 7.3*UP + 3.6*RIGHT
        self.final_value = self.initial_value
        dot = Dot(radius=0.08, color=YELLOW)
        dot.move_to(self.initial_value)
        self.t_offset = 0
        def fx(t,y):
            y = np.zeros_like(self.final_value,dtype=float)
            g = 9.8132
            b = 0.1
            m = 1
            l = 3
            mu = b/m*l**2
            y[1] = (-(g/l)*np.sin(self.final_value[0]) - mu*self.final_value[1])
            y[0] = self.final_value[1]
            y[2] = 0
            return y


        def go_around_circle(mob, dt):
            self.t_offset += (dt)
            sol=scipy.integrate.solve_ivp(fx,(self.t_offset-dt, self.t_offset),self.final_value)
            # print(sol.y[:,-1])
            self.final_value = sol.y[:,-1]
            mob.move_to(self.final_value)

        curve = VGroup()
        curve.add(Line(self.initial_value,self.initial_value))
        def get_curve():
            last_line = curve[-1]
            new_line = Line(last_line.get_end(),self.final_value, color=YELLOW_D)
            curve.add(new_line)

            return curve

        dot.add_updater(go_around_circle).update(dt=0.0000001)

        
        trajectory_line = always_redraw(get_curve)

        self.add(dot)
        self.add(trajectory_line)
        self.wait(20)

        dot.remove_updater(go_around_circle)


class WhyLinearize3(Scene):
    def construct(self):
        self.show_axis()
        self.show_pendulum_background()
        self.move_bob_and_draw_curve()
        self.wait()

    def show_axis(self):
        plane_transformed = NumberPlane(x_range=[-20, 20, 1], y_range=[-20, 20, 1],axis_config={"include_numbers": True}).scale(1)
        xLabel = plane_transformed.get_x_axis_label(r"\theta", edge=RIGHT, direction=RIGHT).scale(0.7)
        yLabel = plane_transformed.get_y_axis_label(r"\dot{\theta}", edge=UP, direction=UP).scale(0.7)
        g = 9.8132
        b = 0.1
        m = 1
        l = 3
        mu = b/m*l**2
        func = lambda pos: (-(g/l)*np.sin(pos[0]) - (mu)*pos[1])*UP + pos[1]*RIGHT #up =Y unit vec and down=X unit vec
        vectorField_transform = ArrowVectorField(func,x_range=[-20, 20, 1], y_range=[-20,20,1]).scale(1)

        self.add(VGroup(plane_transformed, xLabel, yLabel))
        self.play(*[GrowArrow(vec) for vec in vectorField_transform], run_time=1)
        self.wait(3)

    def show_pendulum_background(self):
        self.pend_bg = Rectangle(color=YELLOW, width=12, height=12).move_to(LEFT*7).set_fill(BLACK,opacity = 1)
        self.play(FadeIn(self.pend_bg))
        l = 3
        self.pivot_point = self.pend_bg.get_center()+UP*1
        self.circle = Circle(radius=l).move_to(self.pivot_point)


    def move_bob_and_draw_curve(self):
        orbit = self.circle
        bias = -PI/2
        self.initial_value = 7.3*UP + 3.6*RIGHT
        self.final_value = self.initial_value
        bob = Dot(radius=0.08, color=YELLOW)
        bob.move_to(orbit.point_at_angle(0+bias))
        self.t_offset = 0
        def fx(t,y):
            y = np.zeros_like(self.final_value,dtype=float)
            g = 9.8132
            b = 0.1
            m = 1
            l = 3
            mu = b/m*l**2
            y[1] = (-(g/l)*np.sin(self.final_value[0]) - mu*self.final_value[1])
            y[0] = self.final_value[1]
            y[2] = 0
            return y


        def go_around_circle(mob, dt):
            self.t_offset += (dt)
            sol=scipy.integrate.solve_ivp(fx,(self.t_offset-dt, self.t_offset),self.final_value)
            # print(sol.y[:,-1])
            self.final_value = sol.y[:,-1]
            mob.move_to(orbit.point_at_angle(self.final_value[0]+bias))

        def get_tendon_to_bob():
            return Line(self.pivot_point, bob.get_center(), color=BLUE)

        curve = VGroup()
        curve.add(Line(self.initial_value,self.initial_value))
        def get_curve():
            last_line = curve[-1]
            new_line = Line(last_line.get_end(),self.final_value, color=YELLOW_D)
            curve.add(new_line)

            return curve

        bob.add_updater(go_around_circle).update(dt=0.0000001)

        tendon_to_bob = always_redraw(get_tendon_to_bob)
        trajectory_line = always_redraw(get_curve)

        self.add(bob)
        self.add(tendon_to_bob)
        self.add(trajectory_line)
        self.wait(20)

        bob.remove_updater(go_around_circle)
        
