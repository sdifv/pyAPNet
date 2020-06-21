import json

from client.apkeep import RealConfig

if __name__ == '__main__':
    network = 'forwarding-change-validation'
    base_snapshot = 'base'
    new_snapshot = 'change'

    realConfig = RealConfig(network, base_snapshot)

    ans1 = realConfig.base_check()
    # ans1.describe()
    # ans1.loops()

    ans2 = realConfig.update_check(new_snapshot)
    # ans2.describe()
    ans2.differentialReachability()

