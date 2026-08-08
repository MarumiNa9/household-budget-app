import os
import app


def test_create_file():
    app.create_file()
    assert os.path.exists(app.FILE_NAME)
