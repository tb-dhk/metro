import colorsys

def relative_luminance(r, g, b):
    def linearize(c):
        if c <= 0.03928:
            return c / 12.92
        else:
            return ((c + 0.055) / 1.055) ** 2.4

    R = linearize(r)
    G = linearize(g)
    B = linearize(b)
    return 0.2126 * R + 0.7152 * G + 0.0722 * B

def find_max_v_for_3_1_contrast(h, s):
    for v in range(100, -1, -1):  # 100 iterations is more than enough for double precision
        r, g, b = colorsys.hsv_to_rgb(h / 360, s, v / 100)
        lum = relative_luminance(r, g, b)
        contrast = (1.0 + 0.05) / (lum + 0.05)
        if contrast >= 3:
            hex_color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}" 
            return v, hex_color, contrast

s = 1
for h in range(0, 360, 15):
    if not (0 <= h < 360) or not (0 <= s <= 1):
        print("Invalid input. Hue must be 0-360, Saturation 0-1.")
    else:
        v, hex_color, contrast = find_max_v_for_3_1_contrast(h, s)
        print(f"hue {h}: value {v}, hex {hex_color} (contrast {contrast})")
