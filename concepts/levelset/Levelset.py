from manim import *

class LevelCurve(ThreeDScene):
    def construct(self):
        resolution_fa = 24
        #control the frame_center and zoom to keep the graph in the screen.
        #the frame center is the point in the camera frame that will remain in the center of the screen.
        self.set_camera_orientation(phi=75 * DEGREES, theta=-30 * DEGREES, zoom=0.3, frame_center=[0,0,7])

        def param_gauss(u, v):
            x = u
            y = v
            z = x**2 + y**2
            return np.array([x, y, z])

        gauss_plane = Surface(
            param_gauss,
            resolution=(resolution_fa, resolution_fa),
            v_range=[-3.2, +3.2],
            u_range=[-3.2, +3.2]
        )

        gauss_plane.scale(1, about_point=ORIGIN)
        gauss_plane.set_style(fill_opacity=1,stroke_color=GREEN)
        gauss_plane.set_fill_by_checkerboard(ORANGE, BLUE, opacity=0.5)
        axes = ThreeDAxes(x_range=[-4, 4], y_range=[-4, 4], z_range=[0, 16], x_length=16, y_length=16, z_length=16, axis_config={"include_numbers": True})
        self.add(axes)
        circle=Circle(radius=3).shift(np.array([0,0,param_gauss(2,2)[2]]))
        r = 3
        circle = ParametricFunction(lambda t: np.array([r*np.cos(t), r*np.sin(t), r**2]), t_range=[0, 2*PI], color=PURE_BLUE)
        
        self.begin_3dillusion_camera_rotation(rate=1)
        self.play(Create(gauss_plane))
        self.play(Create(circle))
        self.wait(PI/2)
        self.stop_3dillusion_camera_rotation()

class RadialBound(ThreeDScene):
    def construct(self):
        resolution_fa = 24
        #control the frame_center and zoom to keep the graph in the screen.
        #the frame center is the point in the camera frame that will remain in the center of the screen.
        self.set_camera_orientation(phi=75 * DEGREES, theta=-30 * DEGREES, zoom=0.3, frame_center=[0,0,7])

        def param_gauss(u, v):
            x = u
            y = v
            z = x**2 + y**2
            return np.array([x, y, z])

        gauss_plane = Surface(
            param_gauss,
            resolution=(resolution_fa, resolution_fa),
            v_range=[-3.2, +3.2],
            u_range=[-3.2, +3.2]
        )

        gauss_plane.scale(1, about_point=ORIGIN)
        gauss_plane.set_style(fill_opacity=1,stroke_color=GREEN)
        gauss_plane.set_fill_by_checkerboard(ORANGE, BLUE, opacity=0.5)
        axes = ThreeDAxes(x_range=[-4, 4], y_range=[-4, 4], z_range=[0, 16], x_length=16, y_length=16, z_length=16, axis_config={"include_numbers": True})
        self.add(axes)
        circle=Circle(radius=3).shift(np.array([0,0,param_gauss(2,2)[2]]))

        r = 1
        circle = ParametricFunction(lambda t: np.array([r*np.cos(t), r*np.sin(t), r**2]), t_range=[0, 2*PI], color=PURE_BLUE)
        self.begin_3dillusion_camera_rotation(rate=0.3)
        self.play(Create(gauss_plane))
        self.play(Create(circle))
        n = 40
        for i in range(1,n):
            if i<22:
                circleRB = ParametricFunction(lambda t: np.array([(r+i*0.1)*np.cos(t), (r+i*0.1)*np.sin(t), (r+i*0.1)**2]), t_range=[0, 2*PI], color=PURPLE_E)
            else:
                circleRB = ParametricFunction(lambda t: np.array([(r+i*0.1)*np.cos(t), (r+i*0.1)*np.sin(t), (r+i*0.1)**2]), t_range=[0, 2*PI], color=BLUE_A)
            self.play(Create(circleRB), run_time=0.1)
        self.wait(PI/2)
        self.stop_3dillusion_camera_rotation()