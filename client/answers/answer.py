import pandas as pd
from IPython.display import display, HTML


def pretty_print(df):
    return display(HTML(df.to_html(justify='left').replace("\\n", "<br>")))


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
                for k, v in loop.get('aps').items():
                    aps.append(k + ' : ' + v)
                aps_info.append('\n'.join(aps))
                loop_path.append(loop.get('path'))
                loop_num.append(1)

            data = {'aps_info': aps_info, 'loop_path': loop_path, 'loop_num': loop_num}
            frame = pd.DataFrame(data)
            # frame.style.set_properties(**{'text-align': 'left', 'vertical-align': 'top'})
            return pretty_print(frame)
        else:
            return None

    # def blackhole(self):
    #     pass

    def describe(self, num=0):
        if self.data is not None and num == 0:
            loops_num = len(self.data.get('loops'))
        else:
            loops_num = 0

        print('loops : {}'.format(loops_num))
