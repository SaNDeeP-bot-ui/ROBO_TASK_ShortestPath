from collections import deque

def min_moves_to_collect_artifacts(building_map):
    rows = len(building_map)
    cols = len(building_map[0])
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    start = None
    total_keys = 0  # Bitmask to represent all artifacts we need
    
    # First pass to find start position and collect artifact bitmask
    for r in range(rows):
        for c in range(cols):
            cell = building_map[r][c]
            if cell == '@':
                start = (r, c)
            elif 'a' <= cell <= 'g':
                total_keys |= (1 << (ord(cell) - ord('a')))
    
    # BFS queue: (x, y, collected_mask, steps)
    queue = deque([(start[0], start[1], 0, 0)])
    visited = set([(start[0], start[1], 0)])
    
    while queue:
        x, y, keys, steps = queue.popleft()
        
        # Check if all artifacts are collected
        if keys == total_keys:
            return steps
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < rows and 0 <= ny < cols:
                cell = building_map[nx][ny]
                new_keys = keys
                
                if cell == '#':
                    continue  # wall
                
                # Door logic
                if 'A' <= cell <= 'G':
                    required_key_bit = 1 << (ord(cell.lower()) - ord('a'))
                    if not (keys & required_key_bit):
                        continue  # can't pass the door
                
                # Artifact collection
                if 'a' <= cell <= 'g':
                    new_keys |= (1 << (ord(cell) - ord('a')))
                
                # Visit only new states
                if (nx, ny, new_keys) not in visited:
                    visited.add((nx, ny, new_keys))
                    queue.append((nx, ny, new_keys, steps + 1))
    
    return -1  # If unable to collect all artifacts
if __name__ == "__main__":
    map1 = ["@..a.",
            "###.#",
            "b.A.B"]
    print(min_moves_to_collect_artifacts(map1))  # Output: 8

    map2 = ["@Aa"]
    print(min_moves_to_collect_artifacts(map2))  # Output: -1
