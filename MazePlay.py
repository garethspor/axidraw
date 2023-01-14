import random

def _count_runs(vals):
    p = 0
    r = []
    s = False
    for val in vals:
        if val and s:
            r[-1][1] += 1
        elif val and not s:
            r.append([p,1])
        s = val
        p += 1
    return r

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.make_maze()

    def print(self, squares=None):
        print('-' * (self.width * 4 + 1))
        for y in range(self.height):
            line = '|'
            for x in range(self.width):
                # line += '   ' if any([v == (x,y) for v in visited]) else '   '
                square_text = '   '
                for s in squares:
                    if s[0][0] == x and s[0][1] == y:
                        square_text = s[1]
                line += square_text
                if x < (self.width - 1) and self.h_passable[y][x]:
                    line += ' '
                else:
                    line += '|'
            print(line)
            if y < (self.height - 1):
                line = '|'
                for x in range(self.width):
                    if self.v_passable[y][x]:
                        line += '   '
                    else:
                        line += '---'
                    line += '+'
                print(line)
            else:
                print('-' * (self.width * 4 + 1))

    def make_maze(self):
        visited = []
        total_to_visit = self.width * self.height
        done = False
        self.h_passable = [[False for i in range(self.width-1)] for j in range(self.height)]
        self.v_passable = [[False for i in range(self.width)] for j in range(self.height-1)]
        while not done:
            if len(visited) == 0:
                vx = random.randint(0, self.width - 1)
                vy = random.randint(0, self.height - 1)
                visited.append((vx,vy))
                # print(f'1st pos: {vx},{vy}')
            elif len(visited) == total_to_visit:
                done = True
            else:
                chosen = False
                while not chosen:
                    vx, vy = visited[random.randint(0, len(visited) - 1)]
                    # print(f'Trying {vx},{vy}')
                    potential_neighbors = []
                    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                        pot_neighb = (vx + dx, vy + dy)
                        # print(f'pot_neighb {pot_neighb}')
                        pvx, pvy = pot_neighb
                        if pvx >= 0 and pvx < self.width and pvy >= 0 and pvy < self.height and not any([v == pot_neighb for v in visited]):
                            # print(f'pot_neighb {pot_neighb} good :)')
                            potential_neighbors.append(pot_neighb)
                    if len(potential_neighbors):
                        to_visit = potential_neighbors[random.randint(0, len(potential_neighbors) - 1)]
                        # print(f'connecteing {vx},{vy} to {to_visit}')
                        visited.append(to_visit)
                        upper_left_pos = (min(vx, to_visit[0]), min(vy, to_visit[1]))
                        # print(f'upper_left_pos: {upper_left_pos}')
                        if vx != to_visit[0]:
                            # horizontal move
                            self.h_passable[upper_left_pos[1]][upper_left_pos[0]] = True
                        else:
                            self.v_passable[upper_left_pos[1]][upper_left_pos[0]] = True
                        chosen = True
            # print_maze(self.width, self.height, visited, self.h_passable, self.v_passable)
        # furthest_point_from(0,0, self.width, self.height, h_passable, self.v_passable)


    def segments(self):
        segs = [((0,0), (self.width,0)), ((self.width,0), (self.width,self.height)), ((self.width,self.height), (0,self.height)), ((0,self.height), (0,0))]
        for y in range(self.height-1):
            vals = [not self.v_passable[y][x] for x in range(self.width)]
            for run_start, run_length in _count_runs(vals):
                segs.append(((run_start,y+1), (run_start+run_length,y+1)))
        for x in range(self.width-1):
            vals = [not self.h_passable[y][x] for y in range(self.height)]
            for run_start, run_length in _count_runs(vals):
                segs.append(((x+1,run_start), (x+1, run_start+run_length)))
        return segs

    def _visit(self, origin_x, origin_y, distances, val=0):
        distances[origin_y][origin_x] = -1 if val == 0 else val
        val += 1
        if origin_x > 0 and self.h_passable[origin_y][origin_x-1] and distances[origin_y][origin_x-1] == 0:
            self._visit(origin_x - 1, origin_y, distances, val)
        if origin_x < (self.width-1) and self.h_passable[origin_y][origin_x] and distances[origin_y][origin_x+1] == 0:
            self._visit(origin_x + 1, origin_y, distances, val)
        if origin_y > 0 and self.v_passable[origin_y-1][origin_x] and distances[origin_y-1][origin_x] == 0:
            self._visit(origin_x, origin_y - 1, distances, val)
        if origin_y < (self.height-1) and self.v_passable[origin_y][origin_x] and distances[origin_y+1][origin_x] == 0:
            self._visit(origin_x, origin_y + 1, distances, val)

    def furthest_point_from(self, origin_x, origin_y):
        distances = [[0 for i in range(self.width)] for j in range(self.height)]
        self._visit(origin_x, origin_y, distances)

        for row_vals in distances:
            print(', '.join([str(v) for v in row_vals]))

        max_row_vals = [max(row_vals) for row_vals in distances]
        max_dist = max(max_row_vals)
        print(f'max_dist: {max_dist}')

        max_y = max_row_vals.index(max_dist)
        max_x = distances[max_y].index(max_dist)
        return max_x, max_y






if __name__ == "__main__":
    maze = Maze(17,17)
    for start_x,start_y in [(0,0),(8,8),(16,16)]:
        finish_x,finish_y = maze.furthest_point_from(start_x, start_y)
        maze.print([((start_x,start_y), ' S '), ((finish_x,finish_y), ' F ')])
