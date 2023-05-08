
from collections import defaultdict
from typing import Dict, List
import weakref

from person import Person


# int is the person's ID
# defaultdict is a dictionary that automatically creates an empty list
__map: Dict[int, List] = defaultdict(list)

def add_friend(person: Person, friend: Person):
    # checking for None
    if not person or not friend:
        return
    # not allowing friend of yourself
    if person.id == friend.id:
        return

    # check if friend already exists
    if is_friend(person, friend):
        return

    current_friends = __map[person.id]
    current_friends.append(weakref.ref(friend))

def is_friend(person: Person, friend: Person) -> bool:
    # checking for None
    if not person or not friend:
        return False
    # not allowing friend of yourself
    if person.id == friend.id:
        return False

    friends: List[weakref.WeakMethod] = __map[person.id]
    for ref in friends:
        f: Person = ref()
        if f and f.id == friend.id:
            return True

def get_friends(person: Person) -> List[Person]:
    friends: List[weakref.WeakMethod] = __map[person.id]
    realized_friends = [p for ref in friends if (p := ref())]
    return realized_friends

def erase_person(person: Person):
    if person.id in __map:
        del __map[person.id]

    for lst in __map.values():
        for wr in lst:
            if (p := wr()) and p.id == person.id:
                lst.remove(wr)
                break
