import collections


class Batches:
    def __init__(self, number=3, left=1, right=0):
        '''
        Argument
            - number: int, group length
            - left: int, length of left overlap elements
            - right: int, length of right overlap elements
        '''
        assert number>=left+right, 'number<left+right'
        self.number = number
        self.left = left
        self.right = right

    def split(self, data):
        '''Split `data` into batch with length `left+number+right`.

        Argument:
            - data: iterator
        '''
        values = iter(data)
        length = self.left + self.number + self.right
        this = collections.deque(maxlen=length)
        for _ in range(self.right):
            try:
                this.append(next(values))
            except StopIteration:
                yield this
                return
        for ith, value in enumerate(values):
            this.append(value)
            if (ith+1)%(self.number) == 0:
                yield tuple(this)
                for _ in range(len(this)-self.left-self.right):
                    this.popleft()
        yield tuple(this)

    def concat(self, data, key=None):
        '''Concat `data` with left overlap `left` and right overlap `lap`

        Argument:
            - data: iterator
            - left: int, length of left overlap elements
            - right: int, length of right overlap elements
            - key: callable, how to treat overlap part
        '''
        key = key or (lambda x, y: (x+y)/2)
        data = tuple(data)
        number = len(data)
        length = sum(map(len, data)) - (number-1)*(self.left+self.right)
        result = [None] * length
        ith = 0
        for jth in range(number):
            index = slice(
                {0: None, number-1: self.left}.get(jth, self.left),
                {0: self.number, number-1: None}.get(jth, -self.right),
            )
            for d in data[jth][index]:
                result[ith] = d
                ith += 1
        return result


if __name__ == '__main__':
    values = range(16)
    batch = Batches(number=3, left=2, right=1)
    raw = batch.concat(batch.split(values))
    assert tuple(raw)==tuple(values)
