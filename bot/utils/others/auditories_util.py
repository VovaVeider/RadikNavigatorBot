from bot.bin.auditories import rooms


def display_rooms_by_floor():
    floors = {0: [], 1: [], 2: []}

    # Разделяем комнаты по этажам
    for room, info in rooms.items():
        floors[info["floor"]].append(room)

    # Выводим комнаты по этажам в одну строку
    for floor, rooms_list in floors.items():
        print(f"\nЭтаж {floor}: {', '.join(rooms_list)}")


def find_route(start_room, end_room):
    start = rooms[start_room]
    end = rooms[end_room]

    route = []
    name_wings = {
        "left": "левом",
        "center": "центральном",
        "right": "правом"
    }
    current_floor = start["floor"]
    current_wing = start["wing"]
    current_russion_wing = name_wings[start["wing"]]
    # Добавляем начальную позицию
    route.append(f"Вы находитесь на {current_floor} этаже в {current_russion_wing} крыле.\n")

    # Переход между этажами
    if current_floor != end["floor"]:
        if current_floor > end["floor"]:
            route.append(f"👇 Спуститесь на {end['floor']} этаж")
        else:
            route.append(f"☝️ Поднимитесь на {end['floor']} этаж")
        current_floor = end["floor"]
        route.append(f"Теперь вы находитесь на {current_floor} этаже в {current_russion_wing} крыле.")

    # Переход между крыльями
    if current_wing != end["wing"]:
        if current_wing == "right" and end["wing"] == "center":
            route.append("Перейдите из правого крыла в центр")
        elif current_wing == "center" and end["wing"] == "left":
            route.append("Перейдите из центра в левое крыло")
        elif current_wing == "right" and end["wing"] == "left":
            route.append("Перейдите через центр в левое крыло")
        elif current_wing == "center" and end["wing"] == "right":
            route.append("Перейдите из центра в правое крыло")
        elif current_wing == "left" and end["wing"] == "center":
            route.append("Перейдите из левого крыла в центр")
        elif current_wing == "left" and end["wing"] == "right":
            route.append("Перейдите через центр в правое крыло")
        # current_wing = name_wings[end["wing"]]
        route.append(f"Теперь вы находитесь на {current_floor} этаже в {current_russion_wing} крыле.")
    route.append(f"\n🔎 Найдите аудиторию {end_room}.")

    return route
