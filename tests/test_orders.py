import sys

from src.app import run_from_file


def test_files(capsys):
    for f in os.listdir(test_data):
        run_from_file(f)
        captured = capsys.readouterr()
        with open(f.replace('.in', '.out')) as f:
            assert f.readlines() == captured.out.split('\n')
