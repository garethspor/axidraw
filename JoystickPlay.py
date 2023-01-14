import pygame
import math
import time
from pyaxidraw import axidraw
import MazePlay

pygame.init()


# assumes line segments are stored in the format [(x0,y0),(x1,y1)]
def intersects(s0,s1):
    dx0 = s0[1][0]-s0[0][0]
    dx1 = s1[1][0]-s1[0][0]
    dy0 = s0[1][1]-s0[0][1]
    dy1 = s1[1][1]-s1[0][1]
    p0 = dy1*(s1[1][0]-s0[0][0]) - dx1*(s1[1][1]-s0[0][1])
    p1 = dy1*(s1[1][0]-s0[1][0]) - dx1*(s1[1][1]-s0[1][1])
    p2 = dy0*(s0[1][0]-s1[0][0]) - dx0*(s0[1][1]-s1[0][1])
    p3 = dy0*(s0[1][0]-s1[1][0]) - dx0*(s0[1][1]-s1[1][1])
    return (p0*p1<=0) & (p2*p3<=0)


class Drawer:
    def __init__(self, ad, screen):
        self.ad = ad
        self.screen = screen

        self.pos = (0, 0)
        self.step = 1
        self.max_x = 20
        self.max_y = 20
        self.down = False
        self.linewidth = 1
        self.screen_scale = 40.0
        self.barriers = []
        self.goals = []
        self.celebrated = []

    def add_barrier(self, p1, p2):
        if self.ad:
            self.ad.moveto(p1[0], p1[1])
            self.ad.lineto(p2[0], p2[1])
        self.barriers.append((p1, p2))
        self._drawlineonscreen(p1,p2,(0,0,0))

    def draw_drive(self, points, color):
        if self.ad:
            self.ad.moveto(points[0][0], points[0][1])
        for i in range(1, len(points)):
            if self.ad:
                self.ad.lineto(points[i][0], points[i][1])
            self._drawlineonscreen(points[i-1], points[i], color)

    def add_goal(self, gx, gy, rad=0.4, num_steps=10):
        self.goals.append((gx,gy,rad))
        thetas = [i * math.pi * 2 / num_steps for i in range(num_steps + 1)]
        x_vals = [gx + rad * math.cos(th) for th in thetas]
        y_vals = [gy + rad * math.sin(th) for th in thetas]
        points = [p for p in zip(x_vals,y_vals)]
        self.draw_drive(points, (128, 0, 255))

    def celebrate(self, goal_index):
        self.celebrated.append(goal_index)
        gx,gy,grad = self.goals[goal_index]
        num_steps = 5
        thetas = [i * math.pi * 4 / num_steps for i in range(num_steps+1)]
        dgx = self.pos[0]-gx
        dgy = self.pos[1]-gy
        pen_theta = math.atan2(dgy, dgx)
        pen_dist = max(math.sqrt(dgx**2+dgy**2), grad)
        x_vals = [gx + pen_dist * math.cos(th+pen_theta) for th in thetas]
        y_vals = [gy + pen_dist * math.sin(th+pen_theta) for th in thetas]
        points = [p for p in zip(x_vals,y_vals)]
        self.draw_drive(points, (255, 0, 128))
        if len(self.goals) == len(self.celebrated):
            self.gohome()


    def _barriersintersected(self, p1, p2):
        for barrier in self.barriers:
            if intersects((p1, p2), barrier):
                return True
        return False

    def toggle_up_down(self):
        self.down = not self.down
        print(f'down: {self.down}')
        if self.ad:
            if self.down:
                self.ad.pendown()
            else:
                self.ad.penup()

    def _drawlineonscreen(self, p1, p2, color):
        p1 = (self.screen_scale * p1[0], self.screen_scale * p1[1])
        p2 = (self.screen_scale * p2[0], self.screen_scale * p2[1])
        pygame.draw.line(self.screen, color, p1, p2, width=self.linewidth)

    def _screenlineto(self, x, y, down):
        p1 = (self.screen_scale * self.pos[0], self.screen_scale * self.pos[1])
        p2 = (self.screen_scale * x, self.screen_scale * y)
        linecolor = (255, 128, 0) if down else (200,200,200)
        pygame.draw.line(self.screen, linecolor, p1, p2, width=self.linewidth)

    def move(self, dx, dy):
        px = self.pos[0] + dx * self.step
        py = self.pos[1] + dy * self.step
        legal = px >=0 and px <= self.max_x and py >=0 and py <= self.max_y and not self._barriersintersected(self.pos, (px, py))
        if legal:
            if self.down:
                # print('draw to')
                if self.ad:
                    self.ad.lineto(px, py)
                self._screenlineto(px, py, self.down)
            else:
                # print('move to')
                if self.ad:
                    self.ad.moveto(px, py)
                self._screenlineto(px, py, self.down)
            self.pos = (px, py)
        goal_index = None
        for i in range(len(self.goals)):
            if any(g==i for g in self.celebrated):
                continue
            gx,gy,grad = self.goals[i]
            if math.sqrt((px-gx)**2 + (py-gy)**2) < grad:
                goal_index = i
                break

        return legal, goal_index

    def gohome(self):
        print('goin home')
        self.pos = (0, 0)
        if self.ad:
            self.ad.penup()
            self.ad.moveto(0,0)

    def go_to_start(self, sx, sy):
        print('goin to start')
        self.pos = (sx, sy)
        if self.ad:
            self.ad.penup()
            self.ad.moveto(sx,sy)

    def stop(self):
        pass


