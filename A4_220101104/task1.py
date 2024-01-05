import re
from collections import Counter
from typing import Callable, Iterator, NewType

# Define custom types
Term = NewType('Term', str)
Operator = NewType('Operator', str)

# Flag for tracing
Solution = dict[str, int]
Solver = Callable[[set[int]], Iterator[Solution]]

TRACE = False

class CryptArithm:

    SUPPORTED_OPS = {'=', '+'}

    #---------------------------------------------------------------------------
    
    class Variable:
        """
        A letter-variable in the word-math puzzle.

        Holds the letter, the allowed digits for the letter, and its
        current candidate value.
        """

        __slots__ = ('_letter', '_allowed', '_value')

        def __init__(self, solver: 'CryptArithm', letter: str):
            """
            Initialize a Variable.

            Args:
                solver (CryptArithm): The CryptArithm instance.
                letter (str): The letter associated with the variable.
            """
            self._letter = letter
            self._allowed = set(solver._digits)
            self._value = 0

        def exclude(self, *values):
            """
            Exclude specified values as candidates for the variable.

            This is primarily used to prevent terms with leading zeros.

            Args:
                *values: Variable number of integers to exclude.
            """
            self._allowed -= set(values)

        def solver(self, solver: Solver) -> Solver:
            """
            Generate a solver function for the Variable.

            The solver tries each allowable digit in turn, provided the digit
            is not currently used by another letter. For each valid possible
            digit, it yields solutions from the next solver.

            Args:
                solver (Callable[[set[int]], Iterator[Solution]]): The next solver.

            Returns:
                Callable[[set[int]], Iterator[Solution]]: The generated solver.
            """

            def solve(used: set[int]) -> Iterator[Solution]:
                """
                Solve for a variable by trying each allowable digit.

                For each valid possible digit, yield solutions from the
                next solver.

                Args:
                    used (set[int]): Digits currently in use.

                Yields:
                    Iterator[Solution]: Solutions for the variable.
                """
                
                for digit in self._allowed - used:
                    self._value = digit
                    yield from solver(used | {digit})

            return solve

        def __str__(self):
            """
            Convert the Variable to a string representation.

            Returns:
                str: String representation of the Variable.
            """

            value = self._value
            if value is None:
                value = '{' + ''.join(map(str, self._allowed)) + '}'
            return f"{self._letter}={value}"

        def __repr__(self):
            """
            String representation of Variable for debugging.

            Returns:
                str: Debugging representation of the Variable.
            """

            return f"<{self._letter}>"
                
    #---------------------------------------------------------------------------

    class Column:
        """
        Represents a digit-sum column in the word-puzzle.

        For example, with SEND+MORE=MONEY, the last column of digits
        expresses the digit sum D+E=Y.

        A digit-sum will include a carry-in from a "smaller" column, if
        present, and a carry-out to a "larger" column, if present.
        """

        def __init__(self, solver: 'CryptArithm', result: 'CryptArithm.Variable'):
            """
            Initialize a Column.

            Args:
                solver (CryptArithm): The CryptArithm instance.
                result (CryptArithm.Variable): The result variable for the column.
            """
            self._base = solver._base  # Explanation: Set the base from the CryptArithm instance.
            self._addends = Counter()  # Explanation: Initialize a counter for digit addends.
            self._result = result      # Explanation: Set the result variable for the column.
            self._carry_in = None      # Explanation: Initialize carry-in from a smaller column.
            self._carry_to = None      # Explanation: Initialize carry-out to a larger column.
            self._carry = 0            # Explanation: Initialize carry value for the column.

        def add(self, var: 'CryptArithm.Variable') -> None:
            """
            Add a digit addend to the digit sum.

            Args:
                var (CryptArithm.Variable): The digit variable to add to the digit sum.
            """
            self._addends[var] += 1 # Increment the count of the digit variable.

        def carry_from(self, other: 'CryptArithm.Column') -> None:
            """
            Indicate this digit-sum has a carry-in from another column.

            Args:
                other (CryptArithm.Column): The other column providing the carry-in.
            """
            self._carry_in = other    # Set the carry-in from the specified column.
            other._carry_to = self     # Set the carry-out to the specified column.


        def __str__(self):
            """
            Return a string representation of the digit-sum column.

            Returns:
                str: A string representation of the digit-sum column.
            """
            exp = f"{self._result._letter}=" if self._result else "0="  # Explanation: Initialize the expression with the result or 0.
            if self._carry_in:
                exp += "carry"  # Add "carry" if there is a carry-in.
            for var, count in self._addends.items():
                if count == 1:
                    exp += f"+{var._letter}"  # Add positive digit variable to the expression.
                elif count == -1:
                    exp += f"-{var._letter}"  # Add negative digit variable to the expression.
                elif count != 0:
                    exp += f"{count:+d}{var._letter}"  # Add the count and digit variable to the expression.
            return exp

        def __repr__(self):
            """
            Return a string representation for debugging.

            Returns:
                str: A string representation for debugging purposes.
            """
            return f"Col[{self}]"

        def unknowns(self, knowns: set['CryptArithm.Variable']) -> list['CryptArithm.Variable']:
            """
            Given a set of known variables, determine the list of
            unknown variables in this digit-sum column, ordered in
            decreasing usage.

            Args:
                knowns (set[CryptArithm.Variable]): The set of known variables.

            Returns:
                list[CryptArithm.Variable]: List of unknown variables in decreasing order of usage.
            """

            unknowns = Counter(self._addends) # Count occurrences of digit variables in the digit sum.
            if self._result:
                # Decrement count for the result variable if present.
                unknowns[self._result] -= 1

            unknowns = [(var, abs(count)) for var, count in unknowns.items()]
            unknowns = sorted(unknowns, key=lambda vc: vc[1], reverse=True)
            return [var for var, _ in unknowns if var not in knowns]

        def validator(self, solver: Solver) -> Solver:
            """
            Validate the digit-sum column when all digits are known.

            Args:
                solver (Solver): The next solver function.

            Returns:
                Solver: The validation solver function.
            """
            def validate(used: set[int]) -> Iterator[Solution]:
                """
                Validate the digit-sum column and yield solutions if valid.

                Args:
                    used (set[int]): The set of used digits.

                Yields:
                    Iterator[Solution]: Solutions generated by the next solver.
                """

                # Compute the sum of the digit counts multiplied by their values
                result = sum(count * var._value
                             for var, count in self._addends.items())
                # Add the carry-in, if present
                if self._carry_in:
                    result += self._carry_in._carry

                # Compute the carry and result after division
                carry, result = result // self._base, result % self._base
                
                # Check if the result is correct and the carry-out is allowed
                if (result == self._result._value and
                        (carry == 0 or self._carry_to)):
                    self._carry = carry
                    yield from solver(used)
            
            return validate

        def _solve_for_result(self, solver: Solver) -> Solver:
            """
            Solve for the result digit when all other digits are known.

            Args:
                solver (Solver): The next solver function.

            Returns:
                Solver: The solve function for the result digit.
            """
                
            def solve(used: set[int]) -> Iterator[Solution]:
                """
                Solve for the result digit and yield solutions.

                Args:
                    used (set[int]): The set of used digits.

                Yields:
                    Iterator[Solution]: Solutions generated by the next solver.
                """

                # Compute the sum of the digit counts multiplied by their values
                result = sum(count * var._value
                             for var, count in self._addends.items())
                # Add the carry-in, if present
                if self._carry_in:
                    result += self._carry_in._carry

                # Compute the carry and result after division
                carry, digit = result // self._base, result % self._base

                # Check if the digit is allowed and the carry-out is allowed
                allowed = self._result._allowed - used
                if digit in allowed and (carry == 0 or self._carry_to):
                    self._result._value = digit
                    self._carry = carry
                    yield from solver(used | {digit})

            return solve
        
        def _solve_for_addend(self, addend: 'CryptArithm.Variable'):
            """
            Solve for a non-result digit in the digit-sum column.

            Args:
                addend (CryptArithm.Variable): The non-result digit variable.

            Returns:
                Solver: The solve function for the non-result digit.
            """
            def solver(solver: Solver) -> Solver:
                """
                Solve for the non-result digit and yield solutions.

                Args:
                    solver (Solver): The next solver function.

                Yields:
                    Iterator[Solution]: Solutions generated by the next solver.
                """
                def solve(used: set[int]) -> Iterator[Solution]:
                    # Set the value of the non-result digit to 0
                    addend._value = 0
                    # Compute the sum of the digit counts multiplied by their values
                    result = sum(count * var._value
                                for var, count in self._addends.items())                    
                    # Add the carry-in, if present
                    if self._carry_in:
                        result += self._carry_in._carry

                    # Get the multiplier for the non-result digit (+/- 1)
                    multiplier = self._addends[addend]
                    # Use modular arithmetic to compute the unique digit
                    digit = (self._result._value - result) * multiplier
                    digit %= self._base

                    # Update the result with the computed digit
                    result += digit * multiplier
                    # Compute the carry after division
                    carry = result // self._base

                    # Check if the digit is allowed and the carry-out is allowed
                    allowed = addend._allowed - used
                    if digit in allowed and (carry == 0 or self._carry_to):
                        addend._value = digit
                        self._carry = carry
                        yield from solver(used | {digit})

                return solve
            return solver

        def solver(self, unknown: 'CryptArithm.Variable'):
            """
            Determine the specialized solver for a digit sum column.

            Args:
                unknown (CryptArithm.Variable): The unknown digit variable.

            Returns:
                Solver: The specialized solver function.
                None: If no specialized solver exists.
            """
            # Check if the unknown is the result digit and it's not repeated
            if unknown == self._result:
                if self._addends[unknown] == 0:
                    return self._solve_for_result
            # Check if the unknown is a non-repeated digit
            elif abs(self._addends[unknown]) == 1:
                return self._solve_for_addend(unknown)

            return None
                

    #---------------------------------------------------------------------------
    
    def __init__(self, puzzle: str, base: int = 10, leading_zeros: bool = False):
        """
        Initialize the CryptArithm object with the given puzzle.

        Args:
            puzzle (str): The word math puzzle.
            base (int, optional): The number base. Defaults to 10.
            leading_zeros (bool, optional): Whether leading zeros are allowed. Defaults to False.
        """
        self._puzzle = puzzle
        self._base = base
        self._leading_zeros = leading_zeros

        
        self._puzzle = puzzle
        self._base = base
        self._leading_zeros = leading_zeros
