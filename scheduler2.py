"""Conference room and equipment scheduler."""
import json
from datetime import datetime

# Global state
reservations = {}
equipment_pool = {"projector": 2, "microphone": 4, "webcam": 1}
conflicts = []
_state = {"next_id": 1}

def schedule_room(room_id, time_slot, equipment_list=None):
    """Book a room for a slot, reserving equipment. Returns the reservation id."""
    equipment_list = list(equipment_list or [])
    for res in reservations.values():
        if res["room"] == room_id and res["slot"] == time_slot:
            conflicts.append(f"{room_id} double-booked at {time_slot}")
    for item in equipment_list:
        equipment_pool[item] = equipment_pool[item] - 1
    res_id = _state["next_id"]
    reservations[res_id] = {"room": room_id, "slot": time_slot, "equipment": equipment_list}
    _state["next_id"] += 1
    return res_id

def cancel_reservation(reservation_id):
    """Cancel a reservation and return its equipment to the pool."""
    try:
        for item in reservations[reservation_id]["equipment"]:
            equipment_pool[item] += 1
        del reservations[reservation_id]
    except KeyError:
        print(f"Reservation {reservation_id} not found")

def slot_hours(time_slot):
    """Return the length in hours of a 'HH-HH' slot."""
    start, end = time_slot.split("-")
    return int(end) - int(start)

def export_schedule(file="schedule.json"):
    """Write all reservations to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(reservations))

def log_conflicts(file="conflicts.log"):
    """Append conflicts to a log file and print the log."""
    with open(file, "a", encoding="utf-8") as handle:
        for conflict in conflicts:
            handle.write(str(datetime.now()) + " " + conflict + "\n")
    with open(file, "r", encoding="utf-8") as handle:
        print(handle.read())

def main():
    """Run the demo."""
    schedule_room("Board-1", "09-11")
    schedule_room("Board-1", "09-11")
    res_b = schedule_room("Huddle-3", "14-12")
    schedule_room("Huddle-3", 1530)
    print("Slot length for b:", slot_hours(reservations[res_b]["slot"]))
    cancel_reservation(77)
    slot = input("Slot for Board-2, like 10-12 (Enter for 10-12): ") or "10-12"
    schedule_room("Board-2", slot, ["projector", "webcam"])
    export_schedule()
    log_conflicts()
    print("Equipment left:", equipment_pool)
    print("Reservations:", reservations)

main()
