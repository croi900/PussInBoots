from room import Room
import json
import requests

queue = []

def fetch_queue():
    response = requests.get("http://192.168.202.215:8080/list")
    reslist = json.loads(response.text)

    for target in reslist:
        queue.append((target, 1, len(queue) + 1))
    print(queue)
    

def localization(rooms):
    
    result_dictionary = {}
    """
    for room in rooms:
        for target, attempts, tid in queue:
            if target in room.items:
                room.items.remove(target)
                queue.remove((target, attempts, tid))
                if not result_dictionary.has_key(room.id):
                    result_dictionary[room.id] = []
                result_dictionary[room.id].append((target, attempts, tid))
            else:
                attempts = attempts - 1
                if attempts <= 0:
                    newf = []
                    for tg,at,ii in queue:
                        if ii != tid:
                            newf.append((tg,at,ii))
                    queue.clear()
                    queue = newf
                    failures.append((target, attempts, tid))
    """
    """big_list = []
    s = ""
    for room in rooms:
        for item in room.items:
            big_list.append([item.name, room.id])
            s += item.name + str(room.id)
        s += item[0]
    """

    for room in rooms:
        result_dictionary[room.id] = []
        for item in room.items:
            result_dictionary[room.id].append(item.name)

    s = json.dumps(result_dictionary)

    result = requests.get(f"http://192.168.202.215:8080/response?text={s}")
if __name__ == "__main__":
    localization([])
