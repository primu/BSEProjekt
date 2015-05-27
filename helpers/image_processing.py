from PIL import Image, ImageChops

def crop2(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    # x1, y1, x2, y2 = bbox
    # width = x2 - x1
    # height = y2 - y1
    #
    # if width < height:
    #     pass
    # if height < width:
    #     pass
    # else:
    #     pass

    if bbox:
        return im.crop(bbox)


def crop(array, pad=0, ratio=False):
    top_left = {
        "x": 99999,
        "y": 99999
    }

    bottom_right = {
        "x": -1,
        "y": -1
    }

    for y, row in enumerate(array):
        for x, cell in enumerate(row):
            if cell > 0:
                if top_left["x"] >= x:
                    top_left["x"] = x
                if top_left["y"] >= y:
                    top_left["y"] = y
                if bottom_right["x"] <= x:
                    bottom_right["x"] = x
                if bottom_right["y"] <= y:
                    bottom_right["y"] = y

    new_width = bottom_right["x"] - top_left["x"] + 2 * pad
    new_height = bottom_right["y"] - top_left["y"] + 2* pad

    result = []

    for x in range(pad):
        result.append([0] * new_width)

    for y, row in enumerate(array):
        if not (top_left["y"] <= y <= bottom_right["y"]):
            continue
        new_row = []
        for x in range(pad):
            new_row.append(0)
        for x, cell in enumerate(row):
            if top_left["x"] <= x <= bottom_right["x"]:
                new_row.append(cell)
        for x in range(pad):
            new_row.append(0)
        if new_width % 2 != 0:
            new_row.append(0)
        result.append(new_row)

    for x in range(pad):
        result.append([0] * new_width)

    if new_height % 2 != 0:
        result.append([0] * new_width)

    if ratio:
        if new_width > new_height:
            diff = new_width - new_height
            if diff % 2 != 0:
                result.append([0] * new_width)

            for x in range(diff / 2):
                result.insert(0, [0] * new_width)
                result.append([0] * new_width)

        elif new_height > new_width:
            diff = new_height - new_width
            for row in result:
                for x in range(diff / 2):
                    row.insert(0, 0)
                    row.append(0)
                if diff % 2 != 0:
                    row.append(0)
        else:
            pass
    return result

def scale_to(im, width, height):
    from PIL import Image
    size = (width, height)
    smaller_size = (width - 3, height - 3)

    # w, h = len(array[0]), len(array)
    # image_data = np.zeros((h,w,3), dtype=np.uint8)
    # for y, row in enumerate(array):
    #     for x, cell in enumerate(row):
    #         if cell > 0:
    #             image_data[y][x] = [255, 255, 255]
    #
    # im = Image.fromarray(image_data, "RGB")
    im.thumbnail(smaller_size, Image.ANTIALIAS)
    background = Image.new('RGBA', size, (255, 255, 255, 0))
    background.paste(im, ((size[0] - im.size[0]) / 2, (size[1] - im.size[1]) / 2))
    data = list(background.getdata())

    result = []
    row = []
    i = 0
    for element in data:
        row.append(255 - max(element[:-1]))
        i += 1
        if i == width:
            i = 0
            result.append(row)
            row = []

    return result