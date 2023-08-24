from manim import *

class LevelCurve(ThreeDScene):
    def construct(self):
        resolution_fa = 24
        self.set_camera_orientation(phi=75 * DEGREES, theta=-30 * DEGREES, zoom=0.1)

        def param_gauss(u, v):
            x = u
            y = v
            z = x**2 + y**2
            return np.array([x, y, z])

        gauss_plane = Surface(
            param_gauss,
            resolution=(resolution_fa, resolution_fa),
            v_range=[-4, +4],
            u_range=[-4, +4]
        )

        gauss_plane.scale(1, about_point=ORIGIN)
        gauss_plane.set_style(fill_opacity=1,stroke_color=GREEN)
        gauss_plane.set_fill_by_checkerboard(ORANGE, BLUE, opacity=0.5)
        axes = ThreeDAxes()
        self.add(axes,gauss_plane)
        circle=Circle(radius=3).shift(np.array([0,0,param_gauss(2,2)[2]]))
        r = 3
        circle = ParametricFunction(lambda t: np.array([r*np.cos(t), r*np.sin(t), r**2]), t_range=[0, 2*PI], color=RED)
        self.play(Create(circle))
        self.begin_3dillusion_camera_rotation(rate=1)
        self.wait(PI/2)
        self.stop_3dillusion_camera_rotation()
