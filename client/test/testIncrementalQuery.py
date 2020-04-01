import traceback

from client.queries.incrementQuery import IncrementalQuery
from client.queries.initiationQuery import InitiationQuery

if __name__ == '__main__':
    query_name1 = 'init_apkeep'
    network_name = 'forwarding-change-validation'
    snapshot_name = 'base'
    # make sure that parsed config files and data plane (fibs) hava been generated by batfish
    initQuery = InitiationQuery(query_name1, network_name, snapshot_name)
    try:
        initQuery.resolve()
        query_name2 = 'detect_loops'

        # update_rules path (Diffs of fibs) is generated by Diff.py

        update_rules = '/home/yuhao//workplace/batfish/containers/229a4638-11c4-4429-a373-81c3e5782283/' \
                   'snapshots/1661fa2e-affe-45af-92fb-4b30de945112/output/APKeep/init/update_fibs'

        query = IncrementalQuery(query_name2, update_rules)
        answer = query.resolve()
        print(answer.wrapper())
    except RuntimeError as e:
        traceback.print_exc()
