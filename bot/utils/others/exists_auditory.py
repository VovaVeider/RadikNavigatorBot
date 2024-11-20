def exists_auditory(audotory: str, auditoriums_to_zones) -> bool:
    # Проверяем наличие аудитории в словаре
    for auditoriums in auditoriums_to_zones.values():
        if audotory in auditoriums:
            return True
    return False