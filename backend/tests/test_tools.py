from app.tools.python_analysis import run_python


def test_run_python():
    """Test the Python analysis tool with basic quantitative reasoning."""
    code = "result = (82 + 91 + 87) / 3\nprint(f'Average: {result:.2f}')"
    output = run_python(code)
    assert "Average: 86.67" in output


def test_run_python_error():
    """Test the Python analysis tool handles errors gracefully."""
    code = "1 / 0"
    output = run_python(code)
    assert "ZeroDivisionError" in output
