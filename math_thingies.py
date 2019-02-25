from random import randint

def evaluate(x, difficulty):
    d = difficulty
    return int((1 + d/5) * x)

def get_starting_pixel():
    return (randint(0, 2) * 96, randint(0, 2) * 96)

def cur_frame(x, y):
    a = x % y
    b = y - x % y
    return min(a, b)

def cur_frame_gen(x, a):
    return x % 50 // 25 if not a else x % 50 // 25 + 2