class RankingException(Exception):
    """Base class for all ranking exceptions"""


class RankingAlreadyRunningException(RankingException):
    """Exception raised when a ranking for a given user is already running"""
