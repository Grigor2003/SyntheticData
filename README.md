# SyntheticData Generator

With this program, you can generate synthetic data to train your AI in image detection.

---

## How to use

Open config, set your result, bg, obj PATHs, set parameters as you like and run `run.py` file. It will generate all possible combinations of bg and object.

### Parameters

* `ignore_symbol` - You can specify character(s) to skip an object if it is in the object's filename.
* `merge` - False to create separate folders for data and labels (object relative coordinates on bg)
* `bg_packages` - True for separate folders for each bg
* `out_of_bounds` - True to allow objects to go out of bounds
* `count` - How many times the image will be generated with the current bg and object
* `distribution` - *linear* or *Gaussian* distribution for object placement
* `scale_rate` - Object scale. Values from `0` to infinity to scale based on the value as a multiplier
* `blur_chance` - Chance to blur an object. One number as a value only, `0` - 0% chance, `1` - 100% chance
* `blur_rate` - Blur on the object. Values from `(0, 1*)`, `0` - original image, `1` - completely blurred. *Values can be higher than `1` for really strong blur.
* `noise_rate` - Noise in the final image. Values from `(0, 1)`, `0` - original image, `1` - total noise
* `flip_chance` - Chance to flip an object horizontally. Only one number as value, `0` - probability 0%, `1` - probability 100%

The `scale_rate`, `blur_rate` and `noise_rate` parameters must be given as a tuple with two values `(a, b)` for a random value from the range, list/int/float `[a, b, c]` / ` d` for a random specific value.

---

### Cropping you objects

You can run `crop.py` to crop the empty edges of your objects from the obj folder you specified in `config.py`. This will create a new folder with all your cropped objects. 
