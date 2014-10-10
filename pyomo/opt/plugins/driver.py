
import argparse
import os.path
import textwrap
import logging
import coopr.misc.coopr_parser
import coopr.opt

logger = logging.getLogger('coopr.solvers')


def setup_test_parser(parser):
    parser.add_argument('--csv-file', '--csv', action='store', dest='csv', default=None,
                        help='Save test results to this file in a CSV format')
    parser.add_argument("-d", "--debug", action="store_true", dest="debug", default=False,
                        help="Show debugging information and text generated during tests.")
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
                        help="Show verbose results output.")
    parser.add_argument("solver", metavar="SOLVER", default=None, nargs='*',
                        help="a solver name")

def test_exec(options):
    try:
        import coopr.data.pyomo
    except ImportError:
        print("Cannot test solvers.  The coopr.data.pyomo package is not installed!")
        return
    try:
        import yaml
    except ImportError:
        print("Cannot test solvers.  The pyyaml package is not installed!")
        return
    coopr.data.pyomo.test_solvers(options)
    
    
#
# Add a subparser for the coopr command
#
setup_test_parser(
    coopr.misc.coopr_parser.add_subparser('test-solvers',
        func=test_exec,
        help='Test Coopr solvers',
        description='This coopr subcommand is used to run tests on installed solvers.',
        epilog="""
This Coopr subcommand executes solvers on a variety of test problems that
are defined in the coopr.data.pyomo package.  The default behavior is to
test all available solvers, but the testing can be limited by explicitly
specifying the solvers that are tested.  For example:

  coopr test-solvers glpk cplex

will test only the glpk and cplex solvers.

The configuration file test_solvers.yml in coopr.data.pyomo defines a
series of test suites, each of which specifies a list of solvers that are
tested with a list of problems.  For each solver-problem pair, the Pyomo
problem is created and optimized with the the Coopr solver interface.
The optimization results are then analyzed using a function with the
same name as the test suite (found in the coopr/data/pyomo/plugins
directory).  These functions perform a sequence of checks that compare
the optimization results with baseline data, evaluate the solver return
status, and otherwise verify expected solver behavior.

The default summary is a simple table that describes the percentage of
checks that passed.  The '-v' option can be used to provide a summary
of all checks that failed, which is generally useful for evaluating
solvers.  The '-d' option provides additional detail about all checks
performed (both passed and failed checks).  Additionally, this option
prints information about the optimization process, such as the pyomo
command-line that was executed.

Note:  This capability requires the pyyaml Python package.""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
)

