from django.test import TestCase
from .util import convert_markdown_to_html_text

# Create your tests here.

class MarkDown_Converter(TestCase):

    def test_header_input(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        self.assertIs(convert_markdown_to_html_text("##########Fake Title"), False)




