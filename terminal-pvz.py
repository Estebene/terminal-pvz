from rich.console import Console
from time import sleep
from pynput import keyboard
from random import randint

from cursor_utils import hide_cursor, show_cursor

CANVAS_HEIGHT = 5
CANVAS_WIDTH = 10
EMPTY_CHAR = "  "

STARTING_SUN = 50

canvas = [[EMPTY_CHAR for _ in range(CANVAS_WIDTH)] for _ in range(CANVAS_HEIGHT)]
canvas_styles = [[None for _ in range(CANVAS_WIDTH)] for _ in range(CANVAS_HEIGHT)]

entities = []

def share_position(entity1, entity2):
    return [entity1.position[0] == entity2.position[0], entity1.position[1] == entity2.position[1]].count(True) == 2

class Entity:
    def __init__(self, health, representation, position):
        self.health = health
        self.representation = representation
        self.position: list[int] = position
        self.tick_count = 0

class Zombie(Entity):
    def __init__(self, position):
        self.representation = "🧟"
        self.health = 100
        super().__init__(self.health, self.representation, position)
    
    def tick(self):
        blocked = False
        self.tick_count += 1
        for entity in entities:
            if isinstance(entity, Plant):
                if entity.position[0] == self.position[0] - 1 and entity.position[1] == self.position[1]:
                    blocked = True
                    entity.health -= 10
                    if entity.health <= 0:
                        entities.remove(entity) 
        if not blocked:
            if self.tick_count % 10 == 0:     
                self.position[0] -= 1
        
class Plant(Entity):
    def __init__(self, health, representation, position):
        self.health = health
        self.representation = representation
        super().__init__(self.health, self.representation, position)
        
    def tick(self):
        pass
        
class Sunflower(Plant):
    def __init__(self, position):
        self.representation = "🌻"
        self.health = 100
        super().__init__(self.health, self.representation, position)
        
class Peashooter(Plant):
    def __init__(self, position):
        self.representation = "🌱"
        self.health = 100
        super().__init__(self.health, self.representation, position)
        
        self.pea_cooldown = 0
    
    def tick(self):
        if self.pea_cooldown > 0:
            self.pea_cooldown -= 1
        else:
            entities.append(Pea([self.position[0] + 1, self.position[1]]))
            self.pea_cooldown = 10
        
class Wallnut(Plant):
    def __init__(self, position):
        self.representation = "🌰"
        self.health = 300
        super().__init__(self.health, self.representation, position)
        
class Pea(Entity):
    def __init__(self, position):
        self.representation = "O "
        self.health = 1
        super().__init__(self.health, self.representation, position)
        
    def tick(self):
        for entity in entities:
            if isinstance(entity, Zombie):
                if entity.position[0] == self.position[0] + 1 and entity.position[1] == self.position[1]:
                    entity.health -= 10
                    self.health = 0
                    return
        self.position[0] += 1
            
class LAWNMOWER(Entity):
    def __init__(self, position):
        self.representation = "🚜"
        self.health = 1
        super().__init__(self.health, self.representation, position)
        self.mode = "idle"
        
    def tick(self):
        for entity in entities:
            if isinstance(entity, Zombie):
                if self.mode == "idle":
                    if share_position(entity, self):
                        self.mode = "active"
                if share_position(entity, self) and self.mode == "active":
                    entity.health = 0
        if self.mode == "active":
            self.position[0] += 1
        
class Cursor:
    def __init__(self, position):
        self.position = position
        
    def move(self, x, y):
        self.position[0] += x
        self.position[1] += y
        
cursor = Cursor([0, 0])
        
# on key press, move the cursor
def on_press(key):
    if key == keyboard.Key.up:
        cursor.move(0, -1)
    elif key == keyboard.Key.down:
        cursor.move(0, 1)
    elif key == keyboard.Key.left:
        cursor.move(-1, 0)
    elif key == keyboard.Key.right:
        cursor.move(1, 0)
        
def clear_canvas(canvas):
    for row in canvas:
        for i in range(len(row)):
            row[i] = EMPTY_CHAR
            
    for row in canvas_styles:
        for i in range(len(row)):
            row[i] = None
        
def update_canvas(canvas, entities):
    clear_canvas(canvas)
    
    for entity in entities:
        entity.tick()
        
    clear_dead_entities(entities)
    clear_out_of_bounds_entities(entities)
    
    for entity in entities:
        if is_out_of_bounds(entity):
            entities.remove(entity)
            continue
        x, y = entity.position
        canvas[y][x] = entity.representation
        
    # draw cursor
    x, y = cursor.position
    canvas[y][x] = " X"
    
def reset_cursor_position(cursor_travel_count):
    if cursor_travel_count > 0:
        print("\033[A" * cursor_travel_count, end="") 
        
def print_canvas(canvas):
    console = Console()
    for row in canvas:
        console.print("".join(row), style="on green")
        
    return CANVAS_HEIGHT
        
def print_stats(sun):
    stats_str = f"☀️: {sun}" 
    print(stats_str)
    print("‾" * len(stats_str))
    
    return 2

def clear_dead_entities(entities):
    for entity in entities:
        if entity.health <= 0:
            entities.remove(entity)

def is_out_of_bounds(entity):
    return entity.position[0] < 0 or entity.position[0] >= CANVAS_WIDTH or entity.position[1] < 0 or entity.position[1] >= CANVAS_HEIGHT
            
def clear_out_of_bounds_entities(ents):
    for entity in ents:
        if is_out_of_bounds(entity):
            ents.remove(entity)

def spawn_zombie(game_tick_count):
    if game_tick_count % 27 == randint(0, 20):
        entities.append(Zombie([CANVAS_WIDTH - 1, randint(0, CANVAS_HEIGHT - 1)]))

def main():
    hide_cursor()
    
    cursor_travel_count = 0
    sun = STARTING_SUN
    game_tick_count = 0

    with keyboard.Listener(on_press=on_press) as listener:
        entities.append(Zombie([9, 2]))
        entities.append(Sunflower([1, 2]))
        entities.append(Wallnut([4, 2]))
        
        for i in range(CANVAS_HEIGHT):
            entities.append(LAWNMOWER([0, i]))
        
        for i in range(CANVAS_HEIGHT):
            entities.append(Sunflower([1, i]))
            
        for i in range(CANVAS_HEIGHT):
            entities.append(Peashooter([2, i]))
        
        for _ in range(300):
            # game events
            spawn_zombie(game_tick_count)
            update_canvas(canvas, entities)
            
            # reset
            reset_cursor_position(cursor_travel_count)
            cursor_travel_count = 0
            
            # print
            cursor_travel_count += print_stats(sun)
            cursor_travel_count += print_canvas(canvas)
            
            game_tick_count += 1
            sleep(0.2)
    
if __name__ == "__main__":
    main()
    