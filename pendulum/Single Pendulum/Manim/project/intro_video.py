from  manim import *
from manim_physics import *
import numpy as np


class Introduction(Scene):
    def construct(self):
        title = Tex(r"What are states?")
        basel = MathTex(r"q \>\> \dot{q} \>\> \ddot{q}")
        VGroup(title, basel).arrange(DOWN)
        self.play(
            Write(title),
            FadeIn(basel, shift=DOWN),
        )
        self.wait()
        #self.play(FadeOut(basel, shift=UP))



class PendulumAnimation(SpaceScene):
    def construct(self):
        title = Tex(r"What are states?")
        basel = MathTex(r"q \>\> \dot{q} \>\> \ddot{q}")
        VGroup(title, basel).arrange(DOWN)
        self.add(
            title
        )
        transform_title = Tex("Consider the Simple Pendulum")
        transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(title, transform_title),
            LaggedStart(*[FadeOut(obj, shift=DOWN) for obj in basel])
        )
        self.wait()
        origin = ORIGIN+2*UP + 5*LEFT
        pends = VGroup(*[Pendulum(3, pivot_point=origin)])
        self.add(pends)
        for p in pends:
            self.make_rigid_body(*p.bobs)
            verticalLine = DashedLine(start=origin, end=origin+2*DOWN, color=YELLOW_B)
            self.add(verticalLine)
            p.start_swinging()
        self.wait(6.7)
        #pends[0].end_swinging()
        print(pends[0].bobs[-1].get_center())
        

class PendulumText(Scene):
    def construct(self):
        transform_title = Tex("Consider the Simple Pendulum")
        transform_title.to_corner(UP + LEFT)
        center= [-4.28670321, -0.91745358, 0.]
        origin= ORIGIN+2*UP + 5*LEFT
        tendon = Line(start=origin, end=center, color=WHITE)
        verticalLine = DashedLine(start=origin, end=origin+2*DOWN, color=YELLOW_B)
        bob = Circle(color=ORANGE, fill_opacity=1, radius=.25).shift(center)
        self.add(verticalLine)
        self.add(tendon)
        self.add(bob)
        self.add(transform_title)
        self.play(FadeOut(transform_title))

        path = VMobject()
        dot = Dot().shift(origin+0.7*DOWN).scale(0.5)
        path.set_points_as_corners([dot.get_center(), dot.get_center()])
        def update_path(path):
            previous_path = path.copy()
            previous_path.add_points_as_corners([dot.get_center()])
            path.become(previous_path)
        path.add_updater(update_path)
        self.add(path, dot)
        self.play(Rotating(dot, radians=0.25, about_point=origin, run_time=1))
        self.wait()

        qtex = MathTex(r"q").next_to(path,DOWN*0.5).scale(0.5)
        self.play(Write(qtex))
        self.wait(2)
        qdtex = MathTex(r"\dot{q}").next_to(qtex,DOWN*0.5).scale(0.5)
        self.play(Write(qdtex))
        self.wait(2)
        qddtex = MathTex(r"\ddot{q}").next_to(qdtex,DOWN*0.5).scale(0.5)
        self.play(Write(qddtex))

        states_title = Tex("These are called state variables").to_corner(UP+LEFT)
        self.play(Create(states_title))
        self.wait()
        self.play(FadeOut(states_title))

        states_defined_as = Tex("Dynamics of the Pendulum: ").to_corner(UP+LEFT)
        self.play(FadeIn(states_defined_as))
        self.wait()

        formulationtitle = Tex("via Newtonian/ Euler-Lagrange/ Hamiltonian formulation").to_corner(DOWN+RIGHT).scale(0.5)
        self.play(Create(formulationtitle))
        self.wait()
        
        qdeqtex = MathTex(r"ml^2 \ddot{q}=",r"u" 
                          , r"-", r"mgl\sin{q}", r"-",
                            r"b\dot{q}").next_to(verticalLine, 5*RIGHT).scale(0.7)
        self.play(Write(qdeqtex))
        self.wait()

        formtex = MathTex(r"\ddot{q}", r" =", r" f(q,\dot{q},u)").next_to(qdeqtex,DOWN)
        self.play(Write(formtex))
        self.wait()
        self.play(FadeOut(formtex))

        formfinaltex = MathTex(r"\dot{x}",r"=",r"f(x)",r"+",r"g(x)u").next_to(qdeqtex,DOWN)
        self.play(Write(formfinaltex))
        self.wait()
        xdtex = MathTex(r"\begin{bmatrix}\dot{q} \\ \ddot{q}\end{bmatrix}").next_to(formfinaltex[0],1.5*DOWN).scale(0.5)
        fxtex = MathTex(r"\begin{bmatrix}\dot{q} \\ -\frac{g}{l}\sin{q}-\frac{b}{ml^2}\dot{q}\end{bmatrix}").next_to(formfinaltex[2],DOWN).scale(0.5)
        gxutex = MathTex(r"\begin{bmatrix}0 \\ \frac{u}{ml^2}\end{bmatrix}").next_to(formfinaltex[4],DOWN).scale(0.5)
        framebox0 = SurroundingRectangle(formfinaltex[0], buff = .1)
        framebox2 = SurroundingRectangle(formfinaltex[2], buff = .1)
        framebox4 = SurroundingRectangle(formfinaltex[4], buff = .1)
        self.play(Create(framebox0))
        self.wait()
        self.play(Write(xdtex))

        self.play(Create(framebox2))
        self.wait()
        self.play(Write(fxtex))

        self.play(Create(framebox4))
        self.wait()
        self.play(Write(gxutex))

        self.wait(4)
        boxgroup = Group(framebox0, framebox2, framebox4)
        self.play(FadeOut(boxgroup))
        self.play(FadeOut(qdeqtex), LaggedStart(*[FadeOut(obj, shift=UP) for obj in formfinaltex]))
        formgroup = Group(xdtex,fxtex,gxutex)
        self.play(formgroup.animate.shift(UP+RIGHT).scale(1.5))
        formgroupeq = MathTex(r"=").next_to(xdtex, 0.2*RIGHT).scale(0.5)
        formgroupplus = MathTex(r"+").next_to(fxtex, RIGHT).scale(0.5)
        self.play(Create(formgroupeq), Create(formgroupplus))
        self.wait()
        
        lightsOutPendGroup = Group(tendon,verticalLine,bob,path,dot,qtex,qdtex,qddtex)
        self.play(FadeOut(lightsOutPendGroup), FadeOut(formulationtitle))

        initial_equation = Group(xdtex,fxtex,gxutex,formgroupeq,formgroupplus)
        final_equation = MathTex(r"\begin{bmatrix}\dot{q} \\ \ddot{q}\end{bmatrix}",r"=",
                                 r"\begin{bmatrix}\dot{q} \\ -\frac{g}{l}\sin{q}-\frac{b}{ml^2}\dot{q}\end{bmatrix}", r"+",
                                 r"\begin{bmatrix}0 \\ \frac{u}{ml^2}\end{bmatrix}").to_edge(UP)

        self.play(FadeOut(states_defined_as), Transform(initial_equation,final_equation))
        self.wait(4)

