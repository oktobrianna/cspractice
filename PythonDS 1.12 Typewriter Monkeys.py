from random import choice


def generate_random_string(character_pool: str, target_string: str) -> str:
    """Generate a string of characters randomly chosen from a
    provided pool, equal to the length of a target string.
    """
    random_string = ""
    while len(random_string) < len(target_string):
        new_char = choice(character_pool)
        random_string += new_char
    return random_string


def count_matches(trial_sequence: str | list, target_sequence: str | list) -> int:
    """Iterate over two lists or strings of equal length and count how many of
    the corresponding members are identical.
    """
    num_matches = 0
    for trial_char, target_char in zip(trial_sequence, target_sequence, strict=True):
        if trial_char == target_char:
            num_matches += 1
    return num_matches


def check_possible_match(possible_items: str | list[str], trial_seq: str | list[str]) -> bool:
    """Check whether all characters in one string appear in another string by comparing them as sets."""
    set_possible_items = {ch for ch in possible_items}
    set_trial_seq = {ch for ch in trial_seq}
    return set_trial_seq.issubset(set_possible_items)


def generate_matching_sequence_slow(character_pool: str, target_string: str) -> str:
    """Repeatedly generate random strings to match the target string.

    Call string generator to generate random strings of same length as target string.
    Call scoring function to count number of matching characters.
    Continue generating new strings until target string is matched.
    Print current string and accuracy every thousand attempts.
    If target is reached, print target string and attempt number.
    """
    match_is_possible = check_possible_match(character_pool, target_string)
    if not match_is_possible:
        print("This string cannot be reproduced using the current character pool.")
        return
    num_tries = 0
    isMatch = False
    while isMatch is False:
        random_string = generate_random_string(character_pool, target_string)
        num_tries += 1
        num_matches = count_matches(random_string, target_string)
        if num_matches == len(target_string):
            print(
                f"Target sentence generated! Target was '{target_string},' randomly generated in {num_tries} attempts.")
            isMatch = True
        if num_tries % 1000 == 0:
            percent_matches = 100 * (num_matches / len(target_string))
            percent_matches = round(percent_matches, 2)
            print(
                f"Current attempt is '{random_string},'at attempt {num_tries}, with {percent_matches}% accuracy.")

# obviously this thing is horribly inefficient. but ideally it's written well to do the thing badly.


def generate_character_list(character_pool: str, target_string: str) -> list:
    """Generate a list of characters randomly chosen from a provided pool, equal to the length of a target string."""
    random_character_list = []  # this creates a list because a later function requires mutability.
    while len(random_character_list) < len(target_string):
        new_char = choice(character_pool)
        random_character_list.append(new_char)
    return random_character_list

# Question: I can produce the same result by replacing the iterated appending with a list comprehension,
# but the time appears to come out the same (if I'm using timeit properly). Is this accurate?
# I prefer the iteration for readability, but barely. Is this a good call?
# The possible comprehension: random_character_list = [choice(character_pool) for i in range(len(target_string))]


def randomly_revise_character(character_list: list[str], target_string: str, character_pool: str) -> list:
    """Randomly change the first character in a list that does not match
    the corresponding character in a target string. Return the revised list.
    """
    for i in range(len(character_list)):
        if character_list[i] != target_string[i]:
            character_list[i] = choice(character_pool)
            break
    return character_list


def format_list_to_string(origin_list: list) -> str:
    """Convert a list to a string without separators."""
    final_string = "".join(origin_list)
    return final_string


def generate_matching_sequence_fast(character_pool: str, target_string: str) -> None:
    """Randomly generate string matching a target string, replaicng one incorrect character at a time.

    Call function to generate list of random characters to match a target string.
    Call scoring function to count number of matching characters.
    Revise the sequence with single random characters, keeping correct ones, until target string is matched.
    Print current string and accuracy every thousand attempts.
    If target is reached, print target string and attempt number.
    """
    match_is_possible = check_possible_match(character_pool, target_string)
    if not match_is_possible:
        print("This string cannot be reproduced using the current character pool.")
        return
    isMatch = False
    random_character_list = generate_character_list(
        character_pool, target_string)
    num_tries = 1
    while isMatch is False:
        num_matches = count_matches(random_character_list, target_string)
        if num_matches == len(target_string):
            final_string = format_list_to_string(random_character_list)
            print(
                f"Target sentence generated! Target was '{target_string},' randomly generated as '{final_string}' in {num_tries} attempts.")
            isMatch = True
        else:
            if num_tries % 200 == 0:
                percent_matches = 100 * num_matches / len(target_string)
                percent_matches = round(percent_matches, 2)
                attempt_string = format_list_to_string(random_character_list)
                print(
                    f"Current attempt is '{attempt_string},'at attempt {num_tries}, with {percent_matches}% accuracy.")
            random_character_list = randomly_revise_character(
                random_character_list, target_string, character_pool)
            num_tries += 1


# original assignment not tested for slow generator in main() because it goes for eons.
def main():
    slow_char_pool = "abcdlmno"
    slow_test_string = "bacon"
    slow_test_break = "abcd"
    #generate_matching_sequence_slow(slow_char_pool, slow_test_string)
    #generate_matching_sequence_slow(slow_test_break, slow_test_string)

    character_pool = " abcdefghijklmnopqrstuvwxyz"
    target_string = "methinks it is like a weasel"
    fast_test_break = "Methinks it is like a weasel"
    generate_matching_sequence_fast(character_pool, target_string)
    generate_matching_sequence_fast(character_pool, fast_test_break)


if __name__ == "__main__":
    main()


