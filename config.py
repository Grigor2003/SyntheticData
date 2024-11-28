# Add '/' at the end of dirs' PATHs
result_path = "Result/"
bg_path = "Bg/"
obj_path = "Obj/"
# Parameters
ignore_symbol = "!!!!"
merge = False
bg_packages = False
out_of_bounds = True
out_of_bounds_rate = (0.1, 0.4)
count = 1
obj_count = (1, 2)
# uniform
distribution = "gaussian"
blur_filter = "bilateralFilter"
scale_rate = (0.5, 1.5)
blur_chance = 0.7
blur_spatial_rate = (2 * 0.35, 2 * 0.5)
blur_intensity_rate = (20, 70)
# uniform
noise_type = "gaussian"
noise_rate = (0.1, 0.2)
flip_chance = 0.5
# segmentation, classification
save_type = 'segmentation'
