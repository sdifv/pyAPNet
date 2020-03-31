from client.queries.query import query


class ReachabilityQuery(query):
    range = [
        'reachability',
        'detectLoops',
        'blackHoles'
    ]


    def detectLoops(self):
        pass

    def reachability(self):
        pass

