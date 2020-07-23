#  Copyright (c) 2020  Ngô Ngọc Đức Huy

from email.parser import Parser
from email.policy import default
from quopri import decodestring

from server import parse_payload_tree, replace_image


def test_parse_payload_tree(raw_text_mail, expected_text_html, expected_text_plain):
    """Test parse_payload_tree with text mail."""
    mime_data = Parser(policy=default).parsestr(raw_text_mail)
    parsed_data = parse_payload_tree(mime_data)
    assert parsed_data['text/plain'] == expected_text_plain
    assert parsed_data['text/html'] == expected_text_html


def test_parse_payload_tree_image(raw_image_mail, expected_text_html_image, expected_text_plain_image, expected_images):
    """Test parse_payload_tree with text mail."""
    mime_data = Parser(policy=default).parsestr(raw_image_mail)
    parsed_data = parse_payload_tree(mime_data)
    assert parsed_data['text/plain'] == expected_text_plain_image
    assert parsed_data['text/html'] == expected_text_html_image
    assert 'images' in parsed_data
    assert expected_images == parsed_data['images']


def test_replace_image(expected_text_html_image, expected_images, expected_replaced_html):
    expected_text_html_image = decodestring(expected_text_html_image).decode()
    html = replace_image(expected_text_html_image, expected_images)
    assert html == expected_replaced_html
