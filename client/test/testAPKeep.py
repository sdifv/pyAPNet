from client.apkeep import APKeep


if __name__ == '__main__':
    network = 'forwarding-change-validation'
    base_snapshot = 'base'
    new_snapshot = 'change'

    ap = APKeep(network, base_snapshot)

    ans1 = ap.base_check()
    ans1.describe()
    # ans1.loops()

    # ans2 = ap.update_check(new_snapshot)
    # ans2.describe()
    # print(ans2.loops())
