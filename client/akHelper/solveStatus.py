from enum import Enum


class SolveStatus(Enum):
    START = 'start to link server'
    READY = 'source data is ready'
    POST_QUERY = 'post query data to server'
    GET_RESULT = 'get query result from server'
    END = 'finish solving a query'
    FAIL = 'query execution fail'
    SUCCESS = 'query execution success'

