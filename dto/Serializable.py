import json


class Serializable:

    def __to_json_object(self):

        def process_inner_objects(obj):
            if type(obj) is list:
                return [process_inner_objects(x) for x in obj]
            if type(obj) is dict:
                return {k: process_inner_objects(v) for k, v in obj.items()}
            if isinstance(obj, Serializable):
                return obj.__to_json_object()
            return obj

        return process_inner_objects(vars(self))

    def to_json(self):
        return json.dumps(self.__to_json_object())
