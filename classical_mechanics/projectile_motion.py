import math
from numbers import Real
from typing import Iterator

from matplotlib import pyplot as plt


class ProjectileMotion:
    """
    Source: https://codereview.stackexchange.com/questions/273223/python-class-to-calculate-different-variables-of-a-projectile-motion-with-angle
    
    This class calculates the movement of a projectile using its initial velocity
    and the angle at which it is thrown/shot. The initial height of the projectile
    is 0 by default but can be set by the user when creating an instance.

    The friction forces are neglected, thus the only formula used is the
    following: # △X = x0 + v_x⋅△t - a_x/2⋅△t^2  (and some of its variations)
    """
    g = 9.80665

    def __init__(self, speed0: Real = 1, angle0_degrees: Real = 45, y0: Real = 0) -> None:
        self.y0 = y0
        self.angle0 = math.radians(angle0_degrees)
        self.vx0, self.vy0 = self._get_v0(speed0)
        self.t_apex = self._get_apex_time()
        self.t1 = self._get_t1()

    def _get_v0(self, speed0: Real) -> tuple[float, float]:
        return (
            speed0 * math.cos(self.angle0),
            speed0 * math.sin(self.angle0),
        )

    def _get_t1(self) -> float:
        """
        t_total = time taken for the object to fall on the ground (y=0)
        t_total = (vy + sqrt(vy**2 + 2*y0*g)) / g
        """
        return (
             self.vy0 + math.sqrt(self.vy0**2 + 2*self.y0*self.g)
        ) / self.g

    def get_t(self, n_steps: int) -> Iterator[float]:
        """
        t_vect contains the time at n_steps, the first one being 0
            => need to divide by n_steps-1
        """
        for i in range(n_steps):
            yield self.t1 * i / (n_steps - 1)

    def x_for_t(self, t: float) -> float:
        return self.vx0 * t

    def y_for_t(self, t: float) -> float:
        return self.y0 + self.vy0*t - self.g/2*t**2

    def angle_for_t(self, t: float) -> float:
        return math.degrees(math.atan2(
            self.vy0 - t*self.g,
            self.vx0
        ))

    @property
    def x1(self) -> float:
        return self.x_for_t(self.t1)

    def _get_apex_time(self) -> float:
        """
        max_y attained when vy - g*t = 0 (when the velocity induced by gravity = vy)
        """
        return self.vy0 / self.g

    def desc(self, n_steps: int = 10) -> str:
        return (
            f'Curve over {n_steps} steps:'
            f'\n{"t":>5} {"x":>5} {"y":>5} {"angle°":>6}'
            f'\n'
        ) + '\n'.join(
            f'{t:>5.2f}'
            f' {self.x_for_t(t):>5.2f}'
            f' {self.y_for_t(t):>5.2f}'
            f' {self.angle_for_t(t):>6.1f}'
            for t in self.get_t(n_steps)
        )

    @classmethod
    def with_best_angle(cls, speed0: float, y0: float) -> 'ProjectileMotion':
        """
        https://www.whitman.edu/Documents/Academics/Mathematics/2016/Henelsmith.pdf
        equations 12 & 13
        h: initial height = y0
        v: initial velocity magnitude = speed
        Impact coefficients m = 0, a = 0
        arccotangent(x) = atan(1/x)
        """
        g = ProjectileMotion.g
        v = speed0
        angle = math.atan(
            1/math.sqrt(
                2*y0*g/v/v + 1
            )
        )
        return cls(
            speed0=speed0, angle0_degrees=math.degrees(angle), y0=y0,
        )


def graph(motion: ProjectileMotion) -> plt.Figure:
    fig, ax_x = plt.subplots()
    ax_t: plt.Axes = ax_x.twiny()
    ax_x.set_title('Projectile Motion')

    times = tuple(motion.get_t(n_steps=100))
    ax_x.plot(
        [motion.x_for_t(t) for t in times],
        [motion.y_for_t(t) for t in times],
    )

    ax_x.set_xlabel('x')
    ax_t.set_xlabel('t')
    ax_x.set_ylabel('y')
    ax_x.set_xlim(left=0, right=motion.x_for_t(motion.t1))
    ax_t.set_xlim(left=0, right=motion.t1)
    ax_x.set_ylim(bottom=0)

    return fig


def simple_test() -> None:
    motion = ProjectileMotion(speed0=10, angle0_degrees=30, y0=5)
    print(motion.desc())
    graph(motion)
    plt.show()


def optimisation_test() -> None:
    for y0 in range(1, 102, 10):
        best = ProjectileMotion.with_best_angle(y0=y0, speed0=y0)
        print(f'speed0={y0:3} y0={y0:3} x1={best.x1:6.1f} '
              f'angle0={math.degrees(best.angle0):.1f}')


if __name__ == '__main__':
    print('Simple projectile test:')
    simple_test()
    print()

    print('Angle optimisation test:')
    optimisation_test()
