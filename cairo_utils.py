# CAIRO FUNCTION TEST
import cairo
import math
from utils import longest_string,concatenate_name
import datetime
def text_rotation(ctx, string, pos, theta=0.0, face='Arial', font_size=18):
    ctx.save()

    # build up an appropriate font
    ctx.select_font_face(face, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(font_size)
    fascent, fdescent, fheight, fxadvance, fyadvance = ctx.font_extents()
    x_off, y_off, tw, th = ctx.text_extents(string)[:4]
    nx = -tw / 2.0
    ny = fheight / 2

    ctx.translate(pos[0], pos[1])
    ctx.rotate(theta)
    ctx.translate(nx, ny)
    ctx.move_to(0, 0)
    ctx.show_text(string)
    ctx.restore()


def rectangle(ctx, pos, width, height, height_context):
    ctx.save()

    ctx.rectangle(pos[0], pos[1], width, height)
    ctx.rectangle(pos[0], pos[1] + height, width, height_context)

    ctx.restore()
def outline(context, screen_height, screen_width, margin):
    screen_height -= margin
    screen_width -= margin
    context.save()
    # setting of line width
    context.set_line_width(4)

    # setting of line pattern
    context.set_dash([4.0, 21.0, 2.0])

    # move the context to x,y position
    context.move_to(margin, margin)

    # creating a line
    context.line_to(margin, screen_height)
    # move the context to x,y position
    context.move_to(margin, margin)

    # creating a line
    context.line_to(screen_width, margin)

    context.move_to(screen_width, screen_height)

    # creating a line
    context.line_to(screen_width, margin)

    context.move_to(screen_width, screen_height)
    # creating a line
    context.line_to(margin, screen_height)

    context.stroke()
    context.restore()


def title(context, title, screen_width, font_family="Arial", font_size=75):
    context.save()
    # setting color of the context
    context.set_source_rgb(0, 0, 0)

    # approximate text height
    context.set_font_size(font_size)

    # Font Style
    context.select_font_face(
        font_family, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)

    xbearing, ybearing, width, height, dx, dy = context.text_extents(title)

    # position for the text center
    context.move_to((screen_width // 2) - (width // 2), 300)

    context.show_text(title)

    context.restore()


def summary(context, date, shift, riksa, pos, font_family="Arial", font_size=45):
    context.save()
    posx = pos[0]
    posy = pos[1]

    date = "TANGGAL       : " + date
    shift = "SHIFT               : " + shift
    riksa = "GRUP               : " + riksa
    # print text
    # setting color of the context
    context.set_source_rgb(0, 0, 0)

    # approximate text height
    context.set_font_size(font_size)

    # Font Style
    context.select_font_face(
        font_family, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)

    xbearing, ybearing, width, height, dx, dy = context.text_extents(date)
    paragraph_margin = height + (3 / 5 * font_size)
    context.move_to(posx, posy)
    context.show_text(date)
    context.move_to(posx, posy + paragraph_margin)
    context.show_text(shift)
    context.move_to(posx, posy + 2 * paragraph_margin)

    context.show_text(riksa)

    # setting of line width
    context.set_line_width(12)
    context.rectangle(posx - (height + font_size), posy - (height + font_size), width + 2 * (height + font_size),
                      paragraph_margin * 4)

    # setting of line width
    context.stroke()

    context.restore()


def text_box(context, text, sub_text, pos, font_family="Arial", font_size=45, subtext_font_size=35,
             font_weight=cairo.FONT_WEIGHT_BOLD, rect_line_width=7, rect_dim=None):
    context.save()
    # setting color of the context
    context.set_source_rgb(0, 0, 0)
    # approximate text height
    context.set_font_size(font_size)
    # Font Style
    context.select_font_face(
        font_family, cairo.FONT_SLANT_NORMAL, font_weight)
    posx = pos[0]
    posy = pos[1]
    sub_text = concatenate_name(sub_text)
    paragraph_margin = 0

    xbearing, ybearing, l_width, l_height, dx, dy = context.text_extents(longest_string(text + sub_text))

    for string in text:
        xbearing, ybearing, width, height, dx, dy = context.text_extents(string)
        context.move_to(posx - width / 2, posy + paragraph_margin)
        context.show_text(string)
        paragraph_margin += height + font_size

    # setting of line width
    context.set_line_width(rect_line_width)

    # this is making the box from the center of the text, a lot of magic dont touch it
    rect_x = posx - (l_width / 2 + font_size)
    rect_y = posy - (l_height + font_size)
    rect_width = l_width + (l_height + font_size)
    rect_height = (paragraph_margin + (font_size))
    # branch if rectangle dimension is set force the dimension on it
    context.rectangle(rect_x, rect_y, rect_width, rect_height)
    context.stroke()

    paragraph_margin += font_size
    # approximate text height
    context.set_font_size(subtext_font_size)
    for string in sub_text:
        # approximate text height
        xbearing, ybearing, width, height, dx, dy = context.text_extents(string)
        context.move_to(posx - width / 2, posy + paragraph_margin)
        context.show_text(string)
        paragraph_margin += height + font_size

    rect_x = posx - (l_width / 2 + font_size)
    rect_y = posy - (l_height + font_size)
    rect_width = l_width + (l_height + font_size)
    rect_height = (paragraph_margin + (font_size))
    # branch if rectangle dimension is set force the dimension on it
    context.rectangle(rect_x, rect_y, rect_width, rect_height)
    context.stroke()

    context.restore()
    return rect_x, rect_y, rect_width, rect_height, height, font_size


def scaled_text(context, cur_scale, rect_width, text_width, text):
    context.save()
    context.scale((1 / cur_scale) * 1, 1)
    context.scale((rect_width / text_width), 1)
    context.show_text(text)
    context.restore()


def counter_box(context, counter_name, staff, pos, OUTLINE=100, SCREEN_WIDTH=3508, gap_x=50, rect_dim=None,
                font_family="Arial", font_size=45, subtext_font_size=35, font_weight=cairo.FONT_WEIGHT_BOLD):
    context.save()
    context.scale(1, 1)

    total_counter = len(counter_name.values())

    # setting color of the context
    context.set_source_rgb(0, 0, 0)
    # approximate text height
    context.set_font_size(font_size)
    # Font Style
    context.select_font_face(
        font_family, cairo.FONT_SLANT_NORMAL, font_weight)
    posx = pos[0]
    posy = pos[1]
    posx = posx * (1)
    paragraph_margin = 0

    xbearing, ybearing, l_width, l_height, dx, dy = context.text_extents(longest_string(list(counter_name.values())))
    rect_width = (l_width + font_size + l_height)
    print(dx)
    total_width = (rect_width + gap_x) * (total_counter)

    if (posx - OUTLINE < total_width):
        print(total_width)
        print(posx - OUTLINE)
        scale = ((posx - OUTLINE) / total_width)
        print(scale)
        context.scale(scale, 1)
        posx = posx * (1 / scale)
        is_scaled = True

    # setting of line width
    context.set_line_width(7)
    scaled_rect_width = rect_width * scale - font_size
    print("width", rect_width)
    print("counter len", len(counter_name))
    for idx, text in counter_name.items():
        # approximate text height
        xbearing, ybearing, width, height, dx, dy = context.text_extents(text)

        temp_text = text.split()
        if (len(temp_text) > 2):
            xbearing, ybearing, width, height, dx, dy = context.text_extents(temp_text[0] + " " + temp_text[1])
            scaled_width = width * (1 / scale) * (scaled_rect_width / width)
            context.move_to(posx - scaled_width / 2, posy + paragraph_margin - (font_size / 3))
            scaled_text(context, scale, scaled_rect_width, width, temp_text[0] + " " + temp_text[1])
            context.move_to(posx - width / 2, posy + paragraph_margin + (font_size / 1.5))
            scaled_text(context, scale, scaled_rect_width, width, temp_text[2])
            paragraph_margin += height + font_size
        elif (len(temp_text) < 1):
            pass
        else:
            scaled_width = width * (1 / scale) * (scaled_rect_width / width)
            context.move_to(posx - scaled_width / 2, posy + paragraph_margin)
            scaled_text(context, scale, scaled_rect_width, width, text)
            paragraph_margin += height + font_size

        rect_height = (paragraph_margin + (font_size))

        rect_x = posx - (l_width / 2 + font_size)
        rect_y = posy - (l_height + font_size)
        # branch if rectangle dimension is set force the dimension on it
        context.rectangle(rect_x, rect_y, rect_width, rect_height)

        context.rectangle(rect_x, rect_y + rect_height, rect_width / 2, rect_height)
        context.rectangle(rect_x + (rect_width / 2), rect_y + rect_height, rect_width / 2, rect_height)

        height_multiplier = 5.5
        subtext_y = rect_y + 2 * rect_height
        subtext_height = rect_height * height_multiplier
        subtex_width = rect_width / 2
        context.rectangle(rect_x, subtext_y, subtex_width, subtext_height)
        context.rectangle(rect_x + (rect_width / 2), subtext_y, subtex_width, subtext_height)

        context.save()
        context.scale(1 / scale, 1)
        text_a_x = rect_x * scale + (rect_width / 4) * scale
        text_a_y = subtext_y + (subtext_height / 2)
        text_rotation(context, staff[idx][0], (text_a_x, text_a_y),
                      theta=270 * (math.pi / 180),
                      face='Arial',
                      font_size=font_size)

        text_b_x = rect_x * scale + (rect_width / 4) * scale + (rect_width / 2) * scale
        text_b_y = subtext_y + (subtext_height / 2)
        text_rotation(context, staff[idx][1], (text_b_x, text_b_y),
                      theta=270 * (math.pi / 180),
                      face='Arial',
                      font_size=font_size)
        posx -= (gap_x + rect_width)
        paragraph_margin = 0

        context.restore()
        context.stroke()

    context.restore()

    return rect_width

def create_reports(data):
    SCREEN_WIDTH = data.get("screen_width", 4000)
    SCREEN_HEIGHT =  data.get("screen_height", 4000)
    DATE = data.get("date", datetime.datetime.now().strftime("%d %B %Y"))
    SHIFT = data.get("shift", "default shift")
    RIKSA = data.get("riksa","default riksa") + "." + data.get("subriksa", "default subriksa")
    TITLE = data.get("title","default title")
    OUTLINE = data.get("outline",100)
    coordinate_map = data.get("coordinate_map",{"SUMMARY": (3300, 200)})
    TITLE_FONT_SIZE = data.get("title_font_size",50)
    FONT_SIZE = data.get("font_size", 35)
    SUBTEXT_FONT_SIZE = data.get("subtext_font_size",35)
    RUANG = [ruang for ruang in coordinate_map if "SUMMARY" != ruang]
    MEMBERS_RUANG = data.get("members_ruang", {})

    COUNTER_NO = data.get("counter_no")

    COUNTER_STAFF = data.get("counter_staff")
    COUNTER_X = data.get("counter_x")
    COUNTER_Y = data.get("counter_y")
    POSITION = data.get("position")
    GAP_X = 0
    filename = TITLE+data.get("riksa","default riksa")+"sub"+data.get("subriksa", "default subriksa")+''.join(filter(str.isalnum, DATE))+SHIFT+ ".pdf"
    path: str = "productionfiles/reports/" + filename

    # path
    print(path,SCREEN_HEIGHT,SCREEN_WIDTH)
    with cairo.PDFSurface(path, SCREEN_WIDTH, SCREEN_HEIGHT) as surface:
        # creating a rectangle(square)
        context = cairo.Context(surface)
        outline(context, SCREEN_HEIGHT, SCREEN_WIDTH, OUTLINE)
        title(context, TITLE, SCREEN_WIDTH, font_size=TITLE_FONT_SIZE)
        summary(context, DATE, SHIFT, RIKSA, coordinate_map["SUMMARY"],
                font_size=FONT_SIZE + 10)

        for text in RUANG:
            text_box(context, [text], MEMBERS_RUANG[text], coordinate_map[text],
                     font_size=FONT_SIZE,
                     subtext_font_size=SUBTEXT_FONT_SIZE)

        counter_box(context, COUNTER_NO, COUNTER_STAFF, POSITION,
                    gap_x=GAP_X,
                    font_size=FONT_SIZE - 5,
                    subtext_font_size=10,
                    font_weight=cairo.FONT_WEIGHT_NORMAL)

        context.stroke()

    return path


