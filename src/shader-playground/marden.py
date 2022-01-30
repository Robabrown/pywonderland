import vispy
from vispy import gloo, app
from vispy.io import imsave


vispy.set_log_level("error")


vertex = """
#version 130

in vec2 position;

void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

fragment = """
#version 130

uniform vec3      iResolution;           // viewport resolution (in pixels)
uniform float     iTime;                 // shader playback time (in seconds)
uniform float     iTimeDelta;            // render time (in seconds)
uniform vec4      iMouse;                // mouse pixel coords
uniform vec4      iDate;                 // (year, month, day, time in seconds)
uniform float     iSampleRate;           // sound sample rate (i.e., 44100)
uniform sampler2D iChannel0;             // input channel. XX = 2D/Cube
uniform sampler2D iChannel1;             // input channel. XX = 2D/Cube
uniform sampler2D iChannel2;             // input channel. XX = 2D/Cube
uniform sampler2D iChannel3;             // input channel. XX = 2D/Cube
uniform vec3      iChannelResolution[4]; // channel resolution (in pixels)
uniform float     iChannelTime[4];       // channel playback time (in sec)

out vec4 fragColor;

%s

void main()
{
    mainImage(fragColor, gl_FragCoord.xy);
}
"""


class Marden(app.Canvas):

    def __init__(self, size=(800, 480), title="Marden's theorem",
                 glsl_code="./glsl/marden.frag"):
        app.Canvas.__init__(self,
                            keys="interactive",
                            size=size,
                            title=title)

        with open(glsl_code, "r") as f:
            code = f.read()

        self.program = gloo.Program(vertex, fragment % code)
        self.program["position"] = [
            (-1, -1), (-1, 1), (1, 1), (-1, -1), (1, 1), (1, -1)
        ]
        self.program["iTime"] = 0.
        self.program["iResolution"] = (self.physical_size[0], self.physical_size[1], 0)
        self.timer = app.Timer('auto', connect=self.on_timer, start=False)

    def on_draw(self, event):
        self.program.draw()

    def on_timer(self, event):
        self.program["iTime"] = event.elapsed
        self.update()

    def on_resize(self, event):
        self.program["iResolution"] = (event.size[0], event.size[1], 0)
        gloo.set_viewport(0, 0, event.size[0], event.size[1])

    def save_screenshot(self):
        img = gloo.util._screenshot((0, 0, self.size[0], self.size[1]))
        imsave("capture.png", img)

    def on_key_press(self, event):
        if event.key == "Enter":
            self.save_screenshot()

    def run(self):
        self.timer.start()
        self.show(run=True)


if __name__ == "__main__":
    anim = Marden()
    anim.run()
