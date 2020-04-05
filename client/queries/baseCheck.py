import json
import os
import sys
import traceback

from client.akHelper.fibHelper import ip2decimalism, format_fib_entry
from client.akHelper.jsonHelper import *
from client.akHelper.pathHelper import PathHelper
from client.answers.answer import Answer
from client.queries.query import Query
from client.akHelper.solveStatus import SolveStatus


class BaseCheck(Query):

    def __init__(self, query_name, network_name, snapshot_name):
        Query.__init__(self, query_name)
        self.network = network_name
        self.snapshot = snapshot_name

    def get_snapshot_path(self):
        network = self.network
        snapshot = self.snapshot
        return PathHelper.get_snapshot_path(network, snapshot)

    def send_input_data(self, config_json, topology, updates):
        config_files = os.listdir(config_json)
        for file in config_files:
            with open(os.path.join(config_json, file), mode='r') as f:
                packet = {
                    'head': '/json/'+file,
                    'body': f.read()
                }

                data = warp_input('data', 'input configs', packet)
                # print('send data: ' + packet.get('head'))
                self.socket.sendall(data.encode('utf-8'))

        with open(topology, mode='r') as f:
            packet = {
                'head': '/fw/topo.txt',
                'body': f.read()
            }

            data = warp_input('data', 'input topology', packet)
            # print('send data: ' + packet.get('head'))
            self.socket.sendall(data.encode('utf-8'))

        with open(updates, mode='r') as f:
            packet = {
                'head': '/parsed/updates',
                'body': f.read()
            }
            data = warp_input('data', 'input base rules', packet)
            # print('send data: ' + packet.get('head'))
            self.socket.sendall(data.encode('utf-8'))

        data = warp_input('cmd', 'input_over')
        # print('send cmd: ' + data)
        self.socket.sendall(data.encode('utf-8'))

    def send_init_request(self):
        data = warp_input('cmd', 'init_request', self.network)
        # print('send cmd: ' + data)
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
        init = os.path.join(metadata, 'APKeep', 'init')
        config_json = os.path.join(init, 'parsedConfig')
        topology = os.path.join(init, 'layer1Topology.txt')
        updates = os.path.join(init, 'init_fibs')

        self.generate_init_fibs(metadata, updates)

        if PathHelper.check_init_data(config_json, topology, updates):
            self.set_status(SolveStatus.READY)

        if self.status == SolveStatus.READY:
            self.send_init_request()
            resp_json = self.socket.recv(1024).decode('utf-8')
            # print(resp_json)
            resp = json.loads(resp_json)
            if resp.get('type') == 'aka' and resp.get('query') == 'init request':
                self.set_status(SolveStatus.POST_DATA)
                self.send_input_data(config_json, topology, updates)

                while True:
                    resp_json = self.socket.recv(1024).decode('utf-8')
                    # print(resp_json)
                    resp = json.loads(resp_json)
                    if resp.get('type') == 'aka' and resp.get('query') == 'base check':
                        break
                    else:
                        answer = Answer(resp.get('query'), resp.get('data'))
                self.set_status(SolveStatus.END)
                return answer
            else:
                raise RuntimeError('base check failed!')
        else:
            raise RuntimeError('initial data is not ready')



