import os
from django import template
from datetime import date, timedelta
from ..models import *

register = template.Library()

INTEREST_LIST = {
    'Machine Learning',
    'Data Science',
    'Cryptography',
    'Data Structure and Algorithm',
    'Mathematics',
    'Image Processing'
    'Electrial Engineering',
    'Research'
}

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

skills = [ 'competitive coding', 'web development', 'android development', 'machine learning']

tags = ['computer-science-and-artificial-intelligence-laboratory-csail', 'computer-vision',
                'electrical-engineering-computer-science-eecs', 'imaging', 'research']

tag_link = {'Artificial Intelligence':'computer-science-and-artificial-intelligence-laboratory-csail',
            'Data Structure and Algorithm':'computer-vision',
            'Image Processing': 'imaging',
            'Electrial Engineering':'electrical-engineering-computer-science-eecs',
            'Research': 'reasearch',
            }

@register.filter(name='assignments_in_topic')
def assignments_in_topic(assignments,topic):
    return Assignment.objects.filter(parent_topic=topic)

@register.filter(name='material_in_topic')
def material_in_topic(assignments,topic):
    return Course_Material.objects.filter(parent_topic=topic)

@register.filter(name='quizzes_in_topic')
def quizzes_in_topic(quizzes,topic):
    return Quiz.objects.filter(parent_topic=topic)

@register.filter(name='interest_name')
def interest_name(news_feeds):
    return map(lambda x: x.interest_name, news_feeds)