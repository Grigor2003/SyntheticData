# SyntheticData Generator

With this program you can generate synthetic data for your AI's image detection training.

---

## How to use

Open config, set your result, bg, obj PATHs, set the parameters as you like and run the `run.py` file. It will generate every possible combination of bg and object.

### Parameters

* `ignore_symbol` - You can specify symbol(s) for skipping the object if
  it is in object's file name
* `merge` - If False, creates separate folders for data and labels(relative coordinates of the object on bg)
* `bg_packages` - True for separate folders for each bg
* `out_of_bounds` - True for allowing objects be out of bounds
* `count` - How many times an image will be generated with current bg and object
* `distribution` - *linear* or *Gaussian* distribution for object placement
* `scale_rate` - Scale of the object. Values from `0` to infinity for scaling based on the value as a multiplier
* `blur_chance` - Chance of blurring the object. One number as a value only, `0` - 0% chance, `1` - 100% chance
* `blur_rate` - Blur on the object. Values from `(0, 1*)`, `0` - original image, `1` - fully blurred. *Values may be higher than `1` for extreme blur
* `noise_rate` - Noise on the final image. Values from `(0, 1)`, `0` - original image, `1` - complete noise


`scale_rate`, `blur_rate` and `noise_rate` parameters must be given as two element tuple(`(a, b)`) for a random value from range, list/int/float(`[a, b, c]` / `d`) for a random particular rate.
