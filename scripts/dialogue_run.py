"""File bootstrap used by the TUI transport, never an analysis orchestrator.

Chat agents write the same files directly using implementations/dialogue-run.md.
No viewer, validation, research or next-phase selection happens here.
"""
import json
from pathlib import Path
from datetime import datetime, timezone


def initialize(run, workspace, *, started_at=None, model_label=None):
    from run_progress import atomic, init, record
    from active_run import publish
    run = Path(run).resolve()
    if (run / 'run_config.json').exists():
        raise ValueError('New dialogue run already configured; do not reset history')
    config = dict(protocol_version=2, audit_version=2, execution_driver='dialogue',
                  execution_mode='full', source_selection_version=1, timing_version=1,
                  framework_version=(Path(__file__).resolve().parents[1]/'VERSION').read_text().strip(),
                  model_label=model_label, started_at=started_at or datetime.now(timezone.utc).isoformat(),
                  heavy_analysis='ask', analysis_choices=[])
    atomic(run/'run_config.json', json.dumps(config, ensure_ascii=False, indent=2))
    init(run)
    record(run, phase='intake', state='completed', message='Гипотеза и папка подтверждены в диалоге')
    record(run, phase='validation', state='running', message='Проверяю смысл и полноту входных данных')
    publish(run, workspace)
    return config
