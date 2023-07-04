import io
import json
import numpy as np
import cv2 as cv
from PIL import Image,ImageDraw,ImageFont, ImageChops




letters = "ABCDEFGHIJKLMNOPRSTUWZ"
digits = "0123456789"

font_size = 64
img_size = 128

fnt = "fonts/Uniconform.ttf"
font = ImageFont.truetype(io.BytesIO(open(fnt, "rb").read()), font_size, encoding="unic")


def make_img(text: str):
    char_width, char_height = font.getsize(text)
    from_img = Image.new('L', (char_width, char_height), "black")
    from_draw = ImageDraw.Draw(from_img)
    from_draw.text((0,0), text, 'white', font, anchor='lt')
    from_img = from_img.resize((img_size,img_size), resample=Image.BICUBIC)
    return np.array(from_img) / 256 

def show(from_chars, to_chars, common, prob):
        print(f"{from_chars} -> {to_chars} = {prob}")
        cv.imshow("output", common)
        cv.waitKey(-1)

# substitutions
# zamiany cyfry znaku inną
substitutions_map = {}
for from_char in digits:
    from_data = make_img(from_char)
    substitutions_map[from_char] = {}

    for to_char in digits:
        to_data = make_img(to_char)
        
        common = 1 - np.abs(from_data - to_data)
        prob = np.sum(common) / (img_size*img_size)

        substitutions_map[from_char][to_char] = prob

        # show(from_char, to_char, common, prob)

print(substitutions_map)
with open("substitutions_map.json", "w") as f:
    json.dump(substitutions_map, f, indent=4)


# insertions
# Zamiany jednej cyfry w dwie
insertions_map = {}
for from_char1 in digits:
    for from_char2 in digits:
        from_chars = from_char1 + from_char2
        from_data = make_img(from_chars)
        insertions_map[from_chars] = {}

        for to_char in digits:
            to_data = make_img(to_char)
            
            common = 1 - np.abs(from_data - to_data)
            prob = np.sum(common) / (img_size*img_size)

            insertions_map[from_chars][to_char] = prob

            # show(from_chars, to_char, common, prob)

print(insertions_map)
with open("insertions_map.json", "w") as f:
    json.dump(insertions_map, f, indent=4)


# prawdopodobieństwo zmiany na literę - do użycia w deletions
to_letter_map = {}
for from_char in digits:
    from_data = make_img(from_char)
    to_letter_prob = 0
    for to_char in letters:
        to_data = make_img(to_char)
        
        common = 1 - np.abs(from_data - to_data)
        to_letter_prob += np.sum(common) / (img_size*img_size)     
        # show(from_char, to_char, common, to_letter_prob)

    to_letter_map[from_char] = prob / len(letters)
    


# deletions
# Zamiana cyfry w literę (lub inny znak)
# Zamiana dwóch cyfr w jedną, duwstronnie
# spacja - początek/koniec numeru
deletions_map = {}
for before_char in digits + ' ':
    deletions_map[before_char] = {}
    before_data = make_img(before_char)
    for after_char in digits + ' ':
        deletions_map[before_char][after_char] = {}
        after_data = make_img(after_char)
        for deleted_char in digits:        
            
            right_deleted_data = make_img(before_char + deleted_char)
            left_deleted_data = make_img(deleted_char + after_char)                        
            
            right_deleted_common = 1 - np.abs(right_deleted_data - before_data)
            left_deleted_common = 1 - np.abs(left_deleted_data - after_data)
            
            right_prob = np.sum(right_deleted_common) / (img_size*img_size)
            left_prob = np.sum(left_deleted_common) / (img_size*img_size)

            # show(before_char + deleted_char, before_char, right_deleted_common, right_prob)
            # show(deleted_char + after_char, after_char, left_deleted_common, left_prob)
        
            deletions_map[before_char][after_char][deleted_char] = right_prob * 0.3 + left_prob * 0.3 + to_letter_map[deleted_char] * 0.4 # wagi z sufitu

print(deletions_map)
with open("deletions_map.json", "w") as f:
    json.dump(deletions_map, f, indent=4)