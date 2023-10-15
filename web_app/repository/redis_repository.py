import redis  # type: ignore
import pickle

# r = redis.Redis(host='localhost', port=6379, db=0)
r = redis.Redis(host='redis', port=6379, db=0)


class RedisRepository:
    def add_item_to_cash(self, name: str, value: object):
        pickled_value = pickle.dumps(value)
        return r.set(name, pickled_value, ex=360)

    def get_item_from_cash(self, name: str):
        picklet_value = r.get(name)
        if picklet_value:
            return pickle.loads(picklet_value)

    def del_item_from_cash(self, name: str):
        return r.delete(name)

    def get_list_items_from_cash(self, id_list: list):
        values = r.mget(id_list)
