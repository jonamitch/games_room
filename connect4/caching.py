import sys
from functools import wraps


ACTIVATE_SCORE_CACHING = True

score_cache = {}


def cache_score_of_board():
    def decorator(f):
        @wraps(f)
        def decorated_function(self, *args, **kwargs):
            if ACTIVATE_SCORE_CACHING:
                key = self.id()
                if key in score_cache:
                    self.score, self.score_details, self.winner = score_cache[key]
                else:
                    f(self, *args, **kwargs)
                    score_cache[key] = (self.score, self.score_details, self.winner)
            else:
                f(self, *args, **kwargs)
            return
        return decorated_function
    return decorator
