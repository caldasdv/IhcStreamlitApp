"""Agenda visual experimental baseada em Custom Component v2."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import date, timedelta
from typing import Any

import streamlit as st

from src.domain.session_rules import effective_status


_AGENDA = st.components.v2.component(
    "study_agenda",
    html='''<div class="agenda" id="agenda-root" role="list" aria-label="Agenda semanal"></div>''',
    css='''
    .agenda { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: .5rem; }
    .day { min-height: 8rem; padding: .7rem; border: 1px solid var(--st-border-color); border-radius: var(--st-base-radius); background: var(--st-secondary-background-color); }
    .day h3 { margin: 0 0 .7rem; color: var(--st-heading-color); font: 600 .85rem var(--st-heading-font); }
    .empty { color: var(--st-gray-text-color); font: .8rem var(--st-font); }
    .session { display: block; width: 100%; margin: .35rem 0; padding: .55rem; border: 1px solid var(--st-widget-border-color); border-radius: var(--st-button-radius); background: var(--st-background-color); color: var(--st-text-color); text-align: left; cursor: pointer; }
    .session:hover, .session:focus-visible { border-color: var(--st-primary-color); }
    .session:focus-visible { outline: 3px solid var(--st-primary-color); outline-offset: 2px; }
    .session strong, .session span { display: block; }
    .session strong { font: 600 .8rem var(--st-font); }
    .session span { margin-top: .2rem; font: .75rem var(--st-font); }
    @media (max-width: 900px) { .agenda { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
    @media (max-width: 600px) { .agenda { grid-template-columns: 1fr; } .day { min-height: auto; } }
    ''',
    js='''
    export default function (component) {
      const { data, parentElement, setTriggerValue } = component
      const root = parentElement.querySelector("#agenda-root")
      if (!root) return
      root.replaceChildren()
      for (const day of (data?.days ?? [])) {
        const section = document.createElement("section")
        section.className = "day"
        section.setAttribute("role", "listitem")
        const heading = document.createElement("h3")
        heading.textContent = day.label
        section.appendChild(heading)
        if (!day.sessions.length) {
          const empty = document.createElement("p")
          empty.className = "empty"
          empty.textContent = "Sem sessões"
          section.appendChild(empty)
        }
        for (const session of day.sessions) {
          const button = document.createElement("button")
          button.className = "session"
          button.type = "button"
          button.setAttribute("aria-label", `${session.time}, ${session.topic}, ${session.status}`)
          const time = document.createElement("strong")
          time.textContent = session.time
          const topic = document.createElement("span")
          topic.textContent = `${session.topic} · ${session.duration} min`
          const status = document.createElement("span")
          status.textContent = session.status
          button.append(time, topic, status)
          button.onclick = () => setTriggerValue("selected", session.id)
          section.appendChild(button)
        }
        root.appendChild(section)
      }
    }
    ''',
)


def render_study_agenda(
    sessions: Iterable[dict[str, Any]], week_start: date, *, key: str
) -> str | None:
    """Renderiza a agenda e retorna o ID selecionado nesta execução."""
    sessions_by_date: dict[str, list[dict[str, str]]] = {}
    for session in sessions:
        sessions_by_date.setdefault(session["study_date"], []).append(
            {
                "id": str(session["_id"]),
                "time": str(session["study_time"]),
                "topic": str(session["topic"]),
                "duration": str(session["duration"]),
                "status": effective_status(session),
            }
        )
    weekdays = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    days = [
        {
            "label": f"{weekday} {(week_start + timedelta(days=offset)):%d/%m/%Y}",
            "date": (week_start + timedelta(days=offset)).isoformat(),
            "sessions": sessions_by_date.get((week_start + timedelta(days=offset)).isoformat(), []),
        }
        for offset, weekday in enumerate(weekdays)
    ]
    result = _AGENDA(key=key, data={"days": days}, on_selected_change=lambda: None)
    return getattr(result, "selected", None)
