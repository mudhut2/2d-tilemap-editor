import pygame
import csv

# -------------------
# Setup
# -------------------
pygame.init()
screen = pygame.display.set_mode((1280, 870))
clock = pygame.time.Clock()
running = True

grid_width = 20
grid_height = 15
tile_size = 48
grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

empty_tile = pygame.transform.scale(pygame.image.load("textures/bottom.png"), (tile_size, tile_size))
floor_tile = pygame.transform.scale(pygame.image.load("textures/golgTex.jpg"), (tile_size, tile_size))
wall_tile  = pygame.transform.scale(pygame.image.load("textures/ancient-wall1.jpg"),  (tile_size, tile_size))

# Map tile types to colors
tile_types = {
    0: empty_tile, # empty
    1: floor_tile,  # wall
    2: wall_tile,   # water
}
current_tile_type = 1  # start with "wall" for painting
pygame.mouse.set_cursor(*pygame.cursors.broken_x)

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Change current tile type with number keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                current_tile_type = 0
            elif event.key == pygame.K_1:
                current_tile_type = 1
            elif event.key == pygame.K_2:
                current_tile_type = 2


    # Handle mouse input
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0] or mouse_buttons[2]:  # left or right click
        mouse_pos = pygame.mouse.get_pos()
        tile_x = mouse_pos[0] // tile_size
        tile_y = mouse_pos[1] // tile_size
        # ensure click is inside grid
        if 0 <= tile_x < grid_width and 0 <= tile_y < grid_height:
            if mouse_buttons[0]:  # left click
                grid[tile_y][tile_x] = current_tile_type
            elif mouse_buttons[2]:  # right click
                grid[tile_y][tile_x] = 0  # erase tile
    # Draw grid
    screen.fill(pygame.Color("orange"))  # background
    for y in range(grid_height):
        for x in range(grid_width):
            tile_type = grid[y][x]
            if tile_type != 0:
                screen.blit(tile_types[tile_type], (x * tile_size, y * tile_size))
            pygame.draw.rect(
                screen,
                pygame.Color("grey"),
                pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size),
                width=1,  # outline thickness
                border_radius=2  # rounded corners (optional)
            )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