# Extract unique letters from the puzzle
        letters = set(ch for ch in puzzle if ch.isalpha())
        
        # Check if the number of unique letters exceeds the base
        if len(letters) > 10:
            raise ValueError("Puzzle has too many unique digits. Maximum allowed is 10.")
        
        # Define the range of digits based on the given base
        self._digits = range(base)
        # Create variables for each unique letter in the puzzle
        self._variables = self._create_variables(puzzle)
        # Create digit-sum columns based on the puzzle
        self._columns = self._create_columns(puzzle)

    def _create_variables(self, puzzle: str) -> dict[str, 'CryptArithm.Variable']:
        """
        Create a variable for each unique letter in the puzzle.

        Args:
            puzzle (str): The word math puzzle.

        Returns:
            dict[str, 'CryptArithm.Variable']: Dictionary of variables.
        """
        # Extract unique letters from the puzzle
        letters = set(ch for ch in puzzle if ch.isalpha())
        
        # Check if the number of unique letters exceeds the base
        if len(letters) > self._base:
            raise ValueError(f"Puzzle has too many variables for base-{self._base}")

        # Create variables for each unique letter
        return {letter: CryptArithm.Variable(self, letter) for letter in letters}

    @classmethod
    def _parse(cls, puzzle: str) -> tuple[list[Operator], list[Term]]:
        """
        Parse the puzzle into tokens.

        Args:
            puzzle (str): The word math puzzle.

        Returns:
            tuple[list[Operator], list[Term]]: Parsed operators and terms.
        """
        # Remove spaces, replace multiple equal signs, and split into tokens
        equation = re.sub('=+', '=', re.sub(r'\s+', '', puzzle))
        tokens = re.split(r'(\W+)', equation)
        terms = [token for token in tokens if token.isalpha()]
        operators = [token for token in tokens if not token.isalpha()]

        # Validation
        if len(tokens) < 5 or len(terms) != len(operators) + 1:
            raise ValueError("Refer to instructions")

        # Check for unsupported operators
        if (unsupported := set(operators) - cls.SUPPORTED_OPS):
            raise NotImplementedError(f"Unsupported: {repr(unsupported)[1:-1]}")
        
        # Check for the presence of one equals operator
        if operators.count('=') != 1:
            raise ValueError("Only one equals operator allowed")
        
        
        
  
        # Check if the last operator is an equals sign
        if operators[-1] != '=':
            raise ValueError("Last operator expected to be equals")

        return operators, terms

    def _create_columns(self, puzzle: str) -> list[Column]:
        """
        Parse the puzzle into a list of digit-sum columns.
        """
        operators, terms = self._parse(puzzle)

        # Leading zeros are not allowed
        if not self._leading_zeros:
            for term in terms:
                if len(term) > 1:
                    self._variables[term[0]].exclude(0)
        
        num_columns = max(map(len, terms))      # Maximum columns
        terms = [term[::-1] for term in terms]  # Reverse individual terms
        operators.insert(0, '+')                # First term is "added"
        result = terms.pop()                    # Extract result
        operators.pop()                         # Discard "=" operator

        # Extract into columns
        columns = []
        for col_num in range(num_columns):
            if col_num < len(result):
                var = self._variables[result[col_num]]
            else:
                var = None
                
            column = self.Column(self, var)
            for op, term in zip(operators, terms):
                if col_num < len(term):
                    var = self._variables[term[col_num]]
                    if op == '+':
                        column.add(var)
                    else:
                        raise RuntimeError(f"Unexpected operator: {op}")

            columns.append(column)

        for to, frm in zip(columns[1:], columns[:-1]):
            to.carry_from(frm)
        
        return columns

    def _strategize(self):
        """
        Determine a solving strategy.

        Returns a list of strategy functions.
        """

        strategies = []
        knowns = set()
        
        # For each column, starting at the ones-column...
        for column in self._columns:
            unknowns = column.unknowns(knowns)
            if TRACE:
                print(f"{column}: {unknowns}")

            # If the column has unknowns...
            if unknowns:
                # if it has more than one unknown...
                for var in unknowns[:-1]:
                    strategies.append(var.solver)

                # For the last unknown, attempt to find a specialized solver
                last = unknowns[-1]
                solver = column.solver(last)
                if solver:
                    strategies.append(solver)
                else:
                    # Failing that, try every possible value...
                    strategies.append(last.solver)
                    # ... and validate the column
                    strategies.append(column.validator)

                knowns |= set(unknowns)
            else:
                # No unknowns! Just validate the column
                strategies.append(column.validator)

        return strategies

    def solutions(self) -> Iterator[Solution]:
        """
        Create a solver strategy, and then generate all possible
        solutions.
        """
        
        strategies = self._strategize()
        solver = self._emitter()
        for strategy in reversed(strategies):
            solver = strategy(solver)

        yield from solver(set())

    def solve(self) -> Solution:
        """
        Find the unique solution to the puzzle.
        """
        solution = next(solutions, None)

        if solution is None:
            raise ValueError("No solution found")

        

    def _emitter(self) -> Solver:
        def solver(used: set[int]) -> Iterator[Solution]:
            yield {var._letter: var._value for var in self._variables.values()}
        return solver

    def substitute(self, solution: dict[str, int]) -> str:
        """
        Translate the puzzle using the given solution, into a numeric
        version of the puzzle.
        """
        if self._base > 10:
            raise NotImplementedError("Not yet implemented.")

        puzzle = self._puzzle
        for key, val in solution.items():
            puzzle = puzzle.replace(key, str(val))

        return puzzle

