import tempfile
from pathlib import Path
from typing import List, Optional
import click

special_prefix = '~!~$'
START_REPO = special_prefix + 'start_repo'
START_FILE = special_prefix + 'start_file'
START_FOLDER = special_prefix + 'start_folder'
ALL_CAPS = special_prefix + 'all_caps'
STOP = special_prefix + 'stop'
SPACE = special_prefix + 'spc'
UNKNOWN_REPO_NAME = special_prefix + 'unkrn'

def break_on(s: str, toks: List[str]):
    substr = ''
    res = []
    for c in s:
        if s in toks:
            if substr:
                res.append(substr)
                substr = ''
            res.append(c)
        else:
            substr += c
    return res



def breakup_path(path: str):
    return break_on(path, ['/'])

def breakup_identifiers(word: str):
    if word.startswith(special_prefix):
        return [word]
    if '_' in word:
        subwords = word.lower().split('_')
    elif all([c.isupper() for c in word]):
        subwords = [word.lower()]
    else:
        subwords = []
        current_word = ''
        for char in word:
            if not char.islower():
                subwords.append(current_word)
                current_word = ''
            current_word += char.lower()
        subwords.append(current_word)
    if all([not c.isalpha() or c.isupper() for c in word]) and any([c.isalpha() for c in word]):
        subwords.insert(0, ALL_CAPS)
    return subwords

def lex(text: str):
    tokens = []
    current_token = ''
    for char in text:
        if not char.isalnum() or char == '_':
            if current_token:
                tokens.append(current_token)
            tokens.append(char)
            current_token = ''
        else:
            current_token += char
    if current_token:
        tokens.append(current_token)
    return [SPACE if tok.isspace() else tok for tok in tokens]

def file_header(path: Path, repo_root):
    return [START_FILE, *breakup_path(path.relative_to(repo_root).as_posix()), STOP]

def folder_header(path: Path):
    return [START_FOLDER, *breakup_path(path.as_posix()), STOP]

def tokenize_file(path: Path, repo_root: Path):
    text = path.read_text()
    lexed = lex(text)
    tokenized = sum([breakup_identifiers(word) for word in lexed], [])
    return [*file_header(path, repo_root), *tokenized]

def tokenize_folder(path: Path, repo_root: Path):
    assert path.is_dir()
    res = folder_header(path.relative_to(repo_root))
    dirs = []
    for f in path.iterdir():
        if f.is_dir():
            dirs.append(f)
        else:
            res.extend(tokenize_file(f, repo_root))
    for dir in dirs:
        res.extend(tokenize_folder(dir, repo_root))
    return res

def tokenize_repo(repo_name: Optional[str], repo_path: Path):
    if repo_name is None:
        repo_name = UNKNOWN_REPO_NAME
    header = [START_REPO, repo_name, STOP]
    return [*header, *tokenize_folder(repo_path, repo_path)]

def read_until(iter, tok):
    res = []
    t = next(iter)
    while t != tok:
        res.append(t)
        t = next(iter)
    return res

def handle_special(tok, itr):
    special = next(itr)
    if special == START_REPO:
        repo_name = read_until(itr, STOP)
        print('Parsing repo: ', repo_name)
    elif special == START_FILE:
        pass


def reverse_tokenize(stream):
    target_dir = tempfile.NamedTemporaryFile()
    tokens = stream.split(' ')
    token_iter = iter(tokens)

    while True:
        try:
            tok = next(token_iter)
            if tok == special_prefix:
                pass

        except StopIteration:
            return target_dir


@click.command('')
@click.argument('repo-path', type=click.Path(exists=True, file_okay=True, dir_okay=True))
@click.option('--repo-name')
def main(repo_path: str, repo_name: str):
    repo_path = Path(repo_path)
    click.secho(' '.join(tokenize_repo(repo_name, repo_path)))


if __name__ == "__main__":
    main()
