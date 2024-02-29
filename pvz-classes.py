

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
        self.representation = "O "
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
 