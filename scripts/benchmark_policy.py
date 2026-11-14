"""Fixed input identity for a controlled HST comparison, not an LLM speed claim."""
import hashlib
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def input_digest(text):
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    for key in ['ID гипотезы', 'Дата создания', 'ID прогона', 'Статус']:
        text = re.sub(r'(?m)^- ' + re.escape(key) + r':[^\n]*$', '- ' + key + ': <identity>', text)
    return hashlib.sha256(text.strip().encode('utf-8')).hexdigest()


def metadata(run, case_id, model_label):
    if case_id != 'pipeline-001': raise ValueError('Unknown benchmark case')
    if not model_label or not model_label.strip(): raise ValueError('Benchmark requires --model-label with the actual model/settings label')
    source = ROOT / 'benchmarks/pipeline-001/hypothesis.md'
    expected = input_digest(source.read_text(encoding='utf-8'))
    actual = input_digest((Path(run) / 'input/hypothesis.md').read_text(encoding='utf-8-sig'))
    if actual != expected: raise ValueError('Benchmark input differs from pipeline-001; do not rephrase the fixed card')
    return {'case_id': case_id, 'input_sha256': actual,
            'channels': {'local': False, 'confluence': False, 'internet': False},
            'retrieval_review': 'waived_by_benchmark_prompt'}


def validate(run):
    import json
    run=Path(run)
    config_path=run/'run_config.json'
    if not config_path.exists():return []
    config=json.loads(config_path.read_text(encoding='utf-8-sig'))
    frozen=config.get('benchmark')
    if frozen is None:return []
    if not isinstance(frozen,dict) or frozen.get('case_id')!='pipeline-001':return ['INVALID_BENCHMARK_METADATA']
    errors=[]
    if input_digest((run/'input/hypothesis.md').read_text(encoding='utf-8-sig')) != frozen.get('input_sha256'):
        errors.append('BENCHMARK_INPUT_CHANGED')
    if not config.get('model_label'):errors.append('MISSING_BENCHMARK_MODEL_LABEL')
    expected={'local':False,'confluence':False,'internet':False}
    if frozen.get('channels')!=expected or config.get('source_selection',{}).get('channels')!=expected:
        errors.append('BENCHMARK_SOURCE_CHANNELS_CHANGED')
    return errors
