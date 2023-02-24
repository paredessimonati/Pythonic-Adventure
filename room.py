import random
import attr
import re


class Room:
    def __init__(self) -> None:
        self.current_room = None
        self.description = ""
        self.description_2 = ""
        self.description_3 = ""
        self.description_search = ""
        self.loot = ""
        self.potion = ""
        self.seed = 0

    def room_variables(self):
        return self.current_room

    def room_after_encounter(self):
        return self.description_1, self.description_2, self.description_3

    def room_loot(self):
        return self.loot, self.potion

    def new_room(self) -> None:  # EX get_attr()
        # getting all the variables up and randomized
        random_variables = {
            "room": random.choice(attr.room),
            "visibility": random.choice(attr.visibility),
            "temperature": random.choice(attr.temperature),
            "air": random.choice(attr.air),
            "humidity": random.choice(attr.humidity),
            "decoration": random.choice(attr.decoration),
            "furniture": random.choice(attr.furniture),
            "floor texture": random.choice(attr.floor_texture),
            "torch_number": random.choice(attr.torch_number),
            "torches": random.choice(attr.torches),
            "sound": random.choice(attr.sounds),
            "occupancy": random.choice(attr.occupancy),
            "search": random.choice(attr.search),
            "exits": random.sample(attr.exits, random.randrange(1, 4)),
            "trap_doors": random.choice(attr.trap_doors),
            "containers": random.choice(attr.containers),
            "enemy": random.choice(list(attr.enemies)),
            "loot": random.choice(list(attr.loot)),
            "what_in_front": random.choice(attr.what_in_front),
            "directions": random.shuffle(attr.directions),
            "no_enemy": random.choice(attr.no_enemy),
        }
        self.current_room = random_variables
        self.seed = str(random.randrange(0, 9999999999)).zfill(10)
        """
        10 Digits seed, used in:
        Room - room_search()
            [0:2] = trap door %
            [2:4] = loot container %
            [4:6] = potion %
        Enemy - visibility()
            [6:8] = enemy visibility %
        Enemy - aggro()
            [8]= aggro trigger
        """

    def describe_room(self, count, enemy_spawn):
        # setting up long printing variables
        # dash_line = "-" * 65
        # press_to_continue = f"{'-' * 21}Press Enter to Continue{'-' * 21}"

        # starting to make the string
        # Leaving first line out of the description if the player calls it again.
        # print(f'{dash_line}\n\n{self.current_room["room"]}')

        # If this is the first room defaults to open your eyes.
        if count == 0:
            self.description = "You open your eyes. "

        # Else selects first random string.
        else:
            self.description = self.current_room["room"]

        s = list(self.current_room.values())[1:5]
        self.description += "".join(s)

        ## MAYBE ILL ADD THIS LATER
        #  if room is black and there are no torches make him blind for the room.
        #  stoping here because all the properties until now can be felt if player
        #  is blind.

        s = list(self.current_room.values())[5:8]
        self.description += "".join(s)

        # setting some variables to make the code easier to read
        light_source = self.current_room["torch_number"]
        light_color = self.current_room["torches"]

        if light_source != " you see no light sources.":
            s = light_source.split()[:3] + [light_color] + light_source.split()[3:]
            self.description += " ".join(s)
        else:
            self.description += "and there are no candles or torches to be seen."

        # continuing with the description.
        s = list(self.current_room.values())[10:11]
        self.description += "".join(s)

        # if there is no monster the room should feel empty
        if enemy_spawn is False:
            self.current_room["occupancy"] = random.choice(attr.occupancy_no_spawn)
        self.description += self.current_room["occupancy"]
        return self.description.strip()
        # input(f"{self.description_3}\n\n{press_to_continue}")

    def room_search(self):
        exits = self.current_room["exits"]
        print(f'{self.current_room["search"]}\n')
        print("- Exits:")
        for _ in range(len(exits)):
            print(f"You see {exits[_]} {attr.directions[_]}.")

        if self.seed[0:2] > "95":
            print(f'\nYou see {self.current_room["trap_doors"]} beneath you.')

        if self.seed[2:4] > "00":
            print(
                f'\n- Loot:\nYou see {self.current_room["containers"]} {attr.directions[4]}.'
            )
            self.loot = re.findall(r"'(.*)'", self.current_room["containers"])
        if self.seed[4:6] >= "01":
            self.potion = "red potion"
            print(f"\n- Potion:\nYou see a 'red potion' {attr.directions[5]}.\n")

        return 0
