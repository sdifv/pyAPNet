import traceback

from client.queries.baseCheck import InitiationQuery

if __name__ == '__main__':
    query_name = 'init_apkeep'
    network_name = 'forwarding-change-validation'
    snapshot_name = 'base'
    initQuery = InitiationQuery(query_name, network_name, snapshot_name)
    try:
        initQuery.resolve()
    except RuntimeError as e:
        traceback.print_exc()
