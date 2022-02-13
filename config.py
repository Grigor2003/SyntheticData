# Add '/' at the end of dirs' PATHs
result_path = "Result/"  # Enter Result's folder PATH
bg_path = "Bg/"  # Enter background pictures' folder PATH
obj_path = "Obj/"  # Enter objects' folder PATH
merge = True  # Ctesutyun
bg_packages = False  # True for separate folders for bgs
out_of_bounds = False  # True for allowing objects be out of bounds
count = 2  # How many times the object will be placed on the bg
scale_rate = (0.5, 2)  # Scale, two element tuple for range, list for particular rates
blur_chance = 0.5  # Chance of blurring the object
blur_rate = (0.1, 0.6)  # Blur, two element tuple for range, list for particular rates
noise_rate = (0.2, 0.4)  # Noise, two element tuple for range, list for particular rates
