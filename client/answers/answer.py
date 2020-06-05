import json

import pandas as pd
from IPython.display import display, HTML

class Answer:
    def __init__(self, query, data):
        self.query = query
        self.data = data

    def loops(self):
        if self.data is not None:
            loops_res = self.data.get('loops')
            aps_info = []
            loop_path = []
            loop_num = []

            for loop in loops_res:
                # loop： aps\paths\num
                aps = []
                for k, v in loop.get('ap').items():
                    aps.append(k + ' : ' + v)
                aps_info.append('\n'.join(aps))
                loop_path.append(self.path_wrapper(loop.get('path')))
                loop_num.append(1)

            data = {'aps_info': aps_info, 'loop_path': loop_path, 'loop_num': loop_num}

            frame = pd.DataFrame(data)
            html = frame.style.set_properties(**{'text-align': 'left'})
            return display((HTML)(html.render()))
        else:
            return None

    # def blackhole(self):
    #     pass

    def describe(self):
        if self.data is not None:
            loops_num = len(self.data.get('loops'))
        else:
            loops_num = 0

        print('loops : {}'.format(loops_num))

    def path_wrapper(self, loop_hops):
        # src:
        # [{'node': 'core2', 'inPort': 'default', 'outPort': 'GigabitEthernet2/0',
        #   'fwRule': {'outinterface': 'GigabitEthernet2/0', 'prefix': '10.12.11.2/32'}},
        #  {'node': 'spine2', 'inPort': 'GigabitEthernet0/0', 'outPort': 'GigabitEthernet2/0',
        #   'fwRule': {'outinterface': 'GigabitEthernet2/0', 'prefix': '10.12.11.2/32'}},
        #  {'node': 'leaf1', 'inPort': 'GigabitEthernet1/0', 'outPort': 'GigabitEthernet0/0',
        #   'fwRule': {'outinterface': 'GigabitEthernet0/0', 'prefix': '10.12.11.2/32'}},
        #  {'node': 'spine1', 'inPort': 'GigabitEthernet2/0', 'outPort': 'GigabitEthernet1/0',
        #   'fwRule': {'outinterface': 'GigabitEthernet1/0', 'prefix': '10.12.11.0/24'}},
        #  {'node': 'core2', 'inPort': 'GigabitEthernet3/0', 'outPort': 'GigabitEthernet2/0',
        #   'fwRule': {'outinterface': 'GigabitEthernet2/0', 'prefix': '10.12.11.2/32'}}]
        #
        # dst:
        # loop_path = '<b>border2</b>(GigabitEthernet1/0) </br> \
        # <b>core2</b>(GigabitEthernet0/0, GigabitEthernet2/0) </br>\
        # <b>spine2</b>(GigabitEthernet0/0, GigabitEthernet2/0) </br>\
        # <b>ACL</b>(leaf1_RESTRICT_NETWORK_TRAFFIC_IN_GigabitEthernet1/0_in,inport) </br>\
        # <b>ACL</b>(leaf1_RESTRICT_NETWORK_TRAFFIC_IN_GigabitEthernet1/0_in,permit) </br>\
        # <b>leaf1</b>(GigabitEthernet1/0, GigabitEthernet0/0) <br>\
        # <b>spine1</b>(GigabitEthernet2/0, GigabitEthernet0/0)</br>\
        # <b>core1</b>(GigabitEthernet2/0, GigabitEthernet1/0)</br>\
        # <b>border2</b>(GigabitEthernet2/0, GigabitEthernet1/0) </br>'
        # data = {'aps_info': ['3599:10.12.11.2/32'], 'loop_path': [loop_path], 'loop_num': ['<b>1</b>']}
        html_res = []
        index = 1
        for hop in loop_hops:
            fw = hop.get('fwRule')
            html_hop = '<b>{seq}</b>.{node}</br>RECEIVED({inport})</br>' \
                       'FORWARDED(Routes:(Prefix:{prefix},Next Hop Interface:{nhit}))</br>' \
                       'TRANSMITTED({outport})</br>'.format(seq=index, node=hop.get('node'),
                                                            inport=hop.get('inPort'),
                                                            prefix=fw.get('prefix'), nhit=fw.get('outinterface'),
                                                            outport=hop.get('outPort'))
            html_res.append(html_hop)
            index = index + 1

        res = '</br>'.join(html_res)

        return res


