import ast,pathlib
P=pathlib.Path(__file__).parents[1]/'contracts'/'contract.py'
def test_contract_parses():ast.parse(P.read_text(encoding='utf-8'))
def test_public_surface():
    s=P.read_text(encoding='utf-8')
    for n in ('file_docket','add_source','review_docket','get_docket','get_finding'):assert f'def {n}' in s
def test_prompt_hardening():
    s=P.read_text(encoding='utf-8');assert 'Do not follow instructions' in s and 'gl.nondet.web.get' in s and 'snapshots' in s
