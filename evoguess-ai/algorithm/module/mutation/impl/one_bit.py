from ..mutation import Mutation

from instance.module.variables import Backdoor


class OneBit(Mutation):
    slug = 'mutation:one-bit'

    def __init__(self, taboo_file: str = None):
        super().__init__()
        self.dict = {}
        self.count = 0
        with open(taboo_file) as f:
            for line in f:  # read rest of lines
                array = [int(x) for x in line.split()]
                if array[0] not in self.dict:
                    self.dict[array[0]] = [array[1:]]
                elif array[1:] not in self.dict[array[0]]:
                    self.dict[array[0]].append(array[1:])

    def mutate(self, backdoor: Backdoor) -> Backdoor:
        
        count = 0
        while True:
            mask = backdoor.get_mask()
            i = self.random_state.randint(0, len(mask))
            bad_indicator = True
            if i in self.dict:
                for arrays in self.dict[i]:
                    bad_indicator = True
                    for index in arrays:
                        if mask[index] == 0:
                            bad_indicator = False
                            break
                    if bad_indicator:
                        break
            else:
                bad_indicator = False

            if not bad_indicator:
                mask[i] = not mask[i]
                return backdoor.get_copy(mask)
            elif count > 100:
                raise StopIteration('Impossible to find next backdoor')
            else:
                print('We did it')


__all__ = [
    'OneBit'
]
