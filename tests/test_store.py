from datetime import datetime, timedelta

from triggermind.models import TriggerRecord
from triggermind.storage.json_store import JSONTriggerStore


def test_add_load_cancel(tmp_path) -> None:
    store = JSONTriggerStore(tmp_path / "triggers.json")
    record = TriggerRecord(
        kind="timer",
        message="Test",
        due_at=datetime.now().astimezone() + timedelta(minutes=5),
    )

    store.add(record)
    loaded = store.load()
    assert len(loaded) == 1
    assert loaded[0].id == record.id

    assert store.cancel(record.id) is True
    loaded_after = store.load()
    assert loaded_after[0].status == "cancelled"
