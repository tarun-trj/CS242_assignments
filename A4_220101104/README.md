# ASSIGNMENT 4:
---
### Name: Tarun Raj
### Roll No. 220101104

# TASK 1: CRYPTARITHMIC SOLVER

This Python script is designed to solve Cryptarithmetic puzzles, where letters represent digits in a mathematical equation.

## Prerequisites
Make sure that Python3.x is installed on your system. To check if Python3 is present run the following command:
    `python3 --version`

## How to Use

1. Save the script as `task1.py`.
2. Open a terminal and navigate to the directory containing the script.
3. Run the script using the following command:

   ```bash
   python3 cryptarithm_solver.py

## Input Format

The script supports 3 input formats:

1. SEND + MORE = MONEY
    in this format the spaces dont matter and are ignored

2. SEND
   +MORE
   =MONEY

3.  SEND
   +MORE
   =====
   MONEY

Output will be returned in input format
Leading zeros are eliminated from consideration

## Code Overview

1. **Column Exploration:**
   - The solver starts at the ones column, trying each allowable digit for D and E to satisfy the equation D + E = Y.
   - If a solution violates constraints (e.g., duplicate digits), it discards that solution and continues exploring.
   - The solver advances to the next column, considering known values from the ones column.

2. **Known Values:**
   - Known values from the ones column affect the exploration of subsequent columns.
   - For example, if E is assigned a value from the ones column, it is considered "known," and the solver adjusts its exploration accordingly.

3. **Branching and Backtracking:**
   - The solver explores different branches of the solution space, backtracking when it reaches impossibilities.
   - It uses a stack-like approach, advancing deeper into columns and unwinding when needed.

4. **Yield Mechanism:**
   - The solution is generated using `yield` and `yield from` statements. When a valid solution is found, it returns that solution and pauses the search until the next solution is requested.

5. **Multiple Solutions:**
   - The test code attempts to generate all solutions to ensure uniqueness. If the puzzle has multiple solutions, the solver will find and present them.

---
# TASK 2: CREATING THE REQUESTED LATEX DOCUMENT

## Overview
This LaTeX document serves as a beginner's guide to using LaTeX for typesetting mathematical and scientific content. It covers basic inline and display math, equations, matrices, integrals, derivatives, and more.

## Prerequisites
Make sure you have a LaTeX distribution installed on your system. 
to download latex type in your terminal:
sudo apt-get install texlive
## File Structure
- *task2-1.tex* and *task2-1.tex*: The main LaTeX documents.
- *README*: This file.

## Running the Document
1. Open a terminal and navigate to the directory containing the `task2-1.tex` and `task2-2.tex` files.

2. Compile the LaTeX document using the following commands
   `pdflatex task2-1.tex && rm *.log *.aux *.out`
   `pdflatex task2-2.tex && rm *.log *.aux *.out`

3. This will create two documents `task2-1.pdf` and `task2-2.pdf` respectively as requested.

## Additional Information

The LaTeX document includes examples of:
* Basic math: $a^2 + b^2 = c^2$
* Equations with labels
* Matrix equations
