# from rich import print
from time import sleep
from pynput import keyboard
from cursor_utils import hide_cursor, show_cursor

CANVAS_HEIGHT = 5
CANVAS_WIDTH = 10
EMPTY_CHAR = "  "

STARTING_SUN = 50

canvas = [[EMPTY_CHAR for _ in range(CANVAS_WIDTH)] for _ in range(CANVAS_HEIGHT)]

entities = []

global cursor_travel_count
cursor_travel_count = 0

global sun
sun = STARTING_SUN

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
                if entity.position[0] == self.position[0] - 1:
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
        
class Wallnut(Plant):
    def __init__(self, position):
        self.representation = "🌰"
        self.health = 100
        super().__init__(self.health, self.representation, position)
        
class Pea(Entity):
    def __init__(self, position):
        self.representation = "⬤"
        self.health = -1
        super().__init__(self.health, self.representation, position)
        
    def tick(self):
        for entity in entities:
            if isinstance(entity, Zombie):
                if entity.position[0] == self.position[0] + 1:
                    entity.health -= 10
                    if entity.health <= 0:
                        entities.remove(entity) 
                    entities.remove(self)
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
    
        
def update_canvas(canvas, entities):
    clear_canvas(canvas)
    
    for entity in entities:
        x, y = entity.position
        canvas[y][x] = entity.representation
        entity.tick()
        
    # draw cursor
    x, y = cursor.position
    canvas[y][x] = " X"
    
def reset_cursor_position():
    print("\033[A" * cursor_travel_count, end="") 
        
def print_canvas(canvas):
    # print("\033c", end="")
    
    cursor_travel_count = cursor_travel_count + CANVAS_HEIGHT
    
    for row in canvas:
        print("".join(row))
        
def print_stats(sun):
    stats_str = f"☀️: {sun}" 
    print(stats_str)
    print("‾" * len(stats_str))

def main():
    hide_cursor()    
    
    with keyboard.Listener(on_press=on_press) as listener:
        entities.append(Zombie([9, 2]))
        entities.append(Sunflower([0, 2]))
        entities.append(Peashooter([2, 2]))
        entities.append(Wallnut([4, 2]))
        entities.append(Pea([3, 2]))
        
        for _ in range(100):
            update_canvas(canvas, entities)
            print_stats(sun)
            print_canvas(canvas)
            sleep(0.2)
    
if __name__ == "__main__":
    main()
    