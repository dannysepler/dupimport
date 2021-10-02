import argparse
import ast
import warnings
from pathlib import Path
from typing import Optional, Sequence, Set, Tuple, Union

BOLD = '\033[1m'
END = '\033[0m'


class ImportVisitor(ast.NodeVisitor):
    def __init__(self):
        self.imports: Set[Tuple[str, str]] = set()
        self.dups = set()

    def check_for_dupes(self, node, module=None) -> None:
        for alias in node.names:
            name = alias.name or alias.asname
            if (module, name) in self.imports:
                if name not in self.dups:
                    self.dups.add(name)
            self.imports.add((module, name))

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        self.check_for_dupes(node, module=node.module)

    def visit_Import(self, node: ast.Import) -> None:
        self.check_for_dupes(node)


def ast_parse(contents: str) -> ast.Module:
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        return ast.parse(contents)


def find_dup_imports(contents: str) -> Set[str]:
    parsed = ast_parse(contents)

    visitor = ImportVisitor()
    visitor.visit(parsed)
    return visitor.dups


def _check_path(filepath: Union[str, Path], ignore_syntax_err: bool) -> int:
    path = Path(filepath)
    if not path.exists():
        ValueError(f"Path: '{filepath}' does not exist")
    if path.is_dir():
        return sum(
            _check_path(f, ignore_syntax_err) for f in path.glob('**/*.py')
        )

    try:
        contents = path.read_text()
        dups = find_dup_imports(contents)
    except SyntaxError:
        if not ignore_syntax_err:
            print(f'Skipping file {path} because of syntax errors')
        return 0

    if dups:
        print(
            f"Duplicated import(s) {BOLD}{', '.join(sorted(dups))}{END} "
            'found in {path}',
        )
        return 1
    else:
        return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filepaths', nargs='*')
    parser.add_argument('--ignore-syntax-err', action='store_true')
    args = parser.parse_args(argv)

    ret = 0
    for filepath in args.filepaths:
        ret += _check_path(filepath, args.ignore_syntax_err)
    return ret


if __name__ == '__main__':
    exit(main())
