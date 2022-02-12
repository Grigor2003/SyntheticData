# Add '/' or "\" at the end of dirs' PATHs
result_path = "Result/"  # Enter Result folder's PATH
bg_path = "Bg/"  # Enter background pictures' PATH
object_path = "Obj/"  # Enter objects' PATH
merge = True  # Ctesutyun
bg_packages = True  # True for separate folders for bgs
out_of_bounds = False
count = 1  # How many times will the object be placed on the bg
scale = (0.5, 2)  # Scale, two element tuple for range, list for particular rates
blur_chance = 1  # Chance of blurring the object
blur_rate = (0.1, 0.9)  # Blur, two element tuple for range, list for particular rates
noise_rate = [0, 0.2]  # Noise, two element tuple for range, list for particular rates
