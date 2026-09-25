import pytest
from fastapi import HTTPException

from app import seed
from app.db import connect
from app.repositories import history, settings_repo
from app.services import estimate_service


@pytest.fixture(autouse=True)
def _db():
    seed.init_db()


def _stored(run_id):
    return next(r for r in history.list_runs(1000) if r["id"] == run_id)["result"]


def test_save_pins_orientation_and_rolls():
    out = estimate_service.run_estimate(1, 1, True, "", "horizontal")
    assert out["orientation"] == "horizontal"
    assert out["drops"] == 6
    assert out["rolls"] == 6
    stored = _stored(out["run_id"])
    assert stored["orientation"] == "horizontal"
    assert stored["rolls"] == 6


def test_default_orientation_change_does_not_rewrite_old_runs():
    settings_repo.set_value("default_orientation", "vertical")
    try:
        old = estimate_service.run_estimate(1, 1, True, "", None)
        assert old["orientation"] == "vertical"

        settings_repo.set_value("default_orientation", "horizontal")
        trial = estimate_service.run_estimate(1, 1, False, "", None)
        assert trial["orientation"] == "horizontal"

        assert _stored(old["run_id"])["orientation"] == "vertical"
    finally:
        settings_repo.set_value("default_orientation", "vertical")


def test_non_positive_roll_size_rejected_without_insert():
    conn = connect()
    try:
        cur = conn.execute(
            "INSERT INTO rolls(name,width,length,pattern_cm,data_quality,note) VALUES (?,?,?,?,?,?)",
            ("clean-zero-width", 0.0, 10.0, 0, "clean", ""),
        )
        conn.commit()
        roll_id = int(cur.lastrowid)
    finally:
        conn.close()

    before = len(history.list_runs(1000))
    with pytest.raises(HTTPException) as exc:
        estimate_service.run_estimate(1, roll_id, True, "", "horizontal")
    assert exc.value.status_code == 422
    assert len(history.list_runs(1000)) == before


def test_invalid_orientation_rejected():
    with pytest.raises(HTTPException) as exc:
        estimate_service.run_estimate(1, 1, False, "", "diagonal")
    assert exc.value.status_code == 422
