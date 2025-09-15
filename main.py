import os
import pygame
import csv

pygame.init()
screen = pygame.display.set_mode((1280, 870))
clock = pygame.time.Clock()
running = True

# ----------------------
# Grid settings
# ----------------------
grid_width = 12
grid_height = 9
tile_size = 90  # size of tiles in the main grid
grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

# ----------------------
# Menu settings
# ----------------------
tiles_folder = "textures"
menu_tile_size = 26   # smaller icons in menu
menu_width = 200
game_width = screen.get_width() - menu_width
menu_padding = 10
menu_cols = 2         # number of columns in the menu

# ----------------------
# CSV save/load helpers
# ----------------------
def save_grid_to_csv(filename, grid):
    with open(filename, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(grid)

def load_grid_from_csv(filename):
    loaded_grid = []
    with open(filename, mode="r") as f:
        reader = csv.reader(f)
        for row in reader:
            loaded_grid.append([int(x) for x in row])  # convert strings to ints
    return loaded_grid

# ----------------------
# Load all tile images
# ----------------------
tile_images = []
for filename in sorted(os.listdir(tiles_folder)):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        path = os.path.join(tiles_folder, filename)
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (tile_size, tile_size))
        tile_images.append(img)

# start with first tile
current_tile_type = 1

pygame.mouse.set_cursor(*pygame.cursors.broken_x)

# Main loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Save/load with keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # save to CSV
                save_grid_to_csv("level.csv", grid)
                print("✅ Grid saved to level.csv")
            elif event.key == pygame.K_l:  # load from CSV
                grid = load_grid_from_csv("level.csv")
                print("✅ Grid loaded from level.csv")

    # Handle mouse input
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    # Paint tiles on the grid
    if mouse_buttons[0] or mouse_buttons[2]:  # left or right click
        tile_x = mouse_pos[0] // tile_size
        tile_y = mouse_pos[1] // tile_size
        # ensure click is inside grid area
        if 0 <= tile_x < grid_width and 0 <= tile_y < grid_height and mouse_pos[0] < game_width:
            if mouse_buttons[0]:  # left click = paint
                grid[tile_y][tile_x] = current_tile_type
            elif mouse_buttons[2]:  # right click = erase
                grid[tile_y][tile_x] = 0

    # Select tiles from the menu
    if mouse_buttons[0] and mouse_pos[0] > game_width:  # clicked inside menu
        rel_x = mouse_pos[0] - game_width - menu_padding
        rel_y = mouse_pos[1] - menu_padding
        col = rel_x // (menu_tile_size + menu_padding)
        row = rel_y // (menu_tile_size + menu_padding)
        index = row * menu_cols + col
        if 0 <= col < menu_cols and 0 <= index < len(tile_images):
            current_tile_type = index

    # ----------------------
    # Draw everything
    # ----------------------
    screen.fill(pygame.Color("grey"))  # background

    # Draw grid with tiles
    for y in range(grid_height):
        for x in range(grid_width):
            tile_type = grid[y][x]
            if 0 <= tile_type < len(tile_images):
                screen.blit(tile_images[tile_type], (x * tile_size, y * tile_size))

            # draw grid outline
            pygame.draw.rect(
                screen,
                pygame.Color("black"),
                pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size),
                width=1
            )

    # Draw menu background
    pygame.draw.rect(screen, pygame.Color("blue"), (game_width, 0, menu_width, screen.get_height()))

    # Draw menu tiles in grid layout
    for i, tile in enumerate(tile_images):
        menu_tile = pygame.transform.scale(tile, (menu_tile_size, menu_tile_size))
        col = i % menu_cols
        row = i // menu_cols
        x = game_width + menu_padding + col * (menu_tile_size + menu_padding)
        y = menu_padding + row * (menu_tile_size + menu_padding)
        screen.blit(menu_tile, (x, y))

        # highlight selected tile
        if i == current_tile_type:
            pygame.draw.rect(screen, pygame.Color("yellow"), (x - 2, y - 2, menu_tile_size + 4, menu_tile_size + 4), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
