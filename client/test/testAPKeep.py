from client.apkeep import APKeep


if __name__ == '__main__':
    network = 'forwarding-change-validation'
    base_snapshot = 'base'
    new_snapshot = 'change'

    ap = APKeep()

    ans1 = ap.base_check(network, base_snapshot)
    ans1.describe()
    ans1.loops()

    # ans2 = ap.update_check(new_snapshot)
    # ans2.describe()
    # ans2.loops()