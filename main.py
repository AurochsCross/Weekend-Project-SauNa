import time
from neopixel import Neopixel
import math
import random

numpix = 30
pixels = Neopixel(numpix, 0, 28, "GRB")

color_red = (255, 0, 0)
color_clear = (0, 0, 0)

pixels.brightness(255)
pixels.fill(color_clear)

time_interval = 0.01  # seconds
led_count = 8

def clamp01(x):
    return max(0, min(1, x))

def lerp(a, b, t):
    return a + (b-a)*t

def lerp_array(a, b, t):
    result = get_empty_array(len(a))
    for i in range(0, len(a)):
        result[i] = lerp(a[i], b[i], t)
    
    return result


def get_brightness_from_angle(angle, index, count):
    if (angle > 360):
        angle -= 360

    difference = abs(angle - (360 / count * index))
    difference = min(difference, 360-difference)

    result =  clamp01(1 - (difference / 90))

    return result * result


def get_brightness(x):
    return clamp01((math.sin(x*3.14*2)+0)*1)


def get_brightness_extra(x):
    return clamp01((math.sin(x*3.14*2)+1.2)*1)


def get_empty_array(size):
    return [0] * size


def initial_look_state():
    result = get_empty_array(led_count)
    for i in range(0, led_count):
        result[i] = get_brightness_from_angle(180, i, led_count)

    return result


def sequence_1(current_time, led_count):
    result = get_empty_array(led_count)
    for i in range(0, led_count):
        result[i] = clamp01(math.sin(current_time*2.5)*current_time*current_time*1.6)

    return result


def sequence_2(elapsed_time, led_count):
    result = get_empty_array(led_count)
    for i in range(0, led_count):
        brightness = get_brightness((1/led_count*i) + elapsed_time)
        result[i] = clamp01(brightness*get_brightness_extra(elapsed_time*0.3)+0.1)
    
    return result


def sequence_3(elapsed_time, led_count):
    result = get_empty_array(led_count)
    for i in range(0, led_count):
        result[i] = clamp01((math.sin(elapsed_time*3.15*2)+2)*0.35)
    
    return result


def orcestrated_sequence(elapsed_time, led_count):

    result = get_empty_array(led_count)
    
    if elapsed_time < 0:
        return result
    elif elapsed_time < 3:
        result = sequence_1(elapsed_time / 3, led_count)
    elif elapsed_time >=3 and elapsed_time < 4:
        seq1 = sequence_1(1, led_count)
        seq2 = initial_look_state()
        # seq2 = sequence_2(elapsed_time, led_count)


        for i in range(0, led_count):
            result[i] = lerp(seq1[i], seq2[i], clamp01(elapsed_time-3))
    else:
        result = initial_look_state()

    # if elapsed_time >= 4:
    #     seq1 = sequence_2(elapsed_time, led_count)
    #     seq2 = sequence_3(elapsed_time*3.1563, led_count)
    #     result = lerp_array(seq1, seq2, clamp01(0.1))

    return result


def play_sequences():
    elapsed_time = 0

    while elapsed_time < 4.1:
        elapsed_time += time_interval

        sequence = orcestrated_sequence(elapsed_time, led_count)

        for i in range(0, led_count):
            brightness = sequence[i]
            pixels.set_pixel(i, (255*brightness, 0, 0))

        pixels.show()
        time.sleep(time_interval)

    play_eye_movement()

# play_sequences()

def animate_look(start_angle):
    animation_time = random.random() * 5 + 0.5
    elapsed_time = 0

    # random target angle
    target_angle =  random.randint(0, 360)

    while elapsed_time < animation_time:
        elapsed_time += time_interval

        angle = lerp(start_angle, target_angle, clamp01(elapsed_time/animation_time))

        for i in range(0, led_count):
            brightness = get_brightness_from_angle(angle, i, led_count)
            pixels.set_pixel(i, (255*brightness, 0, 0))

        pixels.show()
        time.sleep(time_interval)

    return target_angle



def play_eye_movement():
    elapsed_time = 0
    angle = 180

    while True:
        angle = animate_look(angle)
        # elapsed_time += time_interval
        # angle += 1

        # print(elapsed_time)

        # for i in range(0, led_count):
        #     brightness = get_brightness_from_angle(angle, i, led_count)
        #     pixels.set_pixel(i, (255*brightness, 0, 0))

        # pixels.show()
        # time.sleep(time_interval)


play_sequences()