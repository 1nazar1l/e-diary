from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation, Subject
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import random

def search_kid(child_name):
    try:
        child = Schoolkid.objects.get(full_name__contains=child_name)
        full_name = child.full_name
        return full_name
    except ObjectDoesNotExist:
        print("Не найдено ни одного ученика. Перепроверьте корректно ли написано имя или фамилия")
        return None
    except MultipleObjectsReturned:
        print("Найдено несколько учеников, укажите более точные данные")


def fix_marks(full_name):
    bad_marks = Mark.objects.filter(schoolkid__full_name=full_name)
    bad_marks.filter(points__in=[2, 3]).update(points=5)
    

def remove_chastisements(full_name):
    bad_remarks = Chastisement.objects.filter(schoolkid__full_name=full_name) 
    bad_remarks.delete()   


def create_commendation(full_name, subject):
    good_praises = ["Хорошая работа на уроке","Отлично отвечал","Хвалю!", "Молодец!", "Лучше всех", "Замечательно!"]
    good_praise = random.choice(good_praises)
    child = Schoolkid.objects.get(full_name=full_name)
    year_of_study = child.year_of_study
    group_letter = child.group_letter
    lessons = Lesson.objects.filter(year_of_study=year_of_study, group_letter=group_letter, subject__title=subject)
    lesson = lessons.order_by("date").first()
    Commendation.objects.create(text=good_praise,created=lesson.date, schoolkid=child, teacher=lesson.teacher, subject=lesson.subject)
    

def main():
    name = input("Введите имя ученика: ")
    full_name = search_kid(name)

    fix_marks(full_name)
    remove_chastisements(full_name)

    subject_title = input("Введите название предмета: ")
    if Subject.objects.filter(title=subject_title).count() != 0:
        create_commendation(full_name, subject_title)
    else:
        print("Перепроверьте название предмета или напишите его с большой буквы")


if __name__ == "__main__":  
    main()