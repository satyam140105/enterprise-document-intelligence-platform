"""Smoke tests — expand during implementation."""

def test_package_importable():
    import docintel

    assert docintel.__version__
