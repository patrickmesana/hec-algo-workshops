import random

class Element:
    def __init__(self, category):
        self.category = category

    def __repr__(self):
        return f"{self.category}"

# The Game class is implemented using a Strategy Design Pattern
class Game:
    def __init__(self, num_elements, visible_elements, max_unload, elements=None, show_hidden=False):
        self.num_elements = num_elements
        self.visible_elements = visible_elements
        self.max_unload = max_unload
        self.show_hidden = show_hidden
        self.moves_counter = 0
        self.game_state = "ongoing"  # Game state can be 'ongoing', 'game_over', or 'quit'
        # Initialize the game with provided elements or random elements represented by integers (categories)
        if elements is None:
            self.elements = [Element(random.randint(1, 100)) for _ in range(num_elements)]
        else:
            self.elements = [Element(category) for category in elements]

    def get_visible_elements(self):
        return self.elements[:self.visible_elements]

    def unload_elements(self, start_index):
        # Get the current visible elements
        visible = self.get_visible_elements()

        if start_index < 0 or start_index >= len(visible):
            return False

        # Increment the moves counter as the index is valid
        self.moves_counter += 1

        # Get the category of the selected element
        unload_category = visible[start_index].category

        # Find the consecutive elements with the given category starting from the chosen index (both directions)
        start = start_index
        end = start_index

        # Move backwards to find the start of the sequence
        while start > 0 and visible[start - 1].category == unload_category:
            start -= 1

        # Move forwards to find the end of the sequence
        while end < len(visible) and visible[end].category == unload_category:
            end += 1

        # Perform unloading of consecutive elements of the given category
        new_visible = visible[:start] + visible[end:]

        # Replace the removed elements with non-visible elements from the array
        non_visible = self.elements[self.visible_elements:]
        count = end - start
        new_elements = new_visible + non_visible[:count]
        # Update the elements list, maintaining order
        self.elements = new_elements + non_visible[count:]
        return True

    def play(self, moves_generator=None):
        while True:
            visible = self.get_visible_elements()
            if len(visible) == 0:
                # Set game state to game over
                self.game_state = "game_over"
                break

            if moves_generator is not None:
                # Get the next move from the generator
                try:
                    start_index = next(moves_generator)
                except StopIteration:
                    break
            else:
                # Use input generator to get user input
                start_index = next(input_generator(self))
            
            if start_index == -1:
                # Set game state to quit
                self.game_state = "quit"
                break
            
            # Adjust to ensure unloading all consecutive elements of the same category starting from start_index
            valid_move = self.unload_elements(start_index)
            if not valid_move:
                continue

    def display_elements(self):
        visible = self.get_visible_elements()
        if self.show_hidden:
            hidden = self.elements[self.visible_elements:]
            print(f"{visible} | {hidden}")
        else:
            print(f"{visible}")

# Example generator for programmatically playing the game
def moves_generator(moves):
    for move in moves:
        yield move

# Example generator for getting input from the user
def input_generator(game):
    while True:
        try:
            game.display_elements()
            user_input = int(input("Enter your move: "))
            yield user_input
        except ValueError:
            print("Invalid input. Please enter a valid index.")
        except StopIteration:
            break



def run_synthetic_game():
    # Initialize and play the game programmatically
    game = Game(num_elements=10, visible_elements=4, max_unload=2, elements=[5, 1, 5, 5, 4, 4, 1, 4, 2, 1], show_hidden=True)
    game.play(moves_generator=moves_generator([0, 1, 2, 3, 1]))
    # game.play(moves_generator=input_generator(game))
    game.display_elements()

    # Check the state of the game in real-time
    if game.game_state == 'game_over':
        print(f"Game over! Total moves: {game.moves_counter}")

    elif game.game_state == 'quit':
        print(f"Game quit! Total moves: {game.moves_counter}")

    elif game.game_state == 'ongoing':
        print(f"Game ongoing! Total moves: {game.moves_counter}")

    else:
        print("Invalid game state!")

def run_play():

    game = Game(num_elements=10, visible_elements=4, max_unload=2, show_hidden=True)
    game.play(input_generator(game))

    #if game over, print the total moves
    if game.game_state == 'game_over':
        print(f"Game over! Total moves: {game.moves_counter}")



if __name__ == "__main__":

    import sys
    if len(sys.argv) == 1:
        run_play()
    elif sys.argv[1] == "play":
        run_play()
    elif sys.argv[1] == "synthetic":
        run_synthetic_game()
    else:
        print("Invalid argument. Please use 'play' or 'synthetic' as arguments.")

