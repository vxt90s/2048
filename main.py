import pygame
import random
import math

pygame.init()

FPS = 60
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 4, 4
RECT_HEIGHT = HEIGHT // ROWS
RECT_WIDTH = WIDTH // COLS

OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)
FONT_COLOR_LIGHT = (249, 246, 242)

FONT_NAME = pygame.font.match_font("comicsans")
MOVE_VEL = 25 # Slightly faster for smoother feel

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

class Tile:
    # UPDATED: The first color (for 2) is now much brighter
    COLORS = [
        (255, 248, 240), # Brightened 2
        (238, 228, 218), # 4
        (237, 224, 200), # 8
        (242, 177, 121), # 16
        (245, 149, 99),  # 32
        (246, 124, 95),  # 64
        (246, 94, 59),   # 128
        (237, 207, 114), # 256
        (237, 204, 97),  # 512
        (237, 200, 80),  # 1024
        (237, 197, 63),  # 2048
        (237, 194, 46),  # 4096
        (60, 58, 50)     # 8192+
    ]

    TEXT_COLORS = {2: FONT_COLOR, 4: FONT_COLOR}

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT

    def get_color(self):
        color_index = int(math.log2(self.value)) - 1
        if color_index < 0: color_index = 0
        if color_index >= len(self.COLORS): color_index = len(self.COLORS) - 1
        return self.COLORS[color_index]

    def get_text_color(self):
        return self.TEXT_COLORS.get(self.value, FONT_COLOR_LIGHT)

    def draw(self, window):
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))
        
        font_size = 60
        if self.value > 512: font_size = 50
        if self.value > 1024: font_size = 40

        font = pygame.font.Font(FONT_NAME, font_size)
        text = font.render(str(self.value), 1, self.get_text_color())
        window.blit(text, (
            self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
            self.y + (RECT_HEIGHT / 2 - text.get_height() / 2),
        ))

    def set_pos(self, ceil=False):
        self.row = math.ceil(self.y / RECT_HEIGHT) if ceil else math.floor(self.y / RECT_HEIGHT)
        self.col = math.ceil(self.x / RECT_WIDTH) if ceil else math.floor(self.x / RECT_WIDTH)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]

def draw_grid(window):
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)
    for col in range(1, COLS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)
    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)

def draw(window, tiles, game_state, score):
    window.fill(BACKGROUND_COLOR)
    for tile in tiles.values():
        tile.draw(window)
    draw_grid(window)

    if game_state == "lost":
        # Create overlay surface
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((255, 255, 255))
        window.blit(overlay, (0, 0))

        font = pygame.font.Font(FONT_NAME, 60)
        # Draw text
        texts = [
            font.render("Game Over!", True, (119, 110, 101)),
            font.render(f"Score: {score}", True, (119, 110, 101)),
            font.render("Press 'R' to Restart", True, (119, 110, 101))
        ]
        
        for i, text_surf in enumerate(texts):
            window.blit(text_surf, (WIDTH/2 - text_surf.get_width()/2, HEIGHT/2 - 100 + (i * 100)))

    pygame.display.update()

def get_random_pos(tiles):
    empty_cells = [(r, c) for r in range(ROWS) for c in range(COLS) if f"{r}{c}" not in tiles]
    return random.choice(empty_cells) if empty_cells else None

def move_tiles(window, tiles, clock, direction, score):
    updated = True
    blocks = set()
    moved = False

    if direction == "left":
        sort_func, reverse, delta, ceil = lambda x: x.col, False, (-MOVE_VEL, 0), True
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, nt: tile.x > nt.x + MOVE_VEL
        move_check = lambda tile, nt: tile.x > nt.x + RECT_WIDTH + MOVE_VEL
    elif direction == "right":
        sort_func, reverse, delta, ceil = lambda x: x.col, True, (MOVE_VEL, 0), False
        boundary_check = lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, nt: tile.x < nt.x - MOVE_VEL
        move_check = lambda tile, nt: tile.x + RECT_WIDTH + MOVE_VEL < nt.x
    elif direction == "up":
        sort_func, reverse, delta, ceil = lambda x: x.row, False, (0, -MOVE_VEL), True
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, nt: tile.y > nt.y + MOVE_VEL
        move_check = lambda tile, nt: tile.y > nt.y + RECT_HEIGHT + MOVE_VEL
    elif direction == "down":
        sort_func, reverse, delta, ceil = lambda x: x.row, True, (0, MOVE_VEL), False
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, nt: tile.y < nt.y - MOVE_VEL
        move_check = lambda tile, nt: tile.y + RECT_HEIGHT + MOVE_VEL < nt.y

    while updated:
        clock.tick(FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile): continue
            next_tile = get_next_tile(tile)
            
            if not next_tile:
                tile.move(delta)
                moved = True
            elif tile.value == next_tile.value and tile not in blocks and next_tile not in blocks:
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    next_tile.value *= 2
                    score += next_tile.value
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
                    moved = True
            elif move_check(tile, next_tile):
                tile.move(delta)
                moved = True
            else: continue

            tile.set_pos(ceil)
            updated = True
        
        # Clear tiles and re-populate for current frame
        tiles.clear()
        for t in sorted_tiles: tiles[f"{t.row}{t.col}"] = t
        draw(window, tiles, "continue", score)

    return score, end_move(tiles) if moved else "continue"

def end_move(tiles):
    pos = get_random_pos(tiles)
    if pos:
        r, c = pos
        tiles[f"{r}{c}"] = Tile(random.choice([2, 4]), r, c)
    
    if len(tiles) == 16 and is_game_over(tiles):
        return "lost"
    return "continue"

def is_game_over(tiles):
    for r in range(ROWS):
        for c in range(COLS):
            curr = tiles.get(f"{r}{c}")
            if not curr: return False
            for dr, dc in [(0, 1), (1, 0)]:
                neighbor = tiles.get(f"{r+dr}{c+dc}")
                if neighbor and neighbor.value == curr.value: return False
    return True

def main(window):
    clock = pygame.time.Clock()
    run = True
    tiles = {f"{r}{c}": Tile(2, r, c) for r, c in [get_random_pos({}), get_random_pos({})]}
    game_state, score = "continue", 0

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if game_state == "lost" and event.key == pygame.K_r:
                    tiles = {f"{r}{c}": Tile(2, r, c) for r, c in [get_random_pos({}), get_random_pos({})]}
                    game_state, score = "continue", 0
                elif game_state == "continue":
                    old_score = score
                    if event.key == pygame.K_LEFT: score, game_state = move_tiles(window, tiles, clock, "left", score)
                    elif event.key == pygame.K_RIGHT: score, game_state = move_tiles(window, tiles, clock, "right", score)
                    elif event.key == pygame.K_UP: score, game_state = move_tiles(window, tiles, clock, "up", score)
                    elif event.key == pygame.K_DOWN: score, game_state = move_tiles(window, tiles, clock, "down", score)
                    pygame.display.set_caption(f"2048 | Score: {score}")

        draw(window, tiles, game_state, score)
    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)