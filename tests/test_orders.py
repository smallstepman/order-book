import sys
import os


def test_files(capsys, app):
    """
        this was very romantic idea
        but worthless
    """
    for f in os.listdir('tests/test_data'):
        if f.endswith('.in'):
            in_file = os.path.join(os.path.abspath('./tests/test_data'), f)
            app.run_from_file(in_file)
            captured = capsys.readouterr()
            out_file = os.path.join(os.path.abspath(
                './tests/test_data'), f.replace('.in', '.out'))
            with open(out_file) as f:
                out_data = f.readlines()
                for line in out_data:
                    assert line.replace('\n', '') in captured.out

