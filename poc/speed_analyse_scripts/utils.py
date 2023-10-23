def count_iterations(min_max, window, step):
    min_i, max_i = min_max
    counter = 0

    init_value = max_i - min_i
    init_value -= window

    while init_value > 0:
        init_value -= step
        counter += 1

    return counter


