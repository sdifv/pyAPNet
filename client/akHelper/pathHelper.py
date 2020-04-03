import os


class PathHelper:

    BFContainer = '/home/yuhao/workplace/batfish/containers/'

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
        raise RuntimeError('snapshot has not been initialized')

    @staticmethod
    def check_init_data(config_json, topology, updates):
        return PathHelper.check_data_exist(config_json) \
               & PathHelper.check_data_exist(topology) \
               & PathHelper.check_data_exist(updates)

    @staticmethod
    def check_data_exist(path):
        if os.path.exists(path):
            if os.path.isdir(path):
                files = os.listdir(path)
                if len(files) == 0:
                    raise RuntimeError('directory[ {} ] is empty'.format(path))
        else:
            raise RuntimeError('directory or file[ {} ] is not exist'.format(path))

        return True




