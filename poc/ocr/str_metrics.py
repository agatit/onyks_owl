def levenshtein_distance(str1: str, str2: str) -> int:
    """
    Calculate the Levenshtein distance between two strings.

    Args:
        str1 (str): First string
        str2 (str): Second string

    Returns:
        int: The minimum number of single-character edits needed to change str1 into str2
    """
    # Create a matrix of size (len(str1) + 1) x (len(str2) + 1)
    rows = len(str1) + 1
    cols = len(str2) + 1
    matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    # Initialize the first row and column
    for i in range(rows):
        matrix[i][0] = i
    for j in range(cols):
        matrix[0][j] = j

    # Fill in the rest of the matrix
    for i in range(1, rows):
        for j in range(1, cols):
            if str1[i - 1] == str2[j - 1]:
                substitution_cost = 0
            else:
                substitution_cost = 1

            matrix[i][j] = min(
                matrix[i - 1][j] + 1,  # deletion
                matrix[i][j - 1] + 1,  # insertion
                matrix[i - 1][j - 1] + substitution_cost  # substitution
            )

    return matrix[rows - 1][cols - 1]


def character_error_rate(expected: str, actual: str) -> float:
    """Levenshtein distance divided by expected string length"""
    return levenshtein_distance(expected, actual) / len(expected)


def jaro_winkler_distance(s1: str, s2: str, p: float = 0.1) -> float:
    """
    Calculate the Jaro-Winkler distance between two strings.

    Args:
        s1 (str): First string to compare
        s2 (str): Second string to compare
        p (float): Winkler's prefix scaling factor (default: 0.1)

    Returns:
        float: Jaro-Winkler distance between 0 and 1, where 1 means exact match
    """
    # If strings are equal, return 1
    if s1 == s2:
        return 1.0

    # If either string is empty, return 0
    if len(s1) == 0 or len(s2) == 0:
        return 0.0

    # Maximum distance between matching characters
    match_distance = max(len(s1), len(s2)) // 2 - 1

    # Find matching characters
    s1_matches = [False] * len(s1)
    s2_matches = [False] * len(s2)
    matches = 0

    for i in range(len(s1)):
        start = max(0, i - match_distance)
        end = min(i + match_distance + 1, len(s2))

        for j in range(start, end):
            if not s2_matches[j] and s1[i] == s2[j]:
                s1_matches[i] = True
                s2_matches[j] = True
                matches += 1
                break

    if matches == 0:
        return 0.0

    # Count transpositions
    k = 0
    transpositions = 0

    for i in range(len(s1)):
        if s1_matches[i]:
            while not s2_matches[k]:
                k += 1
            if s1[i] != s2[k]:
                transpositions += 1
            k += 1

    # Calculate Jaro distance
    transpositions = transpositions // 2
    jaro = (matches / len(s1) +
            matches / len(s2) +
            (matches - transpositions) / matches) / 3.0

    # Calculate common prefix length (up to 4 characters)
    l = 0
    for i in range(min(4, min(len(s1), len(s2)))):
        if s1[i] == s2[i]:
            l += 1
        else:
            break

    # Calculate Jaro-Winkler distance
    return jaro + (l * p * (1 - jaro))
