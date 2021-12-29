from datacenter.models import *
from commendations import COMMENDATIONS
import random
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def get_correct_schoolkid(name_schoolkid: str):
    """Return correct database entry

    Args:
        name_schoolkid (str): format

    Returns:
        object: database entry or exception
    """
    try:
        schoolkid = Schoolkid.objects.get(full_name=name_schoolkid)
    except ObjectDoesNotExist:
        print('Schoolkid not found, please check name')
    except MultipleObjectsReturned:
        print('More than one Schoolkid found, please check name')
    return schoolkid


def fix_marks(schoolkid_name: str):
    """Replace marks schoolkid by schoolkid name,
    when mark >= 3 then replace 5

    Args:
        schoolkid_name (str): format 'Фамилия Имя Отчество'
    """
    schoolkid = get_correct_schoolkid(schoolkid_name)
    all_bad_points = Mark.objects.filter(
        schoolkid=schoolkid,
        points__lte=3
        )
    for bad_point in all_bad_points:
        bad_point.points = 5
        bad_point.save()


def remove_chastisements(schoolkid_name: str):
    """Delete chastiments by schoolkid name

    Args:
        schoolkid_name (str): format 'Фамилия Имя Отчество'
    """
    schoolkid = get_correct_schoolkid(schoolkid_name)
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid_name: str, subject_name: str):
    """Create commendation by schoolkid name and subject

    Args:
        schoolkid_name (str): format 'Фамилия Имя Отчество'
        subject_name (str): format example 'Музыка'
    """
    schoolkid = get_correct_schoolkid(schoolkid_name)
    try:
        last_lesson = Lesson.objects.filter(
            year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter,
            subject__title__contains=subject_name).order_by('-date')[0]
        Commendation.objects.create(
            text=random.choice(COMMENDATIONS),
            created=last_lesson.date,
            schoolkid=schoolkid,
            subject=last_lesson.subject, teacher=last_lesson.teacher)
    except IndexError:
        print('Check correct subject name')
