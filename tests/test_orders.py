import sys


def test_myoutput(capsys):
    print("hello")
    print("hellow")
    print("hellor")
    sys.stderr.write("world\n")
    captured = capsys.readouterr()
    assert "hellor" in captured.out.split('\n')
    assert captured.err == "world\n"
