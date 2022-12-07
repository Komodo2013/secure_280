styles = {
    # text decorations
    "default": "\033[0m",
    "bold": "\033[1m",
    "italic": "\033[3m",
    "underline": "\033[4m",
    "strike": "\033[9m",
    "border": "\033[51m",

    # text colors
    "white": "\033[30m",
    "dark_grey": "\033[37m",
    "black": "\033[97m",
    "red": "\033[31m",
    "pink": "\033[91m",
    "yellow": "\033[93m",
    "mustard": "\033[33m",
    "lime_green": "\033[32m",
    "green": "\033[92m",
    "blue_green": "\033[36m",
    "cyan": "\033[96m",
    "blue": "\033[34m",
    "light_blue": "\033[94m",
    "purple": "\033[35m",
    "light_purple": "\033[95m",

    # background colors
    "white_highlight": "\033[40m",
    "light_grey_highlight": "\033[7m",
    "grey_highlight": "\033[47m",
    "dark_grey_highlight": "\033[100m",
    "red_highlight": "\033[41m",
    "pink_highlight": "\033[101m",
    "yellow_highlight": "\033[103m",
    "mustard_highlight": "\033[43m",
    "lime_green_highlight": "\033[102m",
    "green_highlight": "\033[42m",
    "cyan_highlight": "\033[46m",
    "light_cyan_highlight": "\033[106m",
    "blue_highlight": "\033[44m",
    "light_blue_highlight": "\033[104m",
    "purple_highlight": "\033[45m",
    "light_purple_highlight": "\033[105m",
}


def print_format_table():
    """
    prints table of formatted text format options
    """
    for style in (0,1,3,4,7,9,51): #0 - none, 1 - bold, 3 - italic, 4 - underline, 7 - highlight, 9 - strike, 51 outline
        for fg in range(30, 38):  # 30-38, 90-98
            s1 = ''
            for bg in range(40, 49):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            for bg in range(100, 108):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        for fg in range(90, 98): #30-38, 90-98
            s1 = ''
            for bg in range(40, 49):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            for bg in range(100, 108):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')


print_format_table()