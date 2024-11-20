def get_all_auditories(auditoriums_to_zones) -> str:
    floors = {}
    result_message = ""

    for zone, auditoriums in auditoriums_to_zones.items():
        floor = zone.split('_')[-1]
        if floor.isdigit():
            floor = int(floor)
            if floor not in floors:
                floors[floor] = []
            floors[floor].extend(auditoriums)

    for floor, auditoriums in sorted(floors.items()):
        result_message += f"{floor} этаж: {', '.join(sorted(auditoriums))}\n"

    return result_message