def init_axidraw():
    ad = axidraw.AxiDraw()
    ad.interactive()
    if ad.connect():
        ad.options.units = 1
        ad.options.speed_penup = 100
        ad.options.speed_pendown = 100
        ad.options.pen_pos_up = 50
        ad.options.pen_pos_down = 20
        ad.update()
        return ad

    print("No robot :-(")
    return None


def racecar_main():
    ad = init_axidraw()
    screen = pygame.display.set_mode((800,800))
    pygame.display.set_caption("Maze")
    screen.fill((255, 255, 255))
    drawer = Drawer(ad, screen)

    num_steps = 15
    thetas = [i * math.pi * 2 / num_steps for i in range(num_steps+1)]
    orx = 10
    ory = 7
    irx = 5
    iry = 3
    center_x = 10
    center_y = 10
    outer_xpos = [center_x + orx * math.cos(th) for th in thetas]
    outer_ypos = [center_y + ory * math.sin(th) for th in thetas]
    inner_xpos = [center_x + irx * math.cos(th) for th in thetas]
    inner_ypos = [center_y + iry * math.sin(th) for th in thetas]
    for i in range(1, num_steps):
        bp1 = (outer_xpos[i], outer_ypos[i])
        bp2 = (outer_xpos[i+1], outer_ypos[i+1])
        drawer.add_barrier(bp1, bp2)
    for i in range(1, num_steps):
        bp1 = (inner_xpos[i], inner_ypos[i])
        bp2 = (inner_xpos[i+1], inner_ypos[i+1])
        drawer.add_barrier(bp1, bp2)

    pen_start_x, pen_start_y = (10,5)

    drawer.go_to_start(pen_start_x, pen_start_y)
    drawer.toggle_up_down()

    pygame.display.flip()

    clock = pygame.time.Clock()

    joysticks = {}

    while len(joysticks) == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.
            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")
        if len(joysticks) == 0:
            input('joysticks?')

    done = False
    direction = 0
    velocity = 0
    steering_multiplier = 0.05
    acceleration_multiplier = 0.005
    max_velocity = 0.1
    if ad:
        steering_multiplier *= 4
        acceleration_multiplier *= 4
        max_velocity *= 4
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")
            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

        if len(joysticks):
            print(f'axis_{0}: {joysticks[0].get_axis(0)}  axis_{5}: {joysticks[0].get_axis(5)}')
            steering = joysticks[0].get_axis(0)
            acceleration = joysticks[0].get_axis(5) * acceleration_multiplier
            direction += steering * steering_multiplier
            if velocity < 0:
                if acceleration > 0:
                    velocity += abs(acceleration)
            else:
                velocity += acceleration
                velocity = max(0, velocity)

            velocity = min(max_velocity, velocity)
            print(f'dir: {180*direction/math.pi}, velocity: {velocity}')
            motion_vector = (velocity * math.cos(direction), velocity * math.sin(direction))
            legal, goal_index = drawer.move(motion_vector[0], motion_vector[1])
            if not legal:
                joysticks[1].rumble(0,1,500)
                velocity = -0.2 * velocity
                time.sleep(0.5)
            if goal_index is not None:
                print(f'GOAL!! {goal_index}')
                drawer.celebrate(goal_index)

        clock.tick(30)
        pygame.display.flip()
    print('Bye')
    drawer.gohome()
    drawer.stop()







