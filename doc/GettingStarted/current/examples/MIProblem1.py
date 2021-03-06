from pyomo.opt.blackbox import MixedIntOptProblem

# @prob:
class MixedIntProblem1(MixedIntOptProblem):

    def __init__(self):
        MixedIntOptProblem.__init__(self)
        self.real_lower=[0.0]*4
        self.real_upper=[2.0]*4
        self.int_lower=[-2]*3
        self.int_upper=[0]*3
        self.nreal=4
        self.nint=3
        self.nbinary=2

    def function_value(self, point):
        self.validate(point)
        return sum((x-1)**2 for x in self.reals) + \
               sum((y+1)**2 for y in self.ints) + \
               sum(b for b in self.bits)
# @:prob

