import sys

def stack_permutations(input_list):
    """
    Generate stack-realizable permutations from the given input list.

    Args:
    - input_list (list or str): List of distinct integers or a comma-separated string.

    Returns:
    - list: List of stack-realizable permutations.
    """
    
    def has_repeats(lst):
        return len(lst) != len(set(lst))                                                                    # checks for repeats using non-repeating property of sets

    def follows_sequence(lst):
        return lst == list(range(1, len(lst) + 1))                                                          # creates a list of ordered elements up to the length of input and compares with input

    def generate_permutations(stack, current_permutation, remaining_input):
        """
        Recursively generate stack-realizable permutations.

        Args:
        - stack (list): Stack of elements.
        - current_permutation (list): Current permutation in progress.
        - remaining_input (list): Remaining elements to be injected.

        Returns:
        - None
        """
        # Base case: If both the stack and input are empty, a valid permutation is discovered.
        if not stack and not remaining_input:
            permutations.append(current_permutation[:])                                                     # Insert input to the list of valid permutations
            return

        # Try extracting from the stack if not empty to generate a new sequence of stack realisable permuutations
        if stack:
            top_element = stack.pop()                                                                       # Extraction step from stack
            generate_permutations(stack, current_permutation + [top_element], remaining_input)              # Recurse on the current state of lists and stacks after adding top element to the current permutation list
            stack.append(top_element)                                                                       # Restore the stack to its previous state.

        # Try injecting from the input if not empty to generate another sequence of permutations
        if remaining_input:
            element = remaining_input.pop(0)                                                                # Extract top element from input list
            stack.append(element)                                                                           # Add element to the temporary stack
            generate_permutations(stack, current_permutation, remaining_input)                              # Recurse on the current state of lists and stacks
            stack.pop()                                                                                     # Restore the stack to its previous state.
            remaining_input.insert(0, element)                                                              # Restore the input to its previous state.

    # Input validation
    if isinstance(input_list, str):
        remaining_input = input_list.split(',')                                                             # If the input is a string, split it into a list
    else:
        remaining_input = input_list                                                                        # Otherwise, it's already a list

    try:
        remaining_input = [int(num) for num in remaining_input]                                             # Try to convert the elements to integers
    except ValueError:
        return "Error: Input contains non-integer values."

    # Check for repeats
    if has_repeats(remaining_input):
        return "Error: The input should not contain repeating values."                                      # Error message for repeated numbers in inputs

    # Check if input follows sequence
    if not follows_sequence(remaining_input):
        return "Error: The input should follow the sequence of natural numbers."                            # Error message for not following the sequence

    # Initialize variables
    stack = []
    permutations = []

    # Initiate the permutation generation process.
    generate_permutations(stack, [], remaining_input)

    return permutations


if __name__ == "__main__":
    input_string = input("Enter a comma-separated list of numbers: ")                                       # Input from the user: a comma-separated list of numbers

    result = stack_permutations(input_string)                                                               # Desired list of permutations

    if isinstance(result, str):
        print(f"Error: {result}")
        sys.exit()

    permutations = result
    count = len(permutations)

    # Display the numbered stack-realizable permutations and the total count
    print(f"Stack-realizable permutations for input: {input_string}")
    for i, p in enumerate(permutations, 1):
        print(f"{i}. {p}")

    print(f"Total number of stack-realizable permutations: {count}")
