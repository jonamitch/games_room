import pickle
import os
PICKLE_CACHE_FOLDER = './data/pickle_cache/'

class Globals:
    LOCK = False

def get_from_pickle_cache(cache_id, cache_location=PICKLE_CACHE_FOLDER):
    if Globals.LOCK:
        return
    Globals.LOCK = True
    output_path = os.path.join(cache_location, '{}.pickle'.format(cache_id))
    try:
        pickle_in = open(output_path, "rb")
        object_retrieved = pickle.load(pickle_in)
        Globals.LOCK = False
        return object_retrieved
    except FileNotFoundError:
        Globals.LOCK = False
        return None


def add_to_pickle_cache(obj, cache_id, cache_location=PICKLE_CACHE_FOLDER):
    output_path = os.path.join(cache_location, '{}.pickle'.format(cache_id))
    pickle_out = open(output_path, "wb")
    pickle.dump(obj, pickle_out)
    pickle_out.close()

    return