class PendulumLinearize(Scene):
    def construct(self):
        ssequation = MathTex(r"\begin{bmatrix}\dot{q} \\ \ddot{q}\end{bmatrix}",r"=",
                                 r"\begin{bmatrix}\dot{q} \\ -\frac{g}{l}\sin{q}-\frac{b}{ml^2}\dot{q}\end{bmatrix}", r"+",
                                 r"\begin{bmatrix}0 \\ \frac{u}{ml^2}\end{bmatrix}").to_edge(UP)
        self.add(ssequation)
        
        self.play(ssequation.animate.shift(DOWN).scale(0.7))

        linearizeTitle = Tex("Let us ","Linearize...","!!").to_edge(UP)
        self.play(Create(linearizeTitle))
        self.wait(2)
        frameoval = SurroundingRectangle(linearizeTitle[1],corner_radius=0.3,buff=0.1)
        self.play(Create(frameoval))
        linearizationTitle= Tex("Linearization")
        linearizationQuestion = Tex("??")
        linearizationTitle.to_edge(UP)
        linearizationQuestion.next_to(linearizeTitle,RIGHT)
        self.play(Transform(linearizeTitle[2],linearizationQuestion))
        self.wait()
        self.play(Transform(linearizeTitle[1],linearizationTitle),FadeOut(frameoval),LaggedStart(*[FadeOut(linearizeTitle[0],shift=LEFT), FadeOut(linearizeTitle[2],shift=RIGHT)]))
        self.wait()

        lin_proc_1 = Tex("We linearize around equilibrium where system evolves with little dependence on states").next_to(ssequation, DOWN).scale(0.7)
        self.play(FadeIn(lin_proc_1))
        self.wait()
        self.play(FadeOut(lin_proc_1))

        lin_proc_2 = Tex(r"Setting $\dot{X} = 0$").next_to(ssequation, DOWN).scale(0.7)
        self.play(FadeIn(lin_proc_2))

        lin_proc_3 = MathTex(r"\begin{bmatrix}\dot{q} \\ \ddot{q}\end{bmatrix}",r"=",r"0").next_to(lin_proc_2,DOWN).scale(0.7)
        self.play(Write(lin_proc_3))
        
        lin_proc_4 = Tex(r"$q^* = 0, n\pi; \> u^*=0\>\>\>$where $n \in \mathbb{I}$").next_to(lin_proc_3,DOWN).scale(0.7)
        self.play(Write(lin_proc_4))

        lin_proc_5 = Tex("are the operating points").next_to(lin_proc_4,DOWN).scale(0.7)
        self.play(FadeIn(lin_proc_5))
        self.wait()
        lin_fade_g1 = Group(lin_proc_4, lin_proc_5)
        self.play(FadeOut(lin_fade_g1))

        lin_proc_6 = MathTex(r"\dot{x} = {f}(x,u) \approx {f}(x^*,u^*) + \begin{bmatrix} \frac{\partial f}{\partial x}\end{bmatrix}_{x=x^*,u=u^*} (x - x^*) + \begin{bmatrix} \frac {\partial f}{\partial u}\end{bmatrix}_{x=x^*,u=u^*} (u - u^*)").next_to(lin_proc_3,DOWN).scale(0.7)
        self.play(Write(lin_proc_6))
        self.wait()
        self.play(FadeOut(lin_proc_6))

        linearized = MathTex(r"\begin{bmatrix}\dot{q} \\ \ddot{q}\end{bmatrix}",r"=",
                                 r"\begin{bmatrix}0 & 1\\ -\frac{g}{l} & -\frac{b}{ml^2}\end{bmatrix}",r"\begin{bmatrix}q \\ \dot{q}\end{bmatrix}", r"+",
                                 r"u\begin{bmatrix}0 \\ \frac{1}{ml^2}\end{bmatrix}").next_to(lin_proc_3,DOWN)
        self.play(Write(linearized))
        self.wait(4)

        self.play(FadeOut(lin_proc_2),FadeOut(lin_proc_3),*[FadeOut(obj,shift=DOWN) for obj in ssequation])

        
        self.play(linearized.animate.shift(ORIGIN+3*UP))
        self.wait(2)
        linearizedor = Tex("(or)").next_to(linearized,DOWN).scale(0.6)
        linearizedpi = MathTex(r"\begin{bmatrix}\dot{q} \\ \ddot{q}\end{bmatrix}",r"=",
                                 r"\begin{bmatrix}0 & 1\\ \frac{g}{l} & -\frac{b}{ml^2}\end{bmatrix}",r"\begin{bmatrix}q \\ \dot{q}\end{bmatrix}", r"+",
                                 r"u\begin{bmatrix}0 \\ \frac{1}{ml^2}\end{bmatrix}").next_to(linearizedor,DOWN)

        self.play(FadeIn(linearizedor))
        self.play(Write(linearizedpi))
        self.wait(2)
        self.play(FadeOut(linearizeTitle[1]), FadeOut(linearized),FadeOut(linearizedor),FadeOut(linearizedpi))
        self.wait()


