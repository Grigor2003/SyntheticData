# Add '/' at the end of dirs' PATHs
result_path = "Result/"  # Enter Result's folder PATH
bg_path = "Bg/"  # Enter background pictures' folder PATH
obj_path = "Obj/"  # Enter objects' folder PATH
# Parameters
ignore_symbol = "!!!!"  # You can specify symbol for skipping the object if it is in object's file name
merge = True  # If False, creates separate folders for data and labels
bg_packages = False  # True for separate folders for bg_names
out_of_bounds = False  # True for allowing objects be out of bounds
count = 3  # How many times the object will be placed on the bg
distribution = "linear"  # linear or gaussian
scale_rate = 1  # Scale, two element tuple for range, list for particular rates
blur_chance = 1  # Chance of blurring the object
blur_rate = 0  # Blur, two element tuple for range, list for particular rates
noise_rate = 0  # Noise, two element tuple for range, list for particular rates
