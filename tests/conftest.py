#  Copyright (c) 2020  Ngô Ngọc Đức Huy

from pytest import fixture
from json import load

with open('tests/data.json', 'r') as f:
    data = load(f)


@fixture
def raw_text_mail():
    """MIME data received from a text mail sent from Gmail."""
    global data
    return data['text-mail']['raw']


@fixture
def expected_text_html():
    """Expected HTML representation of a mail (before quopri decode)."""
    global data
    return data['text-mail']['expected-html']


@fixture
def expected_text_plain():
    """Expected plain text of a mail."""
    global data
    return data['text-mail']['expected-plain']


@fixture
def raw_image_mail():
    """MIME data received from a mail with an image sent from Gmail."""
    global data
    return data['image-mail']['raw']


@fixture
def expected_text_html_image():
    """Expected HTML representation of a mail (before quopri decode)."""
    global data
    return data['image-mail']['expected-html']


@fixture
def expected_text_plain_image():
    """Expected plain text of a mail."""
    global data
    return data['image-mail']['expected-plain']


@fixture
def expected_images():
    global data
    return data['image-mail']['expected-images']


@fixture
def expected_replaced_html():
    global data
    return data['image-mail']['expected-replaced-html']
