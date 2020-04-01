import json
import os
import sys
import traceback

from client.akHelper.fibHelper import ip2decimalism, format_fib_entry
from client.akHelper.jsonHelper import *
from client.akHelper.pathHelper import PathHelper
from client.answers.initiationAnswer import InitiationAnswer
from client.queries.query import Query
from client.akHelper.solveStatus import SolveStatus


class InitiationQuery(Query):

    def __init__(self, query_name, network_name, snapshot_name):
        Query.__init__(self, query_name)
        self.network = network_name
        self.snapshot = snapshot_name

    def get_snapshot_path(self):
        network = self.network
        snapshot = self.snapshot
        try:
            return PathHelper.get_snapshot_path(network, snapshot)
        except IOError as e:
            traceback.print_exc()
            sys.exit(-1)

    def send_input_data(self, config_json, topology, updates):
        config_files = os.listdir(config_json)
        for file in config_files:
            with open(os.path.join(config_json, file), mode='r') as f:
                packet = {
                    'head': '/json/'+file,
                    'data': f.read()
                }

                data = warp_input('data', packet)
                print('send data: ' + packet.get('head'))
                self.socket.sendall(data.encode('utf-8'))

        with open(topology, mode='r') as f:
            packet = {
                'head': '/fw/topo.txt',
                'data': f.read()
            }

            data = warp_input('data', packet)
            print('send data: ' + packet.get('head'))
            self.socket.sendall(data.encode('utf-8'))

        with open(updates, mode='r') as f:
            packet = {
                'head': '/parsed/updates',
                'data': f.read()
            }
            data = warp_input('data', packet)
            print('send data: ' + packet.get('head'))
            self.socket.sendall(data.encode('utf-8'))

        data = warp_input('cmd', 'input_over')
        print('send cmd: ' + data)
        self.socket.sendall(data.encode('utf-8'))

    def send_init_request(self):
        data = warp_input('cmd', 'init_request', self.network)
        print('send cmd: ' + data)
        self.socket.sendall(data.encode('utf-8'))

    def generate_init_fibs(self, path, updates):
        fibs_path = os.path.join(path, 'fibs')
        updates_path = updates
        try:
            files = os.listdir(fibs_path)
            with open(updates_path, mode='w') as f:
                for node in files:
                    for line in open(os.path.join(fibs_path, node)):
                        f.write(format_fib_entry('+', line, node))
        except IOError as e:
            traceback.print_exc()
            sys.exit(-1)

    def resolve(self):
        metadata = self.get_snapshot_path()
        APKeep_init = os.path.join(metadata, 'APKeep', 'init')
        config_json = os.path.join(APKeep_init, 'parsedConfig')
        topology = os.path.join(APKeep_init, 'layer1Topology.txt')
        updates = os.path.join(APKeep_init, 'init_fibs')

        self.generate_init_fibs(metadata, updates)

        if PathHelper.check_data_exist(config_json, topology, updates):
            self.set_status(SolveStatus.READY)

        if self.status == SolveStatus.READY:
            self.send_init_request()
            resp4init_request = self.socket.recv(1024)
            if resp4init_request.decode('utf-8') == 'received cmd: init_request':
                self.set_status(SolveStatus.POST_QUERY)
                self.send_input_data(config_json, topology, updates)

                resp4data = self.socket.recv(1024)

                print(resp4data.decode('utf-8'))
                # if resp4data.decode('utf-8') == 'init apkeep: success':
                #     self.set_status(SolveStatus.SUCCESS)
                #     # return InitiationAnswer(self.name, self.status)
                #     print("success")
                self.set_status(SolveStatus.END)
                # else:
                #     print(resp4data.decode('utf-8'))
                #     raise RuntimeError('server fail to receive query data')
            else:
                print(resp4init_request.decode('utf-8'))
                raise RuntimeError('server fail to receive query')



