from PIL import Image, ImageOps
import sys

def main():
    
    if len(sys.argv) != 3:
        print('Incorrect number of arguements. Must input an image to read and an image to write.')
        sys.exit()

    suffixes = ('jpg', 'jpeg', 'png')
    arg1 = str(sys.argv[1])
    arg2 = str(sys.argv[2])

    if not arg1.endswith(suffixes) or not arg2.endswith(suffixes):
        print('Both arguments must be a jgp or png file')
        sys.exit()

    arg1_suffix = arg1.split('.')[1]
    arg2_suffix = arg2.split('.')[1]

    if arg1_suffix != arg2_suffix:
        print('Both images must be the same type of file (Ex- image.png, second_image.png)')
        sys.exit() 

    try:
        image = Image.open(sys.argv[1])
    except FileNotFoundError:
        print("File not found")
        sys.exit()

    shirt = Image.open('shirt.png')
    size = shirt.size

    guy = ImageOps.fit(image, size)
    guy.paste(shirt, shirt)
    guy.show()
    

if __name__ == '__main__':
    main()