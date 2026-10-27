"""Conference room and equipment scheduler."""
import json
from datetime import datetime

# Global state
reservations = {}
equipment_pool = {"projector": 2, "microphone": 4, "webcam": 1}
conflicts = []
_state = {"next_id": 1}


def parse_slot(time_slot):
    """Validate a 'HH-HH' slot and return (start, end) as ints."""
    try:
        start, end = (int(part) for part in str(time_slot).split("-"))
    except ValueError as exc:
        raise ValueError(
            f"Invalid slot {time_slot!r}: use HH-HH, e.g. 10-12") from exc
    if not 0 <= start < end <= 24:
        raise ValueError(
            f"Invalid slot {time_slot!r}: end must be after start (0-24)")
    return start, end


def schedule_room(room_id, time_slot, equipment_list=None):
    """Book a room for a slot, reserving equipment.

    Returns the reservation id, or None if the room is double-booked.
    Raises ValueError for a bad slot or unavailable equipment.
    """
    parse_slot(time_slot)
    equipment_list = list(equipment_list or [])
    for res in reservations.values():
        if res["room"] == room_id and res["slot"] == time_slot:
            conflicts.append(f"{room_id} double-booked at {time_slot}")
            return None
    for item in set(equipment_list):
        if equipment_pool.get(item, 0) < equipment_list.count(item):
            raise ValueError(f"Not enough {item!r} available")
    for item in equipment_list:
        equipment_pool[item] -= 1
    res_id = _state["next_id"]
    _state["next_id"] += 1
    reservations[res_id] = {
        "room": room_id, "slot": time_slot, "equipment": equipment_list}
    return res_id


def cancel_reservation(reservation_id):
    """Cancel a reservation and return its equipment to the pool."""
    if reservation_id not in reservations:
        print(f"Reservation {reservation_id} not found")
        return
    for item in reservations[reservation_id]["equipment"]:
        equipment_pool[item] += 1
    del reservations[reservation_id]


def slot_hours(time_slot):
    """Return the length in hours of a 'HH-HH' slot."""
    start, end = parse_slot(time_slot)
    return end - start


def export_schedule(file="schedule.json"):
    """Write all reservations to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(reservations, handle)


def log_conflicts(file="conflicts.log"):
    """Append new conflicts to a log file, print the log, clear the list."""
    with open(file, "a", encoding="utf-8") as handle:
        for conflict in conflicts:
            handle.write(f"{datetime.now()} {conflict}\n")
    conflicts.clear()
    with open(file, "r", encoding="utf-8") as handle:
        print(handle.read())


def try_schedule(room_id, time_slot, equipment_list=None):
    """Schedule a room, reporting problems instead of crashing."""
    try:
        res_id = schedule_room(room_id, time_slot, equipment_list)
    except ValueError as err:
        print(f"Could not book {room_id}: {err}")
        return None
    if res_id is None:
        print(f"Could not book {room_id}: already booked at {time_slot}")
    return res_id


def main():
    """Run the demo."""
    try_schedule("Board-1", "09-11")
    try_schedule("Board-1", "09-11")
    try_schedule("Huddle-3", "14-12")
    try_schedule("Huddle-3", 1530)
    cancel_reservation(77)
    slot = input("Slot for Board-2, like 10-12 (Enter for 10-12): ") or "10-12"
    res_id = try_schedule("Board-2", slot, ["projector", "webcam"])
    if res_id is not None:
        print("Slot length for Board-2:", slot_hours(slot), "hours")
    export_schedule()
    log_conflicts()
    print("Equipment left:", equipment_pool)
    print("Reservations:", reservations)


if __name__ == "__main__":
    main()
