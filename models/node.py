from matplotlib import markers
from models.settings import Settings
from models.support import Support
from new_utilities import plot_force, plot_moment
from supports import pinned_support, rollerSupport


class Node:
    def __init__(
        self,
        id,
        x,
        y,
        support,
        F_x=0,
        F_y=0,
        M_y=0,
        angle=0,
    ):
        self.id = id
        self.x = x
        self.y = y

        self.F_x = F_x
        self.F_y = F_y
        self.M_y = M_y

        self.displacement_x = 0
        self.displacement_y = 0
        self.displacement_phi = 0

        self.R_F_x = 0
        self.R_F_y = 0
        self.R_M_y = 0

        self.dof_x = id * 3 - 2
        self.dof_y = id * 3 - 1
        self.dof_phi = id * 3

        if support in Support:
            self.support = support
        else:
            raise ValueError("Invalid support type")

        self.angle = angle  # Additional property for support angle

    @property
    def coordinate(self):
        return (self.x, self.y)

    @property
    def displacement_coordinate(self):
        return (
            self.x + Settings.scalingFactor * self.displacement_x,
            self.y - Settings.scalingFactor * self.displacement_y,
        )

    @property
    def degrees_of_freedom(self):
        return [self.dof_x, self.dof_y, self.dof_phi]

    @property
    def restrained_degrees_of_freedom(self):
        if self.support == Support.PINNED:
            return [self.dof_x, self.dof_y]
        elif self.support == Support.ROLLER:
            return [self.dof_y]
        elif self.support == Support.CLAMPED:
            return [self.dof_x, self.dof_y, self.dof_phi]
        elif self.support == Support.MOMENT_JOINT:
            return []
        else:
            return []

    @property
    def F(self):
        return (self.F_x, self.F_y, self.M_y)

    def set_displacements(self, displacement_x, displacement_y, displacement_phi):
        self.displacement_x = displacement_x
        self.displacement_y = displacement_y
        self.displacement_phi = displacement_phi

    def plot(
        self,
        ax,
        show_displacements=False,
        show_reaction_forces=True,
        show_forces=True,
    ):
        x, y = self.displacement_coordinate if show_displacements else self.coordinate

        supportIcon = None
        markerContent = None

        if self.support == Support.PINNED:
            supportIcon = pinned_support()
            markerContent = "o"
        elif self.support == Support.ROLLER:
            supportIcon = rollerSupport()
            markerContent = "o"
        elif self.support == Support.CLAMPED:
            supportIcon = pinned_support()
            markerContent = "s"
        elif self.support == Support.MOMENT_JOINT:
            markerContent = "o"
        else:
            markerContent = "s"

        marker = markers.MarkerStyle(marker=markerContent)

        # marker._transform = marker.get_transform().rotate(nodeAngle)

        ax.annotate(
            self.id,
            (x, y),
            zorder=10,
            ha="center",
            va="center",
            size="8",
        )

        ax.scatter(
            x,
            y,
            c="whitesmoke",
            s=200,
            edgecolors="k",
            zorder=9,
            marker=marker,
        )
        if supportIcon:
            ax.plot(
                x,
                y,
                marker=supportIcon,
                color="k",
                markerfacecolor="lightsteelblue",
                markersize=50,
            )

        if show_forces:
            if self.F_x != 0:
                plot_force(ax=ax, coords=(x, y), text=self.F_x)

            if self.F_y != 0:
                plot_force(ax=ax, coords=(x, y), text=self.F_y, angle=-90)

            if self.M_y != 0:
                plot_moment(ax=ax, coords=(x, y), value=self.M_y)

        if show_reaction_forces:
            if round(self.R_F_x, 3) != 0:
                plot_force(ax=ax, coords=(x, y), text=round(self.R_F_x, 3))

            if round(self.R_F_y, 3) != 0:
                plot_force(ax=ax, coords=(x, y), text=round(self.R_F_y, 3), angle=-90)

            if round(self.R_M_y, 3) != 0:
                plot_moment(ax=ax, coords=(x, y), value=round(self.R_M_y, 3))
