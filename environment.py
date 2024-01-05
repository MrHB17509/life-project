class Hexagon:
    def __init__(self, x, y, biome):
        self.x = x
        self.y = y
        self.biome = biome

class Environment:
    def __init__(self, width, height, hex_size):
        self.width = width
        self.height = height
        self.hex_size = hex_size
        self.hex_grid = self.create_hex_grid()

    def create_hex_grid(self):
        grid = []
        vertical_distance = self.hex_size * 3**0.5
        horizontal_distance = self.hex_size * 1.5
        for row in range(self.height):
            for col in range(self.width):
                x = col * horizontal_distance + (row % 2) * (horizontal_distance / 2)
                y = row * vertical_distance * 0.75
                biome = self.determine_biome(x, y)
                grid.append(Hexagon(x, y, biome))
        return grid

    def determine_biome(self, x, y):
        if y < self.height / 3:
            return "desert" if x % 2 == 0 else "grassland"
        elif y < 2 * self.height / 3:
            return "forest" if x % 2 == 0 else "mountain"
        else:
            return "tundra" if x % 2 == 0 else "swamp"

    def get_biome_at(self, x, y):
        closest_hex = min(self.hex_grid, key=lambda hex: (hex.x - x)**2 + (hex.y - y)**2)
        return closest_hex.biome
