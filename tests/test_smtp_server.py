from email.parser import Parser
from email.policy import default
from server import parse_payload_tree


def test_parse_payload_tree(raw_text_mail, expected_text_html, expected_text_plain):
    """Test parse_payload_tree with text mail."""
    mime_data = Parser(policy=default).parsestr(raw_text_mail)
    parsed_data = parse_payload_tree(mime_data)
    assert parsed_data['text/plain'] == expected_text_plain
    assert parsed_data['text/html'] == expected_text_html


def test_parse_payload_tree_image(raw_image_mail, expected_text_html_image, expected_text_plain_image):
    """Test parse_payload_tree with text mail."""
    mime_data = Parser(policy=default).parsestr(raw_image_mail)
    parsed_data = parse_payload_tree(mime_data)
    assert parsed_data['text/plain'] == expected_text_plain_image
    assert parsed_data['text/html'] == expected_text_html_image
    assert 'images' in parsed_data
    assert 'ii_kcx5p4ld0' in parsed_data['images']
