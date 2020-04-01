from client.queries.query import Query


class ReachabilityQuery(Query):
    range = [
        'reachability',
        'detectLoops',
        'blackHoles'
    ]


    def detectLoops(self):
        pass

    def reachability(self):
        pass

