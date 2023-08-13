import pygame
import math

cell_size=50
observer_pos = []
viewpoint_pos = []
intersects = []

#Initalize Pygame
pygame.init()

#Create Window with custom title
screen = pygame.display.set_mode((1000, 750))
pygame.display.set_caption("Hello World")

def draw_line(x1,y1,x2,y2,color):
    pygame.draw.line(screen,color,(x1*cell_size+cell_size,y1*cell_size+cell_size),(x2*cell_size+cell_size,y2*cell_size+cell_size),1)

def draw_grid():
    for x in range(19):
        draw_line(x,0,x,13,pygame.Color("white"))
    for y in range(14):
        draw_line(0,y,18,y,pygame.Color("white"))

def draw_observer(x1,y1):
    pygame.draw.circle(screen,pygame.Color("red"),(x1*cell_size+cell_size,y1*cell_size+cell_size),10)

def draw_viewpoint(x1,y1):
    pygame.draw.circle(screen,pygame.Color("green"),(x1*cell_size+cell_size,y1*cell_size+cell_size),10)

def draw_intersect(x1,y1):
    pygame.draw.circle(screen,pygame.Color("blue"),(x1*cell_size+cell_size,y1*cell_size+cell_size),5)

# draw line of seight
def draw_los(x1,y1,x2,y2):
    pygame.draw.line(screen,pygame.Color("yellow"),(x1*cell_size+cell_size,y1*cell_size+cell_size),(x2*cell_size+cell_size,y2*cell_size+cell_size),1)

def get_grid_coordinates(x,y):
    cx = (x - cell_size) / cell_size
    cy = (y - cell_size) / cell_size
    return cx,cy

def draw_scene():
    screen.fill((0,0,0))
    draw_grid()
    if len(observer_pos) == 2:
        draw_observer(observer_pos[0],observer_pos[1])
    if len(viewpoint_pos) == 2:
        draw_viewpoint(viewpoint_pos[0],viewpoint_pos[1])
        draw_los(observer_pos[0],observer_pos[1],viewpoint_pos[0],viewpoint_pos[1])

    for inter in intersects:
        draw_intersect(inter[0],inter[1])

    pygame.display.update()

def do_raycast():
    # still an error if dx or dy are 0

    print("--- RAYCAST ----------------")
    print("Observer: ",observer_pos)
    print("Viewpoint: ",viewpoint_pos)
    x = observer_pos[0]
    y = observer_pos[1]

    dx = viewpoint_pos[0] - observer_pos[0]
    dy = viewpoint_pos[1] - observer_pos[1]
    c = math.sqrt(dx**2+dy**2)
    ex = dx/c
    ey = dy/c
    sx = math.sqrt(1 + (dy/dx)**2) if dx !=0 else float(0)
    sy = math.sqrt(1 + (dx/dy)**2) if dy !=0 else float(0)
    vx = ex/abs(ex) if ex != 0 else 0
    vy = ey/abs(ey) if ey != 0 else 0

    print(f"dx,dy: {dx:.3}, {dy:.3}")
    print(f"ex,ex: {ex:.3}, {ex:.3}")
    print(f"sx,sy: {sx:.3}, {sy:.3}")
    print(f"vx,vy: {vx}, {vy}")
    print(f"c: {c:.3}")

    i = 0
    while i < 6:
        nx = math.floor(x+vx) if vx >= 0 else math.ceil(x+vx)
        ny = math.floor(y+vy) if vy >= 0 else math.ceil(y+vy)
        print(f"nx,ny: {nx}, {ny}")

        lenx = (nx - x) * sx
        leny = (ny - y) * sy
        print(f"lenx,leny: {lenx:.3}, {leny:.3}")

        if abs(lenx) <= abs(leny):
            x = nx
            y = y + ey * lenx * vx
            print(f"nextx,nexty: {x}, {y:.3}")
        else:
            x = x + ex * leny * vy
            y = ny
            print(f"nextx,nexty: {x:.3}, {y}")

        intersects.append([x,y])
        i += 1

    return

draw_scene()  

#Record events to stop the script on close
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx,my = pygame.mouse.get_pos()
            cx,cy = get_grid_coordinates(mx,my)
            if len(observer_pos) == 2 and len(viewpoint_pos) == 0:
                viewpoint_pos = [cx,cy]
                do_raycast()
            elif len(observer_pos) != 2 or len(viewpoint_pos) == 2:
                observer_pos = [cx,cy]
                viewpoint_pos.clear()
                intersects.clear()

            draw_scene()

        elif event.type == pygame.QUIT:
            pygame.quit()
            run = False
