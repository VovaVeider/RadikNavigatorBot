import heapq

from bot.bin.auditories_config import auditoriums_to_zones, transitions
from bot.entity.enum.Zones import Zones
from bot.entity.navigation.Route import Route


# Функция для определения зоны по номеру аудитории
def find_zone(auditorium):
    for zone, rooms in auditoriums_to_zones.items():
        if auditorium in rooms:
            return Zones[zone]
    return None



def dijkstra(start_zone, goal_zone):
    queue = [Route(0, start_zone, [])]
    visited = set()

    while queue:
        route = heapq.heappop(queue)
        current_weight, current_zone, path = route.weight, route.dst, route.path

        if current_zone in visited:
            continue

        path = path + [current_zone]

        if current_zone == goal_zone:
            return current_weight, path

        visited.add(current_zone)

        for (src, dst), data in transitions.items():
            if src == current_zone and dst not in visited:
                weight = data['weight']
                heapq.heappush(queue, Route(current_weight + weight, dst, path))
            elif dst == current_zone and src not in visited:
                weight = data['weight']
                heapq.heappush(queue, Route(current_weight + weight, src, path))

    return float('inf'), []


def print_path_descriptions(path):
    steps_message = ""
    for i in range(len(path) - 1):
        src = path[i]
        dst = path[i + 1]

        # Проверяем, есть ли описание перехода из src в dst
        if (src, dst) in transitions:
            description = transitions[(src, dst)]['descr_to']
        else:
            description = transitions[(dst, src)]['descr_reverse']

        steps_message += f"{description}\n"
    return steps_message


def find_route(current_aud, find_aud):
    result_steps_message = ""

    start_zone = find_zone(current_aud)
    goal_zone = find_zone(find_aud)

    total_weight, path = dijkstra(start_zone, goal_zone)

    if path:
        result_steps_message = print_path_descriptions(path)
        result_steps_message += f"\nНайдите аудиторию: {find_aud}"
    else:
        result_steps_message = f"Путь не найден."

    return result_steps_message
