from pytest import fixture
from json import load

with open('data.json', 'r') as f:
    data = load(f)


@fixture
def raw_text_mail():
    """MIME data received from a text mail sent from Gmail."""
    global data
    return data['raw-text-mime'].encode('utf-8')


@fixture
def raw_image_mail():
    """MIME data received from a mail with an image sent from Gmail."""
    global data
    return data['raw-image-mime']


@fixture
def html():
    """HTML representation of a mail."""
    pass
