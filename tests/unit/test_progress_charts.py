from src.ui.components.progress_charts import subject_progress_figure, weekly_progress_figure


def test_subject_progress_figure_contains_minutes_series():
    figure = subject_progress_figure(
        [{"disciplina": "IHC", "planejados": 90, "concluídos": 60}]
    )

    assert [trace.name for trace in figure.data] == ["Planejados", "Concluídos"]
    assert figure.data[0].x == (90,)
    assert figure.layout.xaxis.title.text == "Minutos"


def test_weekly_progress_figure_contains_daily_series():
    figure = weekly_progress_figure(
        [{"dia": "segunda 24/08", "planejados": 60, "concluídos": 30}]
    )

    assert len(figure.data) == 2
    assert figure.data[1].y == (30,)
    assert figure.layout.yaxis.title.text == "Minutos"
