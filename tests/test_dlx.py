from sudoku.solve import dlx


def test_node():
    n1 = dlx.Node(1)
    n2 = dlx.Node(2)
    n1.right = n2
    n2.left = n1


def test_insert():
    n1 = dlx.Node(1)
    n2 = dlx.Node(2)
    n3 = dlx.Node(3)
    n4 = dlx.Node(4)

    dlx.insert_before(n4, n1)

    assert n1.left is None
    assert n1.right == n4
    assert n4.left == n1
    assert n4.right is None

    dlx.insert_after(n1, n2)

    assert n1.right == n2
    assert n2.left == n1
    assert n2.right == n4
    assert n4.left == n2

    dlx.insert_before(n4, n3)

    assert n2.right == n3
    assert n3.left == n2
    assert n3.right == n4
    assert n4.left == n3
    assert n4.right is None


def test_forwards():
    n1 = dlx.Node(1)
    n2 = dlx.Node(2)
    n3 = dlx.Node(3)
    n4 = dlx.Node(4)

    dlx.insert_after(n1, n2)
    dlx.insert_after(n2, n3)
    dlx.insert_after(n3, n4)

    it = dlx.forwards(n1)
    assert [n.val for n in it] == [1, 2, 3, 4]

    it = dlx.forwards(n2)
    assert [n.val for n in it] == [2, 3, 4]

    dlx.insert_after(n4, n1)

    it = []
    for i, n in enumerate(dlx.forwards(n1), 1):
        it.append(n.val)
        if i >= 10:
            break

    assert it == [1, 2, 3, 4, 1, 2, 3, 4, 1, 2]


def test_pairs():
    x = [1, 2, 3, 4]
    prs = list(dlx.pairs(x))
    assert prs == [(1, 2), (2, 3), (3, 4)]
    x = [1]
    prs = list(dlx.pairs(x))
    assert prs == []


def test_create_list():
    nodes = [dlx.Node(i) for i in range(1, 5)]
    for left, right in dlx.pairs(nodes):
        dlx.insert_after(left, right)

    it = dlx.forwards(nodes[0])
    assert [n.val for n in it] == [1, 2, 3, 4]

    nodes = [dlx.Node(i) for i in range(1, 5)]
    nodes += [nodes[0]]
    for left, right in dlx.pairs(nodes):
        dlx.insert_after(left, right)

    it = []
    for i, n in enumerate(dlx.forwards(nodes[0]), 1):
        it.append(n.val)
        if i >= 10:
            break

    assert it == [1, 2, 3, 4, 1, 2, 3, 4, 1, 2]
