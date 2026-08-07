import unittest
import os
import app


class TestKakeiboApp(unittest.TestCase):

    def test_create_file(self):
        app.create_file()
        self.assertTrue(os.path.exists(app.FILE_NAME))


if __name__ == "__main__":
    unittest.main()
