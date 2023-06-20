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

        transform_title = Tex("Imagine a Pendulum")
        transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(title, transform_title),
            LaggedStart(*[FadeOut(obj, shift=DOWN) for obj in basel]),
        )
        self.wait()

class PendulumExample(SpaceScene):
    def construct(self):
        pends = VGroup(*[Pendulum(3)])
        self.add(pends)
        for p in pends:
            self.make_rigid_body(*p.bobs)
            print(p.pivot_point)
            p.start_swinging()
        self.wait(10)