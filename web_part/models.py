from pony.orm import *
from datetime import datetime

db = Database()

class Object(db.Entity):
    tracker_id = Required(int, unique=True)
    name = Required(str)
    img_path = Optional(str)

    time_appear = Required(datetime)
    time_exit = Required(datetime)

    confidence = Optional(float)


db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
set_sql_debug(False)

@db_session
def create_object(tracker_id, name, img_path, time_appear, confidence):
    now = datetime.now()
    Object(tracker_id=tracker_id, name=name, img_path=img_path,
           time_appear=time_appear if time_appear else now,
           time_exit=now, confidence=confidence)
    # commit() will be done automatically

@db_session
def update_object_exit_time(tracker_id, time_exit):
    obj = db.Object.get(tracker_id=tracker_id)
    obj.time_exit = time_exit

@db_session
def get_object(tracker_id):
    return db.Object.get(tracker_id=tracker_id)

@db_session
def get_all_object():
    return Object.select().order_by(lambda c: desc(c.time_appear))

@db_session
def delete_all_object():
    Object.select().delete(bulk=True)



@db_session
def get_object_in_date_range(start: datetime, end: datetime):
    #   user    user
    #   [       ]
    #Obj    Obj
    #[      ]
    return select(obj for obj in Object if not (
                  obj.time_exit <= start or
                  end <= obj.time_appear
                  ))


@db_session
def query_object(date_start: datetime, date_end: datetime, types: [str]) -> [Object]:
    #   user    user
    #   [       ]
    #Obj    Obj
    #[      ]
    return select(obj for obj in Object if not (
                  obj.time_exit <= date_start or
                  date_end <= obj.time_appear
                  ) and (
                      obj.name in types
                ))

