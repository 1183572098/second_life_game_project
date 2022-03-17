from unittest import TestCase
from django.contrib.auth.models import User
from game.models import Announcement


class AnnouncementClassTest(TestCase):
    def test_title_not_null(self):
        announcement = Announcement(title=None, content='test')
        error_message = ""
        try:
            announcement.save()
        except Exception as e:
            error_message = str(e)
        self.assertEqual(error_message, '(1048, "Column \'title\' cannot be null")')

    def test_content_not_null(self):
        announcement = Announcement(title="test", content=None)
        error_message = ""
        try:
            announcement.save()
        except Exception as e:
            error_message = str(e)
        self.assertEqual(error_message, '(1048, "Column \'content\' cannot be null")')

    def test_title_max_length(self):
        title = ''
        for i in range(30):
            title = title + "test"
        announcement = Announcement(title=title, content=None)
        error_message = ""
        try:
            announcement.save()
        except Exception as e:
            error_message = str(e)
        self.assertEqual(error_message, '(1406, "Data too long for column \'title\' at row 1")')

    def test_content_max_length(self):
        content = ''
        for i in range(100):
            content = content + "test_content_max_length"
        announcement = Announcement(title="test", content=content)
        error_message = ""
        try:
            announcement.save()
        except Exception as e:
            error_message = str(e)
            # print(error_message)
        self.assertEqual(error_message, '(1406, "Data too long for column \'content\' at row 1")')

    def test_ensure_save_correctly(self):
        announcement = Announcement(title='test', content='test')
        announcement.save()
        self.assertEqual((announcement.title == 'test'), True)

