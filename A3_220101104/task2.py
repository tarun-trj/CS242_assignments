# Maze Solver

# Input the size of the square maze
size = int(input("Enter number(n) of rows for square matrix: (n x n) "))
visited = {}

# Input maze data row by row
maze_data = []
for i in range(size):
    row = []
    row_input = input(f"Enter row as space-separated 0s and 1s {i+1}: ").split()
    for value in row_input:
        row.append(int(value))
    maze_data.append(row)

# Initialize the maze by reversing the input data
maze = [[0 for _ in range(size)] for _ in range(size)]
for i in range(size):
    for j in range(size):
        maze[i][j] = maze_data[size - i - 1][j]

# Print the maze
print("The maze is: ")
for i in range(size):
    for j in range(size):
        print(maze[size - i - 1][j], end=" ")
    print()

# Input the starting and ending points
start_row = int(input("Row number of Starting Point: (check from bottom)")) - 1
start_col = int(input("Column number of Starting Point: (check from left)")) - 1
s_x = start_row
s_y = start_col

end_row = int(input("Row number of Ending Point: (check from bottom)")) - 1
end_col = int(input("Column number of Ending Point: (check from left)")) - 1

# Initialize the visited dictionary with the starting point
visited = {str([start_row, start_col]): 0}
current_path = [[start_row, start_col]]

# Initialize paths and ans lists
paths = []
ans = []

# Initialize step counter
step = 0

# Perform breadth-first search to explore all paths
while(len(current_path) != 0):
    for i in range(-1, 2, 1):
        for j in range(-1, 2, 1):
            
            if((str([max(start_row + i, 0), max(start_col + j, 0)]) not in visited) and (start_row + i < size and start_col + j < size)):
                if(maze[max(start_row + i, 0)][max(start_col + j, 0)] != 1):
                    visited[str([max(start_row + i, 0), max(start_col + j, 0)])] = visited[str([start_row, start_col])] + 1
                    current_path.append([max(start_row + i, 0), max(start_col + j, 0)])
            if((str([min(start_row + i, size - 1), min(start_col + j, size - 1)]) not in visited) and (start_row + i >= 0 and start_col + j >= 0)):
                if(maze[min(start_row + i, size - 1)][min(start_col + j, size - 1)] != 1):
                    visited[str([min(start_row + i, size - 1), min(start_col + j, size - 1)])] = visited[str([start_row, start_col])] + 1
                    current_path.append([min(start_row + i, size - 1), min(start_col + j, size - 1)])
    current_path.pop(0)
    if(len(current_path)):
        start_row = current_path[0][0]
        start_col = current_path[0][1]
paths.append([s_x, s_y])

# Construct the path from the starting point to the ending point
def make_path(s_x, s_y, visited):

    '''
    function to generate shortest paths

    Inputs: start row, start column, list of visited points

    Result: None
    Prints all paths
    '''
    global ans                                              # Global variable to store the final path
    global paths                                            # Global variable to store intermediate paths
    global distance                                         # Global variable to store the distance
    global end_row                                          # Global variable for the ending row
    global end_col                                          # Global variable for the ending column
    
    for i in range(-1, 2, 1):
        for j in range(-1, 2, 1):
            
            # Check if the neighbor is in the visited dictionary
            if(str([s_x + i, s_y + j]) in visited):
                
                # Check if the neighbor is the next step in the path
                if(visited[str([s_x + i, s_y + j])] == visited[str([s_x, s_y])] + 1):
                    paths.append([s_x + i, s_y + j])        # Add the neighbor to the path
                    
                    # Check if the path has reached the destination
                    if len(paths) == distance + 1:
                        
                        # Check if the destination is reached
                        if(paths[-1] == [end_row, end_col]):
                            print("start here", end="->")
                            
                            # Print the path elements
                            for element in paths:
                                print("(", element[0] + 1, ",", element[1] + 1, ")", end="->")
                            print("end reached")
                    
                    # Recursively explore the neighbor
                    make_path(s_x + i, s_y + j, visited)
                    paths.pop()  # Backtrack by removing the last element from the path

    return ans  # Return the final path

# Check if the maze is unreachable
if(maze[s_x][s_y] == 1 or maze[end_row][end_col] == 1 or (str([end_row, end_col]) not in visited)):
    print("unreachable")
else:
    # Print the least distance and all possible paths
    print("The least distance is:", end=" ")
    print(visited[str([end_row, end_col])])
    print("All possible paths are:")
    distance = visited[str([end_row, end_col])]
    make_path(s_x, s_y, visited)
