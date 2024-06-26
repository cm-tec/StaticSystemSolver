from vector import vector


class Node:

    def __init__(self, id, x=0, y=0, support=0):
        if support < 0:
            raise SupportMustBeGreaterZero()
        if support > 8:
            raise SupportMustBeLessNine()

        self.id = id

        self.x = x
        self.y = y

        self.dof_x = id * 3 - 2
        self.dof_y = id * 3 - 1
        self.dof_phi = id * 3

        self.support = support

    def get_coordinate(self):
        return vector(self.x, self.y)

    def get_dofs(self):
        return vector(self.dof_x, self.dof_y, self.dof_phi)

    def get_support(self):
        return self.support

    def get_restrained_dofs(self):
        if self.support == 0:
            return vector()
        elif self.support == 1:
            return vector(self.dof_x)
        elif self.support == 2:
            return vector(self.dof_y)
        elif self.support == 3:
            return vector(self.dof_phi)
        elif self.support == 4:
            return vector(self.dof_x, self.dof_y)
        elif self.support == 5:
            return vector(self.dof_x, self.dof_phi)
        elif self.support == 6:
            return vector(self.dof_y, self.dof_phi)
        elif self.support == 7:
            return vector(self.dof_x, self.dof_y, self.dof_phi)


class SupportMustBeGreaterZero(Exception):
    pass


class SupportMustBeLessNine(Exception):
    pass
