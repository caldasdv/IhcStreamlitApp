from datetime import date

from src.services.report_service import build_subject_summary, build_week_summary


SUBJECTS = [{"_id": "ihc", "name": "IHC"}, {"_id": "bd", "name": "Banco de Dados"}]


def test_subject_summary_separates_planned_and_completed_minutes():
    sessions = [
        {"subject_id": "ihc", "study_date": "2026-08-30", "duration": 60, "status": "Concluída"},
        {"subject_id": "ihc", "study_date": "2026-08-31", "duration": 30, "status": "Pendente"},
        {"subject_id": "bd", "study_date": "2026-08-31", "duration": 45, "status": "Pendente"},
    ]

    result = build_subject_summary(sessions, SUBJECTS)

    assert result == [
        {"disciplina": "IHC", "planejados": 90, "concluídos": 60, "pendentes": 1, "atrasadas": 0},
        {"disciplina": "Banco de Dados", "planejados": 45, "concluídos": 0, "pendentes": 1, "atrasadas": 0},
    ]


def test_week_summary_always_has_seven_days_and_marks_overdue():
    sessions = [
        {"study_date": "2026-08-24", "duration": 60, "status": "Concluída", "subject_id": "ihc"},
        {"study_date": "2026-08-25", "duration": 30, "status": "Pendente", "subject_id": "ihc"},
    ]

    result = build_week_summary(sessions, date(2026, 8, 24), today=date(2026, 8, 25))

    assert len(result) == 7
    assert result[0]["concluídos"] == 60
    assert result[1]["pendentes"] == 1
    assert result[6]["data"] == "2026-08-30"
