from numpy import zeros


def linear_filter(image, kernel):
    (shift_x, shift_y), (a, b) = kernel
    rows, columns = image.shape
    f_rows, f_columns = (rows - shift_x), (columns - shift_y)
    gi = zeros((f_rows, f_columns))
    for i in range(f_rows):
        for j in range(f_columns):
            gi[i][j] = a*image[i][j] + b*image[i+shift_x][j+shift_y]
    return gi


def linear_filter_hw(image, g):
    rows, columns = image.shape
    gl = len(g)
    offset = (gl+(gl%2))/2 - 1
    gi = zeros((rows, columns))
    for i in range(rows):
        for j in range(columns):
            for u in range(gl):
                x = (j-offset+u)
                if x < 0 or x > (columns-1):
                    pixel = 0
                else:
                    pixel = image[i][x]
                gi[i][j] += pixel * g[u]
    return gi