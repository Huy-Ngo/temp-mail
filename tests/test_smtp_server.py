from email.parser import Parser
from email.policy import default
from server import parse_payload_tree


def test_parse_payload_tree(raw_text_mail, expected_text_html, expected_text_plain):
    """Test parse_payload_tree with text mail."""
    mime_data = Parser(policy=default).parsestr(raw_text_mail)
    parsed_data = parse_payload_tree(mime_data)
    assert parsed_data['text/plain'] == expected_text_plain
    assert parsed_data['text/html'] == expected_text_html

