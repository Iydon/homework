import collections


def split(data, number=3, left=1, right=0):
    '''Split `data` into batch with length `left+number+right`.

    Argument:
        - data: iterator
        - number: int, group length
        - left: int, length of left overlap elements
        - right: int, length of right overlap elements
    '''
    values = iter(data)
    length = left + number + right
    this = collections.deque(maxlen=length)
    for _ in range(right):
        try:
            this.append(next(values))
        except StopIteration:
            yield this
            return
    for ith, value in enumerate(values):
        this.append(value)
        if (ith+1)%(number) == 0:
            yield tuple(this)
            for _ in range(len(this)-left-right):
                this.popleft()
    yield tuple(this)


if __name__ == '__main__':
    values = range(16)
    bs = split(values, number=3, left=2, right=1)
    for b in bs:
        print(b)
