import json

import pandas as pd
from IPython.display import display, HTML


def flow_wrapper(flow):
    return '<b>src ip</b>:{src_ip}</br>' \
           '<b>dst ip</b>:{dst_ip}</br>' \
           '<b>src port</b>:{src_port}</br>' \
           '<b>dst port</b>:{dst_port}</br>' \
           '<b>protocol</b>:{protocol}</br>'.format(src_ip=flow.get("src ip"),
                                                    dst_ip=flow.get("dst ip"),
                                                    src_port=flow.get("src port"),
                                                    dst_port=flow.get("dst port"),
                                                    protocol=flow.get("protocol"))


def try_get(obj, attr):
    if obj is None:
        return None
    else:
        return obj.get(attr)


def path_wrapper(paths):
    paths_html = []
    path_index = 1
    for path in paths:
        hops_html = ['<b>{path_seq}</b>'.format(path_seq=path_index)]
        hop_index = 1
        for hop in path:
            fw = hop.get('fwRule')
            in_acl = hop.get('inACL')
            out_acl = hop.get('outACL')
            hop_html = '<b>({hop_seq})</b>.{node}</br>RECEIVED({in_port})</br>' \
                       'INACL({in_action}:{in_acl})</br>' \
                       'FORWARDED(Routes:(Prefix:{prefix},Next Hop Interface:{nhit}))</br>' \
                       'OUTACL({out_action}:{out_acl})</br>' \
                       'TRANSMITTED({out_port})'.format(hop_seq=hop_index, node=hop.get('node'),
                                                        in_port=hop.get('inPort'),
                                                        in_action=try_get(in_acl, 'action'),
                                                        in_acl=try_get(in_acl, 'acl name'),
                                                        # prefix=fw.get('prefix'), nhit=fw.get('outinterface'),
                                                        prefix='None', nhit='None',
                                                        out_action=try_get(out_acl, 'action'),
                                                        out_acl=try_get(out_acl, 'acl name'),
                                                        out_port=hop.get('outPort'))
            hops_html.append(hop_html)
            hop_index = hop_index + 1
        path_html = '</br>'.join(hops_html)
        paths_html.append(path_html)
        path_index = path_index + 1

    return '</br>'.join(paths_html)


class Answer:
    def __init__(self, query, data):
        self.query = query
        self.data = data

    def loops(self):
        if self.data is not None:
            loops_res = self.data.get('loops')
            loops_flow = []
            loops_path = []
            loops_num = []

            for loop in loops_res:
                loops_flow.append(flow_wrapper(loop.get('flow')))
                loops_path.append(path_wrapper(loop.get('path')))
                loops_num.append(1)

            data = {'aps_info': aps_info, 'loop_path': loop_path, 'loop_num': loop_num}

            frame = pd.DataFrame(data)
            html = frame.style.set_properties(**{'text-align': 'left'})
            return display((HTML)(html.render()))
        else:
            return None

    # def blackhole(self):
    #     pass

    def differentialReachability(self):
        if self.data is not None:
            diffs = self.data.get('reachability diff')
            diff_flows = []
            before_paths = []
            after_paths = []

            for diff in diffs:
                diff_flows.append(flow_wrapper(diff.get('flow')))
                before_paths.append(path_wrapper(diff.get('before')))
                after_paths.append(path_wrapper(diff.get('after')))

            data = {'flows': diff_flows, 'before paths': before_paths, 'after paths': after_paths}
            frame = pd.DataFrame(data)
            html = html = frame.style.set_properties(**{'text-align': 'left'})
            return display((HTML)(html.render()))
        else:
            return None

    def describe(self):
        loops_num = 0
        diffs_num = 0
        if self.data is not None:
            if self.data.get('loops') is not None:
                loops_num = len(self.data.get('loops'))

            if self.data.get('reachability diff') is not None:
                diffs_num = len(self.data.get('reachability diff'))

        print('loops : {loops}, differentialReachability : {diffs}'.format(loops=loops_num, diffs=diffs_num))
