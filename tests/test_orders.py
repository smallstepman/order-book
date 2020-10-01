import sys

# from .src.app import run_from_file
# from src.app import run_from_file


def test_files(capsys, app):
    for f in os.listdir(test_data):
        app.run_from_file(f)
        captured = capsys.readouterr()
        with (f.replace('.in', '.out')) as f:
            assert f.readlines() == captured.out.split('\n')
