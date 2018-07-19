from pathlib import Path

from repo_tokenizer import breakup_identifiers, ALL_CAPS, lex, tokenize_file, SPACE, tokenize_repo


def test_tokenize_word():
    assert breakup_identifiers('data_len') == ['data', 'len']
    assert breakup_identifiers('dataLen') == ['data', 'len']
    assert breakup_identifiers('DATA_LEN') == [ALL_CAPS, 'data', 'len']
    assert breakup_identifiers('data2') == ['data', '2']
    assert breakup_identifiers('LICENSE') == [ALL_CAPS, 'license']


def test_lex():
    assert lex('if(n2 == 5) { return \'OK\' }') == ['if', '(', 'n2', SPACE, '=', '=', SPACE, '5', ')', SPACE, '{', SPACE,
                                                    'return', SPACE, "'", 'OK', "'", SPACE, '}']


def test_tokenize_file():
    repo_root = Path('repo_test_files')
    res = ' '.join(tokenize_file(repo_root / 'example.js', repo_root))
    assert res == '~!~$start_file example .js ~!~$stop  /  * ~!~$spc ~!~$spc  * ~!~$spc  copyright ~!~$spc  2 0 1 8 ' \
                  '~!~$spc  palantir ~!~$spc  technologies  , ~!~$spc  inc  . ~!~$spc  all ~!~$spc rights ~!~$spc ' \
                  'reserved  . ~!~$spc ~!~$spc  * ~!~$spc ~!~$spc  * ~!~$spc  licensed ~!~$spc under ~!~$spc the ' \
                  '~!~$spc terms ~!~$spc of ~!~$spc the ~!~$spc ~!~$all_caps license ~!~$spc file ~!~$spc distributed ' \
                  '~!~$spc with ~!~$spc this ~!~$spc project  . ~!~$spc ~!~$spc  *  / ~!~$spc ~!~$spc  /  *  * ~!~$spc  ' \
                  'alignment ~!~$spc along ~!~$spc the ~!~$spc horizontal ~!~$spc axis  . ~!~$spc  *  / ~!~$spc export ' \
                  '~!~$spc const ~!~$spc  alignment ~!~$spc  = ~!~$spc  { ~!~$spc ~!~$spc ~!~$spc ~!~$spc ~!~$spc ' \
                  '~!~$all_caps center  : ~!~$spc  " center  " ~!~$spc as ~!~$spc  " center  "  , ~!~$spc ~!~$spc ' \
                  '~!~$spc ~!~$spc ~!~$spc ~!~$all_caps left  : ~!~$spc  " left  " ~!~$spc as ~!~$spc  " left  "  , ' \
                  '~!~$spc ~!~$spc ~!~$spc ~!~$spc ~!~$spc ~!~$all_caps right  : ~!~$spc  " right  " ~!~$spc as ' \
                  '~!~$spc  " right  "  , ~!~$spc  }  ; ~!~$spc export ~!~$spc type ~!~$spc  alignment ~!~$spc  ' \
                  '= ~!~$spc typeof ~!~$spc  alignment  [ keyof ~!~$spc typeof ~!~$spc  alignment  ]  ;'

def test_tokenize_repo():
    with open('test_output', 'w') as f:
        f.write(' '.join(tokenize_repo('test_folders', Path('repo_test_files/test_folders'))))

