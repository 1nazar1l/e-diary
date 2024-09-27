from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation, Subject
import random

def search_kid(child_name):
    try:
        school_kid = Schoolkid.objects.get(full_name__contains=child_name)
        return school_kid
    except Schoolkid.DoesNotExist:
        print("Не найдено ни одного ученика. Перепроверьте корректно ли написано имя или фамилия")
    except Schoolkid.MultipleObjectsReturned:
        print("Найдено несколько учеников, укажите более точные данные")


def fix_marks(school_kid):
    marks = Mark.objects.filter(schoolkid=school_kid)
    marks.filter(points__in=[2, 3]).update(points=5)
    

def remove_chastisements(school_kid):
    bad_remarks = Chastisement.objects.filter(schoolkid=school_kid) 
    bad_remarks.delete()   


def create_commendation(school_child, subject):
    good_praises = ["Хорошая работа на уроке","Отлично отвечал","Хвалю!", "Молодец!", "Лучше всех", "Замечательно!"]
    good_praise = random.choice(good_praises)
    year_of_study = school_child.year_of_study
    group_letter = school_child.group_letter
    if Subject.objects.filter(title=subject).exists():
        lessons = Lesson.objects.filter(year_of_study=year_of_study, group_letter=group_letter, subject__title=subject)
        lesson = lessons.order_by("date").last()
        Commendation.objects.create(text=good_praise,created=lesson.date, schoolkid=school_child, teacher=lesson.teacher, subject=lesson.subject)
    else:
        print("Перепроверьте название предмета или напишите его с большой буквы")