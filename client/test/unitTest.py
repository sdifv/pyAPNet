import json
import pandas as pd
from IPython.display import display, HTML
from client.akHelper.solveStatus import SolveStatus


# def pretty_print(df):
#     return display(HTML(df.to_html().replace("\\n", "<br>")))
#
#
# if __name__ == '__main__':
#
#     line = {"query": ['send\ncmd'], "type": ["aka"]}
#     print(pretty_print(pd.DataFrame(line)))

def pretty_print(df):
    return display(HTML(df.to_html().replace("\\n","<br>")))


data = [
       {'id': 1, 't': 'very long text\ntext line 2\ntext line 3'},
       {'id': 2, 't': 'short text'}
       ]
df = pd.DataFrame(data)
df.set_index('id', inplace=True)

pretty_print(df)
