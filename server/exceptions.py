class ReplayException(Exception):
    pass


class UntrackedReplay(ReplayException):
    pass


class ReplayAlreadyExists(ReplayException):
    pass


class RateLimitExceeded(Exception):
    pass
