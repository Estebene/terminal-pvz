from rich import print
from time import sleep
from pynput import keyboard

CANVAS_HEIGHT = 5
CANVAS_WIDTH = 10

canvas = [[" " for _ in range(CANVAS_WIDTH)] for _ in range(CANVAS_HEIGHT)]

entities = []

class Entity:
    def __init__(self, health, representation, position):
        self.health = health
        self.representation = representation
        self.position: list[int] = position

class Zombie(Entity):
    def __init__(self, position):
        self.representation = "🧟"
        self.health = 100
        super().__init__(self.health, self.representation, position)
    
    def tick(self):
        blocked = False
        for entity in entities:
            if isinstance(entity, Plant):
                if entity.position[0] == self.position[0] - 1:
                    blocked = True
                    entity.health -= 10
                    if entity.health <= 0:
                        entities.remove(entity) 
        if not blocked:      
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
        

        
def clear_canvas(canvas):
    for row in canvas:
        for i in range(len(row)):
            row[i] = " "
    
        
def update_canvas(canvas, entities):
    clear_canvas(canvas)
    
    for entity in entities:
        x, y = entity.position
        canvas[y][x] = entity.representation
        entity.tick()
        
def print_canvas(canvas):
    # clear the terminal
    print("\033c", end="")
    for row in canvas:
        print("".join(row))

def main():
    
    
    entities.append(Zombie([9, 2]))
    entities.append(Sunflower([0, 2]))
    entities.append(Peashooter([2, 2]))
    entities.append(Wallnut([4, 2]))
    entities.append(Pea([3, 2]))
    
    for _ in range(10):
        update_canvas(canvas, entities)
        print_canvas(canvas)
        sleep(1)
        print("\n" * CANVAS_HEIGHT)
    
if __name__ == "__main__":
    main()
    