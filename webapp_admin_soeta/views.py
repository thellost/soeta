from django.shortcuts import render, redirect, reverse

from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
import math
from cairo_utils import *
from django.template import loader
from firebase_utils import create_employees_document, get_users, search_employee_by_name, get_templates, get_name
from cairo_utils import create_reports
from django.views.decorators.csrf import csrf_protect


def index(request):
    print(request)
    if request.method == "POST":
        # handling create account
        create_employees_document(request.POST.dict())
        HttpResponseRedirect(reverse('index'))

    # handling html view
    page = int(request.GET.get('page', 1))
    show = int(request.GET.get('show', 10))
    user_list = get_users()
    employee_num = len(user_list)
    num_of_shows = [10, 20, 30, 50]
    num_of_pages = [*range(1, math.ceil(employee_num / show) + 1)]
    print(num_of_pages)

    context = {
        'page': page,
        'show': show,
        "employee_num": employee_num,
        "num_of_shows": num_of_shows,
        "num_of_pages": num_of_pages,
        "employees": user_list[show * (page - 1):(page * show)]
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


def dashboard(request):
    with cairo.PDFSurface("productionfiles/reports/2FIIIsubII09132023Sore.pdf", 1000, 100) as surface:
        print("something")
    template = loader.get_template('dashboard.html')

    return HttpResponse(template.render({}, request))


def download_file(request):
    SCREEN_WIDTH = 4208
    SCREEN_HEIGHT = 2480
    DATE = "14 AGUSTUS 2023"
    SHIFT = "MALAM II"
    RIKSA = "Riksa IV.4"
    TITLE = "LAYOUT TERMINAL 3 KEBERANGKATAN"
    OUTLINE = 50
    coordinate_map = {
        "SUMMARY": (3300, 200),
        "MEJA POLSUS 1": (1400, 550),
        "MEJA POLSUS 2": (700, 550),
        "Anrtian Autogate": (3200, 1000),
        "AUTOGATE": (3200, 1400),
        "TU": (3800, 1000)
    }
    TITLE_FONT_SIZE = 50
    FONT_SIZE = 35
    SUBTEXT_FONT_SIZE = 35
    RUANG = ["MEJA POLSUS 1", "MEJA POLSUS 2", "Anrtian Autogate", "AUTOGATE", "TU"]
    MEMBERS_RUANG = {
        "MEJA POLSUS 1": ["Suherman", "Encep", "Iman Rohiman", "Iman Rohiman", "M Rusli"],
        "MEJA POLSUS 2": ["Ahmad", "Nurdin"],
        "Anrtian Autogate": ["SALSABILA", "SABILA", "ZORDY", "BAYHAQI"],
        "AUTOGATE": ["APRIYANTO"],
        "TU": ["Adegutama", "Arrachman", "Ikrar", "Gilang", "Rabbani", "Mora", "Parlindungan"]

    }

    COUNTER_NO = {
        1: "CREW",
        2: "PRIORITY & GARUDA",
        3: "DIPLOMATIC & ABTC",
        4: "PEKERJA MIGRAN INDONESIA",
        5: "INDONESIA",
        6: "INDONESIA",
        7: "INDONESIA",
        8: "INDONESIA",
        9: "FOREIGNER",
        10: "FOREIGNER",
        11: "FOREIGNER",
        12: "FOREIGNER",
        13: "FOREIGNER",
        14: "",
        15: "",
        16: ""
    }

    COUNTER_STAFF = {
        1: ["ALVIN", ""],
        2: ["RAMA", ""],
        3: ["", "AFFANDI"],
        4: ["RESTU", ""],
        5: ["NANDI", "SAIFAN"],
        6: ["", "ALDY"],
        7: ["IKHSAN", ""],
        8: ["FIKRIE", "ANDR"],
        9: ["", "CAHYO"],
        10: ["SURYA", "RAZQI"],
        11: ["", "ZULFIKAR"],
        12: ["", "ALFRIDA"],
        13: ["PANDU", "HERY"],
        14: ["", ""],
        15: ["", ""],
        16: ["", ""]
    }
    COUNTER_X = 2700
    COUNTER_Y = 960
    GAP_X = 0
    filename = TITLE + ".pdf"
    path: str = "download/" + filename

    # path
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

        counter_box(context, COUNTER_NO, COUNTER_STAFF, (COUNTER_X, COUNTER_Y),
                    gap_x=GAP_X,
                    font_size=FONT_SIZE - 5,
                    subtext_font_size=10,
                    font_weight=cairo.FONT_WEIGHT_NORMAL)

        context.stroke()

    response = FileResponse(open(path, 'rb'))
    return response


@csrf_protect
def reports(request):
    if request.method == "POST":
        print(request.POST)
        nama_counter = request.POST.getlist("namacounter")
        nama_meja = request.POST.getlist("namameja")
        xPositionMeja = request.POST.getlist("xPositionMeja")
        yPositionMeja = request.POST.getlist("yPositionMeja")

        coordinate_map = {}
        members_ruang = {}
        counter_no = {}
        counter_member = {}
        for idx, name in enumerate(nama_counter):
            counter_no[idx + 1] = name
            counter_member[idx + 1] = request.POST.getlist("membercounter" + str(idx + 1), ["", ""])
            if len(counter_member[idx + 1]) < 2:
                counter_member[idx + 1].append('')
            counter_member[idx + 1] = list(map(get_name, counter_member[idx + 1]))

        for idx, name in enumerate(nama_meja):
            coordinate_map[name] = (int(xPositionMeja[idx]), int(yPositionMeja[idx]))
            members_ruang[name] = request.POST.getlist("membermeja" + str(idx + 1), [""])
            members_ruang[name] = list(map(get_name, members_ruang[name]))


        data = get_templates(request.POST.getlist("template")[0])
        data["counter_no"] = counter_no
        data["counter_staff"] = counter_member
        data["coordinate_map"] = coordinate_map
        data["members_ruang"] = members_ruang
        data["riksa"] =  request.POST.getlist("riksa")[0]
        data["subriksa"] = request.POST.getlist("subriksa")[0]
        data["date"] = request.POST.getlist("date")[0]
        data["shift"] = request.POST.getlist("shift")[0]
        path = create_reports(data)
        response = FileResponse(open(path, 'rb'))
        return response

    template = loader.get_template('reports.html')
    return HttpResponse(template.render({}, request))


def listing_api(request):
    page_number = request.GET.get("page", 1)
    per_page = request.GET.get("per_page", 2)
    startswith = request.GET.get("startswith", None)

    if startswith is None:
        paginator = Paginator(get_users(), per_page)
    else:
        paginator = Paginator(search_employee_by_name(startswith, per_page), per_page)

    page_obj = paginator.get_page(page_number)
    data = [{"nip": emp["nip"],
             "full_name": emp["full_name"],
             "email": emp["email"],
             "nickname": emp["nickname"],
             "riksa": emp["riksa"],
             "subriksa": emp["subriksa"]
             } for emp in page_obj.object_list]

    payload = {
        "page": {
            "current": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
        },
        "data": data,
    }
    return JsonResponse(payload)


def select2_user(request):
    users = get_users()
    for user in users:
        user["text"] = user.get("nickname")
        user["id"] = user.get("nip")
    return JsonResponse(users, safe=False)


def listing_template(request):
    template_dict = {}
    for template in get_templates():
        template_dict[template['title']] = template

    return JsonResponse(template_dict)
