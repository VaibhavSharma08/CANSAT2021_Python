import sys
from itertools import chain
import datetime

print(
    datetime.datetime.fromtimestamp(
        int("1284105682")
    ).strftime('%Y-%m-%d %H:%M:%S')
)

# TO FIX : Insert mein shift hote hue last element starting mein aa jaata hai

class largeList(object):
    def __init__(self, mylist=[]):
        self.maxSize = int(10000000000 / 4)
        self.src = [[]]
        self.extend(mylist)

    def __iter__(self):
        return chain(*self.src)

    def __getitem__(self, idx):
        return self.src[int(idx / self.maxSize)][idx % self.maxSize]

    def __setitem__(self, idx, item):
        self.src[int(idx / self.maxSize)][idx % self.maxSize] = item
        # expand set/getitem to support negative indexing.

    def append(self, item):
        if len(self.src[-1]) < self.maxSize:
            self.src[-1].append(item)
        else:
            self.src.append([item])

    def extend(self, items):
        remainder = self.maxSize - len(self.src[-1])
        self.src[-1].extend(items[:remainder])
        for i in range(0, len(items[remainder:]), self.maxSize):
            self.src.append(items[remainder:][i:i + self.maxSize])

    def __len__(self):
        return sum(len(l) for l in self.src)

    def __str__(self):
        size = self.__len__()
        if size >= 8:
            first, last = [], []
            for i, ele in enumerate(self.__iter__()):
                if i < 3:
                    first.append(ele)
                if i >= size - 3:
                    last.append(ele)
            return str(first)[:-1] + ', ..., ' + str(last)[1:]
        return str(list(self.__iter__()))

    def pop(self, idx):
        listidx = int(idx / self.maxSize)
        itempopped = self.src[listidx].pop(idx % self.maxSize)
        for i in range(listidx, len(self.src) - 1):
            self.src[i].append(self.src[i + 1].pop(0))
        if not self.src[-1]:
            del self.src[-1]
        return itempopped

    def remove(self, item):
        for i, ele in enumerate(self.__iter__()):
            if ele == item:
                self.pop(i)
                break

    def insert(self, idx, item):
        listidx = int(idx / self.maxSize)
        itemtoshift = self.src[listidx].pop(-1)
        self.src[listidx].insert(idx % self.maxSize, item)
        for i in range(listidx + 1, len(self.src) - 1):
            itemremoved = self.src[i].pop(-1)
            self.src[i].insert(0, itemtoshift)
            itemtoshift = itemremoved
        if len(self.src[-1]) < self.maxSize:
            self.src[-1].insert(0, itemtoshift)
        else:
            self.src.append([self.src[-1].pop(-1)])
            self.src[-2].insert(0, itemtoshift)

    def index(self, item):
        for i, ele in enumerate(self.__iter__()):
            if ele == item:
                return i
        return -1
