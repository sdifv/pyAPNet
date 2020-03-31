import os


class PathHelper:
    BFContainer = '/home/yuhao/workplace/batfish/containers/'

    def __init__(self):
        pass

    @staticmethod
    def get_snapshot_path(network_name, snapshot_name):
        network_id_path = os.path.join(PathHelper.BFContainer, 'network_ids', network_name+'.id')
        if os.path.isfile(network_id_path):
            with open(network_id_path, mode='r') as f:
                network_id = f.readline()
            network_dir = os.path.join(PathHelper.BFContainer, network_id)
            if os.path.isdir(network_dir):
                snapshot_id_path = os.path.join(network_dir, 'snapshot_ids', snapshot_name+'.id')
                if os.path.isfile(snapshot_id_path):
                    with open(snapshot_id_path, mode='r') as f:
                        snapshot_id = f.readline()
                        return os.path.join(network_dir, 'snapshots', snapshot_id, 'output')
                else:
                    print('snapshot has not been created')
            else:
                print('network has not been created')
        else:
            print('container has not been created')
        raise IOError('snapshot has not been initialized')

    @staticmethod
    def check_data_exist(config_json, topology, updates):
        if os.path.isdir(config_json):
            files = os.listdir(config_json)
            if len(files) == 0:
                raise RuntimeError('config_json files not exist')
        else:
            raise RuntimeError('config_json dir not exist')

        if not os.path.isfile(topology):
            raise RuntimeError('topology file not exist')

        if not os.path.isfile(updates):
            raise RuntimeError('init_fibs file not exist')

        return True



