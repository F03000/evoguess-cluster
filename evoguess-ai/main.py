from algorithm.impl import Elitism
from algorithm.module.mutation import Doer, OneBit
from algorithm.module.crossover import TwoPoint
from algorithm.module.selection import Roulette

from function.impl import RhoFunction
from function.module.solver import pysat
from function.module.measure import Propagations, Conflicts

from instance.impl import Instance
from instance.module.encoding import CNF
from instance.module.variables import Interval

from output.impl import OptimizeLogger
from typings.work_path import WorkPath
from executor.impl import ProcessExecutor

from core.impl import Optimize
from core.module.space import SearchSet
from core.module.sampling import Const
from core.module.limitation import WallTime
from core.module.comparator import MinValueMaxSize

if __name__ == '__main__':
    root_path = WorkPath('examples')
    data_path = root_path.to_path('data/mul')
    cnf_file = data_path.to_file('CvD.cnf')
    taboo_path = root_path.to_path('taboo/mul')
    taboo_file = taboo_path.to_file('CvD.tab')

    logs_path = root_path.to_path('logs', 'test')
    solution = Optimize(
        space=SearchSet(
            by_mask=[],
            variables=Interval(start=1, length=2984)
        ),
        executor=ProcessExecutor(max_workers=4),
        sampling=Const(size=1024, split_into=256),
        instance=Instance(
            encoding=CNF(from_file=cnf_file)
        ),
        function=RhoFunction(
            penalty_power=2 ** 10,
            measure=Conflicts(),
            solver=pysat.Glucose3()
        ),
        algorithm=Elitism(
            elites_count=2,
            population_size=6,
            mutation=Doer(taboo_file=taboo_file),
            crossover=TwoPoint(),
            selection=Roulette(),
            min_update_size=6
        ),
        comparator=MinValueMaxSize(),
        logger=OptimizeLogger(logs_path),
        limitation=WallTime(from_string='00:01:00'),
    ).launch()

    for point in solution:
        print(point)