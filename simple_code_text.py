import math


def crafting_inequality(coded_alphabet):
    """Crafting inequality. Returns bool."""
    return math.fsum([2 ** (-len(item)) for item in coded_alphabet]) <= 1


def entropy(list_probability):
    """Энтропия"""
    l = [num * math.log2(num) for num in list_probability if num != 0]
    res = math.fsum(l)
    return -res


def average_codeword(coded_alphabet):
    """Средняя длина слова"""
    return sum([len(elem) for elem in coded_alphabet]) / len(coded_alphabet)


def redundancy(list_probability):
    """Избыточность"""
    return 1 - entropy(list_probability) / math.log2(len(list_probability))


def hafman(list_probability, list_alphabet):
    """Алгоритм Хаффмана"""

    class BNode:
        def __init__(self, data, symbol, right=None, left=None):
            self.symbol = symbol
            self.data = data
            self.blood = None
            self.left = left
            self.right = right

        def __lt__(self, other):
            return self.data < other.data

    tree = [BNode(node, symbol) for node, symbol in zip(list_probability, list_alphabet)]
    m0 = len(list_probability)

    # Created tree
    while m0 > 1:
        tree_node = BNode(tree[-1].data + tree[-2].data, None, tree[-1], tree[-2])
        tree[-1].blood = tree_node
        tree[-2].blood = tree_node

        tree = tree[:-2]
        tree.append(tree_node)

        tree.sort(reverse=True)

        m0 -= 1

    # Depth-first walk
    res = {}
    s = ""

    def depth(node, st):
        if node.right is not None:
            st += "1"
            depth(node.right, st)
            st = st[:-1]
        if node.left is not None:
            st += "0"
            depth(node.left, st)
        else:
            res[node.symbol] = st

    depth(tree[0], s)

    return res


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


def code_text(text, dict_coded):
    coded = ""
    for i in range(len(text)):
        coded += dict_coded[text[i]]

    return coded


def decode_text(text, dict_coded):
    values = [len(elem) for elem in dict_coded.values()]
    min_of_list = min(values)
    max_of_list = max(values)
    position = 0
    quantum = min_of_list
    decoded = ""

    while len(text) > position:
        substring = text[position:position+quantum]
        if substring in dict_coded.values():
            decoded += get_key(dict_coded, substring)
            position += quantum
            quantum = min_of_list
        else:
            quantum += 1
            if quantum > max_of_list:
                raise ValueError

    return decoded