#===============================================================================

if __name__ == '__main__':
    # Prompt user for input formats and puzzles
    print("Enter word math puzzles Multiline is allowed. (press Enter twice after each puzzle and thrice after last puzzle has been entered):")
    print("Note that upper and lower case characters are perceived as distinct digits and leading zeros are acceptable")
    print("No output for empty strings!!!")
    print("Valid input formats are: ")
    print("Format 1:SEND +MORE + STUFF= MONEY\n")
    print("Format 2:SEND\n\t+MORE\n\t=MONEY\n")
    print("Format 3:SEND\n\t+MORE\n\t=====\n\tMONEY\n")
    puzzles = []

    while True:
        puzzle_lines = []
        print("Enter the puzzle:")

        while True:
            line = input()
            if not line.strip():  # Stop when the user presses Enter
                break
            puzzle_lines.append(line)

        if not puzzle_lines:
            break

        puzzle = '\n'.join(puzzle_lines)
        puzzles.append(puzzle)

    for idx, puzzle in enumerate(puzzles, start=1):
        print(f"\nSolving Puzzle #{idx}:\n")

        try:
            # Create CryptArithm instance
            ca = CryptArithm(puzzle)
        except (ValueError, NotImplementedError, RuntimeError) as e:
            print(f"Error in puzzle format: {e}")
            continue

        unique_variables = len(ca._variables)
        if unique_variables > 10:
            print(f"Error: Too many unique variables ({unique_variables}). Maximum allowed is 10.")
            continue

        try:
            # Solve the puzzle and print solutions
            solutions = ca.solutions()
            solution_count = 0

            for i, solution in enumerate(solutions, start=1):
                solution_count += 1
                print(f"Solution #{solution_count}:")
                print(ca.substitute(solution))
                print('-'*20)

            if solution_count == 0:
                print("No solution found")
        except ValueError as e:
            print(f"{str(e)}")  # Print the custom message for no solution found