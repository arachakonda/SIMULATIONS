from manim import *
import scipy
import numpy as np

config.frame_height = 18
config.frame_width = 32


class PhasePortraitIntro(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.3,
            zoomed_display_height=3,
            zoomed_display_width=3,
            zoomed_display_center=UR*5,
            image_frame_stroke_width=20,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
                },
            **kwargs
        )


    def construct(self):
        self.show_axis()
        self.wait()
        self.zoomed_frames()
        self.wait()

    def zoomed_frames(self):
        dot = Dot().shift(UL * 2)

        frame_text = Tex("$q,\dot{q}$", color=PURPLE, font_size=37)
        zoomed_camera_text = Text("", color=RED, font_size=37)

        self.add(dot)
        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        frame.move_to(dot)
        frame.set_color(PURPLE)
        zoomed_display_frame.set_color(RED)
        zoomed_display.shift(DOWN)

        zd_rect = BackgroundRectangle(zoomed_display, fill_opacity=0, buff=MED_SMALL_BUFF)
        self.add_foreground_mobject(zd_rect)

        unfold_camera = UpdateFromFunc(zd_rect, lambda rect: rect.replace(zoomed_display))

        frame_text.next_to(frame, DOWN)

        self.play(Create(frame),FadeIn(frame_text, shift=UP))
        self.activate_zooming()

        self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera)
        zoomed_camera_text.next_to(zoomed_display_frame, DOWN)
        
        
        # Scale in        x   y  z
        scale_factor = [1, 1, 0]
        self.play(
            frame.animate.scale(scale_factor),
            zoomed_display.animate.scale(scale_factor),
            FadeOut(zoomed_camera_text),
            FadeOut(frame_text)
        )
        self.wait()
        self.play(ScaleInPlace(zoomed_display, 2))
        self.wait()
        self.play(frame.animate.shift(5 * DOWN))
        self.wait()
        self.play(frame.animate.shift(5 * UL))
        self.wait()
        self.play(frame.animate.shift(5 * RIGHT))
        self.wait()
        self.play(FadeIn(zoomed_camera_text, shift=UP))
        self.wait()
        self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera, rate_func=lambda t: smooth(1 - t))
        self.play(Uncreate(zoomed_display_frame), FadeOut(frame))
        self.wait()



    def show_axis(self):
        plane_transformed = NumberPlane(x_range=[-20, 20, 1], y_range=[-20, 20, 1],axis_config={"include_numbers": True}).scale(1)
        xLabel = plane_transformed.get_x_axis_label(r"q", edge=RIGHT, direction=RIGHT).scale(0.7)
        yLabel = plane_transformed.get_y_axis_label(r"\dot{q}", edge=UP, direction=UP).scale(0.7)
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


class WhyLinearize1(Scene):
    def construct(self):
        self.show_axis()
        self.show_pendulum_background()
        self.move_bob_and_draw_curve()
        self.wait()

    def show_axis(self):
        plane_transformed = NumberPlane(x_range=[-20, 20, 1], y_range=[-20, 20, 1],axis_config={"include_numbers": True}).scale(1)
        xLabel = plane_transformed.get_x_axis_label(r"q", edge=RIGHT, direction=RIGHT).scale(0.7)
        yLabel = plane_transformed.get_y_axis_label(r"\dot{q}", edge=UP, direction=UP).scale(0.7)
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
        self.initial_value = 7.3*UP +0*RIGHT
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

class WhyLinearize2(Scene):
    def construct(self):
        self.show_axis()
        self.show_pendulum_background()
        self.move_bob_and_draw_curve()
        self.wait()

    def show_axis(self):
        plane_transformed = NumberPlane(x_range=[-20, 20, 1], y_range=[-20, 20, 1],axis_config={"include_numbers": True}).scale(1)
        xLabel = plane_transformed.get_x_axis_label(r"q", edge=RIGHT, direction=RIGHT).scale(0.7)
        yLabel = plane_transformed.get_y_axis_label(r"\dot{q}", edge=UP, direction=UP).scale(0.7)
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
        
class ZeroInput(Scene):
    def construct(self):
        ssequation = MathTex(r"\begin{bmatrix}\dot{q} \\ \ddot{q}\end{bmatrix}",r"=",
                                 r"\begin{bmatrix}\dot{q} \\ -\frac{g}{l}\sin{q}-\frac{b}{ml^2}\dot{q}\end{bmatrix}", r"+",
                                 r"\begin{bmatrix}0 \\ \frac{u}{ml^2}\end{bmatrix}").shift(ORIGIN)
        plane_transformed = NumberPlane(x_range=[-20, 20, 1], y_range=[-20, 20, 1],axis_config={"include_numbers": True}).scale(1)
        xLabel = plane_transformed.get_x_axis_label(r"q", edge=RIGHT, direction=RIGHT).scale(0.7)
        yLabel = plane_transformed.get_y_axis_label(r"\dot{q}", edge=UP, direction=UP).scale(0.7)
        self.add(VGroup(plane_transformed, xLabel, yLabel))
        background = Rectangle(color=WHITE,height=4,width=10).set_fill(BLACK,opacity=1)
        self.play(Create(background))
        self.play(Create(ssequation))
        self.wait(4)
        self.play(FadeOut(ssequation[3]),FadeOut(ssequation[4]))
        logroup = VGroup(ssequation[0],ssequation[1],ssequation[2])
        self.play(logroup.animate.move_to(ORIGIN))
        self.wait(5)