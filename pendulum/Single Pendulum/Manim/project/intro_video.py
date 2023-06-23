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



class Pendulum(SpaceScene):
    def construct(self):
        title = Tex(r"What are states?")
        basel = MathTex(r"q \>\> \dot{q} \>\> \ddot{q}")
        VGroup(title, basel).arrange(DOWN)
        self.add(
            title
        )
        transform_title = Tex("Imagine a Pendulum")
        transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(title, transform_title),
            LaggedStart(*[FadeOut(obj, shift=DOWN) for obj in basel]),
        )
        self.wait()
        origin = ORIGIN+2*UP + 3*LEFT
        pends = VGroup(*[Pendulum(3, pivot_point=origin)])
        self.add(pends)
        for p in pends:
            self.make_rigid_body(*p.bobs)
            verticalLine = DashedLine(start=origin, end=origin+2*DOWN, color=YELLOW_B)
            self.add(verticalLine)
            p.start_swinging()
        self.wait(10)

class PendulumText(scene):
    def construct(self):
        pass