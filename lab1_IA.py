import heapq

#  Эта функция создает сетку (grid) заданных размеров и заполняет ее блоками, 
#  каждый из которых имеет уникальный идентификатор (block_id).
def initialize_world(size_x, size_y, num_blocks):
    grid = [[[] for _ in range(size_x)] for _ in range(size_y)]
    blocks = {}
    for _ in range(num_blocks):
        block_id = input("Enter the cube ID:")
        x = int(input(f"Enter the X coordinate for the cube {block_id}: "))
        y = int(input(f"Enter the Y coordinate for the cube {block_id}: "))
        grid[y][x].append(block_id)
        blocks[block_id] = (x, y)
    return grid, blocks

# Это функция, которая возвращает эвристическую оценку расстояния между двумя 
# точками на сетке. В данном случае используется манхэттенское расстояние.
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Это реализация алгоритма A*. Он ищет кратчайший путь от начальной точки (start)
# до конечной точки (end) на сетке, используя эвристическую оценку (heuristic) для оценки расстояния.
def a_star(grid, start, end):
    directions = [(0, 1, 'up'), (1, 0, 'right'), (0, -1, 'down'), (-1, 0, 'left')]
    queue = [(0 + heuristic(start, end), 0, start, [])]
    visited = set()
    while queue:
        _, cost, current, path = heapq.heappop(queue)
        if current == end:
            return path
        if current in visited:
            continue
        visited.add(current)
        for dx, dy, direction in directions: 
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and not grid[ny][nx] and (nx, ny) not in visited:
                heapq.heappush(queue, (cost + heuristic((nx, ny), end), cost + 1, (nx, ny), path + [direction]))
    return []

# Эта функция перемещает блок из начальной позиции в целевую позицию, используя алгоритм A*. Если путь найден, 
# блок перемещается и его новая позиция отображается. Если путь не найден, блок остается на месте.
def move_block(grid, blocks, block_id, target):
    if block_id not in blocks:
        print("Cube not found")
        return
    start = blocks[block_id]
    grid[start[1]][start[0]].remove(block_id)
    path = a_star(grid, start, target)
    if path:
        print(f"Cube {block_id} was moved: " + ", ".join(path))
        grid[target[1]][target[0]].append(block_id)
        blocks[block_id] = target
    else:
        print("Path not found.")
        grid[start[1]][start[0]].append(block_id)

size_x, size_y = 5, 5
num_blocks = int(input("How many cubes will be in your program? "))
grid, blocks = initialize_world(size_x, size_y, num_blocks)

# В этом цикле пользователь указывает идентификатор блока, который он хочет переместить, 
# а также целевые координаты. Затем вызывается функция move_block для перемещения блока,
# и после этого отображается конечное расположение всех блоков на сетке.
while True:
    block_id = input("Which cube should I move? ")
    if block_id == 'quit':
        break
    target_x = int(input("End X coordinate: "))
    target_y = int(input("End Y coordinate: "))
    move_block(grid, blocks, block_id, (target_x, target_y))

    print("\nFinal position of the cubes")
    for y in range(size_y - 1, -1, -1):
        for x in range(size_x):
            cell = grid[y][x]
            if cell:
                print(cell[-1], end=' ')
            else:
                print('%', end=' ')
        print()