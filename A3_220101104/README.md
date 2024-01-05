# TASK1:

---

# Stack-Realizable Permutations Generator

## Introduction
This Python script generates stack-realizable permutations from a given input list of distinct integers. Stack-realizable permutations are those that can be generated using a stack following specific rules. The script provides an interactive interface for users to input a comma-separated list of numbers and outputs the stack-realizable permutations along with the total count.

## Requirements
The system must have Python 3.x installed

## Usage
1. Run the script in your terminal or preferred Python environment.
    		`python3 task1.py`
    		
2. Enter a comma-separated list of distinct integers when prompted.

3. The script will output the stack-realizable permutations and the total count.



## Input Requirements
- The input should be a comma-separated list of distinct integers.
- The integers should follow the sequence of natural numbers (1, 2, 3, ...).
- The input should not contain repeating values.

## Example
```plaintext
Enter a comma-separated list of numbers: 1,2,3
Stack-realizable permutations for input: 1,2,3
1. [1, 2, 3]
2. [1, 3, 2]
3. [2, 1, 3]
4. [3, 1, 2]
5. [3, 2, 1]
Total number of stack-realizable permutations: 5


## Code Explanation
The code recursively generates all possible stack realisable permutations by pushing and poopping inputs from input stream to stack and output streams.
Whenever the input stream and stack together become empty means a possible permutation has been achieved.
Such a permutation is pushed to output list
This process is repeated by recursion till all possiblilities have been explored.

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# TASK2:

# Maze Solver

## Introduction
This Python script takes user input for a square maze, starting point, and ending point. It then finds the shortest path from the starting point to the ending point in the maze.

## Requirements
The system must have Python 3.x installed

## Usage

1. Run the script on terminal in the same directory as the python3 file using the command:
		`python3 task2.py`
		
2. Enter the number of rows for the square maze.

3. Enter the maze configuration row by row, using space-separated 0s and 1s.

4. Specify the starting point (row and column).

5. Specify the ending point (row and column).



The script will output the maze, the least distance from the starting point to the ending point, and all possible paths.

## Code Explanation

### Input and Initialization

- `size`: Takes user input for the size of the square maze.
- `maze_data`: Takes user input row by row to initialize the maze matrix.
- `maze`: Initializes the maze by reversing the input data.
- `start_row`, `start_col`: Input the starting point (checking from the bottom and left).
- `end_row`, `end_col`: Input the ending point (checking from the bottom and left).
- `visited`: Initializes a dictionary to keep track of visited points.
- `current_path`: Initializes a list to keep track of the current path during breadth-first search.

### Breadth-First Search

- The script performs breadth-first search to find the shortest path from the starting point to the ending point.
- It uses a nested loop to explore neighboring points and updates the visited dictionary and current path accordingly.
- The search continues until the destination is reached or all possible paths are explored.

### Path Construction

- The `make_path` function is defined to construct the path from the starting point to the ending point.
- It uses recursion to explore and backtrack through the neighboring points, adding them to the path.
- When the destination is reached, it prints the path elements.

### Output

- The script checks if the maze is unreachable or if the destination is not in the visited dictionary.
- If reachable, it prints the least distance and all possible paths.

## Example

```plaintext
Enter number(n) of rows for square matrix: (n x n) 5
Enter row as space-separated 0s and 1s 1: 0 1 0 0 0
Enter row as space-separated 0s and 1s 2: 0 1 0 1 0
Enter row as space-separated 0s and 1s 3: 0 0 0 1 0
Enter row as space-separated 0s and 1s 4: 0 1 0 1 0
Enter row as space-separated 0s and 1s 5: 0 0 0 0 0
The maze is:
0 0 0 0 0
1 1 0 1 0
0 0 0 1 0
0 1 0 1 0
0 0 0 0 0
Row number of Starting Point: (check from bottom) 1
Column number of Starting Point: (check from left) 2
Row number of Ending Point: (check from bottom) 5
Column number of Ending Point: (check from left) 4
The least distance is: 8
All possible paths are:
start here->(1, 2)->(2, 2)->(3, 2)->(4, 2)->(5, 2)->(5, 3)->(5, 4)->end reached
start here->(1, 2)->(2, 2)->(3, 2)->(4, 2)->(5, 2)->(5, 3)->(4, 3)->end reached
start here->(1, 2)->(2, 2)->(3, 2)->(4, 2)->(5, 2)->(5, 4)->(4, 4)->end reached


