import pytest

from dupimport import find_dup_imports


@pytest.mark.parametrize(
    'text, output', [
        ('from pathlib import Path, Path', {'Path'}),
        ('from a import one, two, one', {'one'}),
        ('from a import one, one, two, two', {'one', 'two'}),
        (
            'from a import one\n'
            'from a import one',
            {'one'},
        ),
    ],
)
def test_finds_duplicated_imports(text, output):
    assert find_dup_imports(text) == output


@pytest.mark.parametrize(
    'text', [
        'from pathlib import Path',
        'from pathlib import Path, AnotherPath',
        (
            'from pathlib import Path\n'
            'from os import Path as AnotherPath'
        ),
        (
            'if some_var:\n'
            '    from a import one\n'
            'else:\n'
            '    from b import one'
        ),
    ],
)
def test_doesnt_find_duplicated_imports(text):
    assert find_dup_imports(text) == set()
