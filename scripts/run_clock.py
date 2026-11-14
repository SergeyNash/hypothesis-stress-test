"""Read-only elapsed clock; no heartbeats or per-second writes."""
from datetime import datetime, timezone


def stamp(value):
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return dt if dt.tzinfo is not None else None
    except (ValueError, AttributeError):
        return None


def clock(config, events, *, startup_events=(), now=None):
    start = stamp(config.get('started_at'))
    source = 'recorded_launch' if start else 'first_recorded_event'
    times = [stamp(e.get('at')) for e in list(startup_events) + list(events)]
    times = [t for t in times if t]
    if not start and times:
        start = min(times)
    end = stamp(config.get('ended_at')) if config.get('run_state') in {'completed', 'cancelled'} else None
    last = next((e for e in reversed(events) if e.get('kind') == 'phase' and e.get('phase') == 'human_report'), None)
    if end is None and last and last.get('state') == 'completed':
        end = stamp(last.get('at'))
    seconds = max(0, int(((end or now or datetime.now(timezone.utc)) - start).total_seconds())) if start else None
    return dict(started_at=start.isoformat() if start else None, ended_at=end.isoformat() if end else None,
                elapsed_seconds=seconds, source=source)


def display(value, *, now=None):
    start, end = stamp(value.get('started_at')), stamp(value.get('ended_at'))
    if start is None:
        return '—'
    seconds = max(0, int(((end or now or datetime.now(timezone.utc)) - start).total_seconds()))
    return f'{seconds//3600:02d}:{seconds//60%60:02d}:{seconds%60:02d}'