def maze_main():

    joysticks = {}

    while len(joysticks) == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.
            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")
        if len(joysticks) == 0:
            input('joysticks?')

    ad = init_axidraw()
    screen = pygame.display.set_mode((800,800))
    pygame.display.set_caption("Maze")
    screen.fill((255, 255, 255))
    drawer = Drawer(ad, screen)

    maze_width = 13
    maze_height = 13
    maze = MazePlay.Maze(maze_width, maze_height)
    maze_segments = maze.segments()
    maze_scale = 16.0 / maze_width
    maze_x_offset = 2
    maze_y_offset = 2
    for segment in maze_segments:
        bp1 = (segment[0][0] * maze_scale + maze_x_offset, segment[0][1] * maze_scale + maze_y_offset)
        bp2 = (segment[1][0] * maze_scale + maze_x_offset, segment[1][1] * maze_scale + maze_y_offset)
        drawer.add_barrier(bp1, bp2)

    maze_start_x, maze_start_y = (0,0)
    pen_start_x = maze_x_offset + maze_scale * (maze_start_x+0.5)
    pen_start_y = maze_y_offset + maze_scale * (maze_start_y+0.5)
    maze_finish_x, maze_finish_y = maze.furthest_point_from(maze_start_x, maze_start_y)
    # drawer.add_goal(pen_start_x + maze_scale, pen_start_y + maze_scale, rad=maze_scale*0.4)
    drawer.add_goal(maze_x_offset + maze_scale * (maze_finish_x+0.5), maze_y_offset + maze_scale * (maze_finish_y+0.5), rad=maze_scale*0.4)
    print(f'maze_finish {maze_finish_x},{maze_finish_y}')

    drawer.go_to_start(pen_start_x, pen_start_y)
    drawer.toggle_up_down()

    pygame.display.flip()

    clock = pygame.time.Clock()

    done = False
    while not done:
        # Event processing step.
        # Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED
        direction_vec = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.

            # if event.type == pygame.JOYHATMOTION:
            #     direction_vec = (event.value[0], -event.value[1])

            if event.type == pygame.JOYBUTTONDOWN:
                if event.instance_id == 0:
                    print(f"Joystick button pressed event.button: {event.button}")
                    if event.button == 0:
                        drawer.toggle_up_down()

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")

            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

        if direction_vec is None:
            if len(joysticks):
                dx = joysticks[0].get_axis(0)
                dy = joysticks[0].get_axis(1)
                if (dx**2+dy**2) > 0.25:
                    speed = 0.2 if ad else 0.035
                    axis_dir = math.atan2(dy,dx)
                    dx = math.cos(axis_dir) * speed
                    dy = math.sin(axis_dir) * speed
                    direction_vec = (dx, dy)

        if direction_vec is not None:
            legal, goal_index = drawer.move(direction_vec[0], direction_vec[1])
            if not legal:
                joysticks[1].rumble(0,1,500)
                time.sleep(0.5)
            if goal_index is not None:
                print(f'GOAL!! {goal_index}')
                drawer.celebrate(goal_index)

            # Limit to 30 frames per second.
        clock.tick(30)
        pygame.display.flip()
    print('Bye')
    drawer.gohome()
    drawer.stop()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='GameController experiments')
    parser.add_argument('game', help='game to play')
    args = parser.parse_args()

    if args.game == 'maze':
        maze_main()
    elif args.game == 'racecar':
        racecar_main()

    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()
