import json
import logging

from .redis import RedisFunction
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class RedisApi:

    def __init__(self):
        self.redis_obj = RedisFunction()

    def get_note(self, user):
        try:
            data = self.redis_obj.get_key(user)
            if data is None:
                return {}
            return json.loads(data)
        except Exception as e:
            logging.error(e)
            return Response({'message': e})

    def add_note(self, user, note):
        try:
            data = self.get_note(user)
            data.update({note.get('id'): note})
            # data = {**note_check, **{note.get('id'): note}}
            # data = {note.get('id'): note}

            self.redis_obj.set_key(user, json.dumps(data))
        except Exception as e:
            logger.error(e)

    def update_note(self, note):
        try:
            user_id = note.get('user')
            id = str(note.get("id"))
            note_dict = json.loads(self.redis_obj.get_key(user_id))

            if note_dict.get(id):
                note_dict.update({id: note})
                self.redis_obj.set_key(user_id, json.dumps(note_dict))
            else:
                print("id not found")

        except Exception as e:
            logging.error(e)

    def delete_note(self, note, user_id):
        try:

            # user_id = note.get('user')
            note_dict = json.loads(self.redis_obj.get_key(user_id))

            if note_dict is not None:
                print(note_dict)
                note_dict.pop(str(note.id))
                print(note_dict)
                self.redis_obj.set_key(user_id, note_dict)
            return None

        except Exception as e:
            logging.error(e)
