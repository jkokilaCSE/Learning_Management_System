from django.shortcuts import render
from ..models import Faculty_details, Users, Room, ClassRooms, class_enrolled, Attendees
from django.shortcuts import render
from bing_image_downloader import downloader
from LMS.settings import BASE_DIR
from .Tool.Tools import get_user_mail, get_user_name, get_user_role, get_user_obj
import datetime
from .Tool.Code_scriping_Tool import get_image_url


def nave_home_classroom(request, pk, class_id):
    if pk == "join":
        try:
            if class_enrolled.objects.filter(mail_id=get_user_mail(request), subject_code=class_id).exists():
                print("connection passed...")
            else:
                class_en = class_enrolled(
                    mail_id=get_user_mail(request), subject_code=class_id)
                class_en.save()
        except:
            if class_enrolled.objects.filter(mail_id=request.user.username, subject_code=class_id).exists():
                print("connection passed...")
            else:
                class_en = class_enrolled(
                    mail_id=request.user.username, subject_code=class_id)
                class_en.save()
        peoples = []
        people = class_enrolled.objects.filter(subject_code=class_id)
        for i in people:
            print(i.class_id, i.mail_id)
            person_obj = Users.objects.get(mail_id=i.mail_id)
            peoples.append(person_obj)
        detials = ClassRooms.objects.get(subject_code=class_id)

        # create new chat room..........

        if Room.objects.filter(name=class_id).exists():
            return render(request, 'class_room/classroom.html', {'people': peoples, "detail": detials})
        else:
            new_room = Room.objects.create(name=class_id)
            new_room.save()
            return render(request, 'class_room/classroom.html', {'people': peoples, "detail": detials})
    elif pk == "attendes":
        peoples = []
        people = class_enrolled.objects.filter(subject_code=class_id)
        for i in people:
            print(i.class_id, i.mail_id)
            person_obj = Users.objects.get(mail_id=i.mail_id)
            peoples.append(person_obj)
        detials = ClassRooms.objects.get(subject_code=class_id)
        print([str(i.user_name) for i in peoples])
        return render(request, 'class_room/attendes.html', {'people': [[j, i] for i, j in enumerate(peoples)], "ids": [str(i.id) for i in peoples], "detail": detials, "date": datetime.datetime.now().date()})
    else:
        peoples = []
        people = class_enrolled.objects.filter(subject_code=class_id)
        test = class_enrolled.objects.all()
        detials = ClassRooms.objects.get(subject_code=class_id)

        for i in test:
            print(i.class_id, i.mail_id, i.subject_code)
        for i in people:
            print(i.class_id, i.mail_id, i.subject_code)
            person_obj = Users.objects.get(mail_id=i.mail_id)
            peoples.append(person_obj)
        if Room.objects.filter(name=class_id).exists():
            return render(request, 'class_room/classroom.html', {'people': peoples, "detail": detials})
        else:
            new_room = Room.objects.create(name=class_id)
            new_room.save()
            return render(request, 'class_room/classroom.html', {'people': peoples, "detail": detials})


def home_classroom(request):
    classes = []
    img = {}
    dep = []
    sem = [1, 2, 3, 4, 5, 6, 7, 8]
    try:
        enroll_classes = class_enrolled.objects.filter(
            mail_id=get_user_mail(request))
    except:
        enroll_classes = class_enrolled.objects.filter(
            mail_id=request.user.email)

    for i in enroll_classes:
        classrooms = ClassRooms.objects.filter(subject_code=i.subject_code)
        print(i.class_id)
        print(classrooms)
        for i in classrooms:
            print(i.id, i.class_name)
            classes.append(i)
            if i.department not in dep:
                dep.append(i.department)
    try:
        return render(request, 'class_room/class_room_home.html', {'classes': classes, 'img': img, 'sem_': sem, 'dep': dep, "user_name": get_user_name(request), "User_role": get_user_role(request), "usr_img": get_user_obj(request)})
    except:
        return render(request, 'class_room/class_room_home.html', {'classes': classes, 'img': img, 'sem_': sem, 'dep': dep, "user_name": request.user.username})


def add_class(request):
    return render(request, 'class_room/new_add.html')


def delete_class(request, room):
    class_room = ClassRooms.objects.get(id=room)
    class_room.delete()
    return render(request, 'class_room/new_add.html')


def save_add_class(request):
    class_name = request.POST.get('class_name')
    subject_code = request.POST.get('subject_code')
    department = request.POST.get('department')
    semester = request.POST.get('semester')
    discription = request.POST.get('discription')

    class_room = ClassRooms(class_image=get_image_url(class_name+" logos"), class_name=class_name, subject_code=subject_code,
                            department=department, semester=semester, discription=discription, owner=Faculty_details.objects.get(mail=get_user_mail(request)))
    class_room.save()
    class_id = ClassRooms.objects.get(subject_code=subject_code)
    enroll_class = class_enrolled(mail_id=get_user_mail(
        request), subject_code=subject_code, class_id=class_id.id)
    enroll_class.save()

    return render(request, 'class_room/new_add.html')


def attendes(request):
    return render(request, 'class_room/attendes.html')


def update_attendes(request):
    data: str = []
    print("length is : ", request.POST.get('length'))
    for i in range(int(request.POST.get('length'))):
        datas = request.POST.get('#cars'+str(i))
        data.append(datas)
    for i in data:
        splited = i.split('~~')
        print(i.split('~~'), i)
        if Attendees.objects.filter(class_id=splited[2], user_name=splited[1], subject_states=splited[0]).exists():
            print("Data Already Exists....")
        else:
            obj = Attendees(
                class_id=splited[2], user_name=splited[1], subject_states=splited[0]
            )
            obj.save()
        for i in Attendees.objects.all():
            print(i.user_name, i.subject_states)
    return render(request, 'class_room/attendes.html')
