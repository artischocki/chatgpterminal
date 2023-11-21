def create_box(width, height):
    horizontal_border = '+' + '-' * (width - 2) + '+'
    vertical_border = '|' + ' ' * (width - 2) + '|'

    print(horizontal_border)
    for _ in range(height - 2):
        print(vertical_border)
    print(horizontal_border)

def input_text_in_box(width, height):
    text_box = [' ' * (width - 2) for _ in range(height - 2)]
    
    while True:
        for row in text_box:
            print('|' + row + '|')
        print('+' + '-' * (width - 2) + '+')

        row_num = int(input("Enter row number (1 to {}), or 0 to exit: ".format(height - 3)))
        if row_num == 0:
            break
        elif 1 <= row_num <= height - 3:
            row_text = input("Enter text for row {}: ".format(row_num))
            if len(row_text) <= width - 2:
                text_box[row_num - 1] = row_text[:width - 2]
            else:
                print("Text too long! Maximum length is", width - 2)

width_input = int(input("Enter the width of the box: "))
height_input = int(input("Enter the height of the box: "))

create_box(width_input, height_input)
input_text_in_box(width_input, height_input)

