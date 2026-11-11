import random

PET_TYPES = ["кот", "собака", "дракон", "робот"]

TYPE_BONUSES = {
    "кот": {"happiness": 5},
    "собака": {"energy": 10},
    "дракон": {"health": 10},
    "робот": {"cleanliness": 10}
}

EVENTS = [
    {"text": "Питомец нашёл интересную игрушку!", "happiness": 10},
    {"text": "Питомец случайно разбил вазу...", "happiness": -5, "cleanliness": -10},
    {"text": "Питомец сладко подремал на солнышке.", "energy": 15},
    {"text": "Питомец съел что-то несвежее.", "health": -10},
    {"text": "К вам зашёл друг, питомец рад!", "happiness": 15},
    {"text": "Питомец устроил погром в комнате.", "cleanliness": -20, "happiness": 5}
]

EVENT_CHANCE = 0.4


def create_pet(name: str, pet_type: str) -> dict:
    pet = {
        "name": name,
        "type": pet_type,
        "hunger": 50, # сытость (100 = сыт)
        "happiness": 50,
        "cleanliness": 50,
        "energy": 50,
        "health": 100,
        "age": 0 # возраст в днях
    }

    if pet_type in TYPE_BONUSES:
        for stat, value in TYPE_BONUSES[pet_type].items():
            pet[stat] = min(100, pet[stat] + value)

    return pet


def apply_action(pet: dict, action: str) -> dict:
    action_effects = {
        "1": {"name": "покормил", "hunger": 30, "cleanliness": -5},
        "2": {"name": "поиграл", "happiness": 25, "energy": -15, "hunger": -10},
        "3": {"name": "уложил спать", "energy": 40, "hunger": -5},
        "4": {"name": "помыл", "cleanliness": 40, "happiness": -5},
        "5": {"name": "полечил", "health": 30, "happiness": -10}
    }

    if action not in action_effects:
        return pet

    effect = action_effects[action]
    print(f"Ты {effect['name']} питомца.")

    for stat, change in effect.items():
        if stat in pet and stat != "name":
            pet[stat] = max(0, min(100, pet[stat] + change))

    # Питомец переел
    if action == "1" and pet["hunger"] >= 100:
        print("Питомец переел! Ему стало плохо.")
        pet["health"] = max(0, pet["health"] - 10)

    return pet


def trigger_random_event(pet: dict) -> dict:
    if random.random() < EVENT_CHANCE:
        event = random.choice(EVENTS)
        print(f"\nСобытие: {event['text']}")
        for stat, change in event.items():
            if stat in pet and stat != "text":
                pet[stat] = max(0, min(100, pet[stat] + change))
    return pet


def check_evolution(pet: dict) -> str:
    avg_stats = (pet["hunger"] + pet["happiness"] + pet["cleanliness"]
                 + pet["energy"] + pet["health"]) / 5

    if pet["health"] <= 0:
        return "ушёл из жизни"
    elif pet["age"] >= 30 and avg_stats >= 70:
        return "взрослый"
    elif pet["age"] >= 15 and avg_stats >= 50:
        return "подросток"
    elif avg_stats < 20:
        return "болеет"
    else:
        return "малыш"


def display_pet(pet: dict):
    stage = check_evolution(pet)
    
    print("\n" + "=" * 45)
    print(f"  {pet['name']} ({pet['type']}) — {stage}")
    print(f"  Возраст: {pet['age']} дней")
    print("=" * 45)

    stats = [
        ("Сытость", pet["hunger"]),
        ("Счастье", pet["happiness"]),
        ("Чистота", pet["cleanliness"]),
        ("Энергия", pet["energy"]),
        ("Здоровье", pet["health"])
    ]

    for label, value in stats:
        filled = value // 5
        bar = "#" * filled + "-" * (20 - filled)
        print(f"  {label:<10} [{bar}] {value}%")

    print("=" * 45 + "\n")


def main():
    print("Виртуальный питомец")
    print("=" * 40)

    print("\nВыбери тип питомца:")
    for i, pet_type in enumerate(PET_TYPES, 1):
        print(f"{i}. {pet_type.capitalize()}")

    while True:
        choice = input("Введи номер (1-4): ").strip()
        if choice in ["1", "2", "3", "4"]:
            pet_type = PET_TYPES[int(choice) - 1]
            break
        print("Неверный ввод, попробуй снова.")

    name = input("Как назовём питомца? ").strip() or "Без имени" # если пользователь оставит поле пустым, то имя будет "Без имени"

    pet = create_pet(name, pet_type)
    print(f"\nПоздравляем! У тебя теперь есть {pet_type}: {name}!")

    while True:
        display_pet(pet)

        if pet["health"] <= 0:
            print(f"{pet['name']} ушёл из жизни... Ты плохо за ним смотрел.")
            break

        print("Что сделать?")
        print("1. Покормить")
        print("2. Поиграть")
        print("3. Уложить спать")
        print("4. Помыть")
        print("5. Полечить")
        print("6. Пропустить день")
        print("7. Покинуть питомца")

        action = input("Твой выбор (1-7): ").strip()

        if action == "7":
            print(f"Ты оставляешь {pet['name']}. Прощай...")
            break
        elif action == "6":
            pet["age"] += 1
            pet["hunger"] = max(0, pet["hunger"] - 15)
            pet["happiness"] = max(0, pet["happiness"] - 10)
            pet["cleanliness"] = max(0, pet["cleanliness"] - 10)
            pet["energy"] = max(0, pet["energy"] - 10)
            print(f"\nПрошёл день. {pet['name']} стал старше.")
            pet = trigger_random_event(pet)
        elif action in ["1", "2", "3", "4", "5"]:
            pet = apply_action(pet, action)
        else:
            print("Неверная команда.")


if __name__ == "__main__":
    main()
