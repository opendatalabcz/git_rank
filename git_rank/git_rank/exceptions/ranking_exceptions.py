class RankingException(Exception):
    """Base class for all ranking exceptions"""


class RankingAlreadyRunningException(RankingException):
    """Exception raised when a ranking for a given user is already running"""


class NoRepositoryFoundException(RankingException):
    """Exception raised when no repository is found on given URL"""
