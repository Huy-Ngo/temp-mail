from pytest import fixture
from json import load

with open('data.json', 'r') as f:
    data = load(f)


@fixture
def raw_text_mail():
    global data
    return data['raw-text-mime']


@fixture
def raw_image_mail():
    global data
    return data['raw-image-mime']


@fixture
def html():
    pass
