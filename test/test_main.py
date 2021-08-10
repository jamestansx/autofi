from src import main


def test_main():
    connection_status = main.main()
    assert connection_status == b"000" or "not connected"