class WhyLinearize(Scene):
    def construct(self):
        # resolution_fa = 24
        # self.set_camera_orientation(phi=75 * DEGREES, theta=-30 * DEGREES)

        # def param_diff(q, qd):
        #     x = q
        #     y = qd
        #     g = 9.8132
        #     b = 0.1
        #     m = 1
        #     l = 3
        #     z = -(g/l)*np.sin(q) - (b/(m*l^2))*qd
        #     return np.array([x, y, z])

        # param_plane = Surface(
        #     param_diff,
        #     resolution=(resolution_fa, resolution_fa),
        #     v_range=[-5, +5],
        #     u_range=[-5, +5]
        # )

        # param_plane.scale(0.5, about_point=ORIGIN)
        # param_plane.set_style(fill_opacity=1,stroke_color=GREEN)
        # param_plane.set_fill_by_checkerboard(ORANGE, BLUE, opacity=0.5)
        # axes = ThreeDAxes()
        # self.add(axes,param_plane)

        # self.begin_ambient_camera_rotation(rate=1)
        # self.wait(5)
        # self.stop_ambient_camera_rotation()
        # self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES)
        # self.wait()

        plane = NumberPlane(x_range=[-10, 10, 1], y_range=[-10, 10, 1], axis_config={"include_numbers": True}).scale(1)
        xLabel = plane.get_x_axis_label(r"\theta", edge=RIGHT, direction=RIGHT).scale(0.7)
        yLabel = plane.get_y_axis_label(r"\dot{\theta}", edge=UP, direction=UP).scale(0.7)
        g = 9.8132
        b = 0.1
        m = 1
        l = 3
        func = lambda pos: (-(g/l)*np.sin(pos[0]) - (b/(m*l^2))*pos[1])*UP + pos[1]*RIGHT
        vectorField = ArrowVectorField(func, x_range=[-10, 10, 0.5]).scale(1)

        self.play(FadeIn(VGroup(plane, xLabel, yLabel)))
        self.play(*[GrowArrow(vec) for vec in vectorField], run_time=5)
        self.wait(3)

class WhyLinearize2(ThreeDScene):
    def construct(self):
        resolution_fa = 24
        self.set_camera_orientation(phi=75 * DEGREES, theta=-30 * DEGREES)

        def param_diff(q, qd):
            x = q
            y = qd
            g = 9.8132
            b = 0.1
            m = 1
            l = 3
            z = np.arcsin(((m*l**2)*qd +b*q)/(-m*g*l))
            return np.array([x, y, z])

        param_plane = Surface(
            param_diff,
            resolution=(resolution_fa, resolution_fa),
            v_range=[-1, +1],
            u_range=[-1, +1]
        )

        param_plane.scale(0.5, about_point=ORIGIN)
        param_plane.set_style(fill_opacity=1,stroke_color=GREEN)
        param_plane.set_fill_by_checkerboard(ORANGE, BLUE, opacity=0.5)
        axes = ThreeDAxes()
        self.add(axes,param_plane)

        self.begin_ambient_camera_rotation(rate=1)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES)
        self.wait()
