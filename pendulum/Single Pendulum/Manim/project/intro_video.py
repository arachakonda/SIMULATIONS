from  manim import *
from manim_physics import *
from numpy import angle


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
        fxtex = MathTex(r"-\begin{bmatrix}-\dot{q} \\ -\frac{g}{l}\sin{q}-\frac{b}{ml^2}\dot{q}\end{bmatrix}").next_to(formfinaltex[2],DOWN).scale(0.5)
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


        