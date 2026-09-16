"""Grade semanal visual de aulas com ações rápidas."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from datetime import time
import re
from typing import Any

import streamlit as st


_TIMETABLE = st.components.v2.component(
    "class_timetable",
    html='''<p class="timetable-hint">Deslize para ver a semana completa.</p><div class="timetable-scroll"><div class="timetable" id="timetable-root" role="list" aria-label="Grade semanal de aulas"></div></div>''',
    css='''
    .timetable-hint { display: none; margin: 0 0 .5rem; color: var(--st-gray-text-color); font: .8rem var(--st-font); }
    .timetable-scroll { max-width: 100%; overflow-x: auto; padding: .15rem .15rem .75rem; scrollbar-color: var(--st-primary-color) var(--st-secondary-background-color); scrollbar-width: thin; }
    .timetable { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: .8rem; min-width: 0; }
    .day { min-height: 14rem; padding: .85rem; border: 1px solid var(--st-border-color); border-radius: var(--st-base-radius); background: var(--st-secondary-background-color); }
    .day h3 { margin: 0 0 .7rem; padding-bottom: .6rem; border-bottom: 1px solid var(--st-border-color); color: var(--st-heading-color); font: 600 .85rem var(--st-heading-font); letter-spacing: .04em; text-transform: uppercase; }
    .empty { margin-top: 2.6rem; color: var(--st-gray-text-color); font: .75rem var(--st-font); text-align: center; }
    .meeting { position: relative; margin: .3rem 0; padding: .55rem 3.5rem .55rem .55rem; border: 1px solid var(--st-widget-border-color); border-left: 3px solid var(--meeting-color, var(--st-primary-color)); border-radius: var(--st-button-radius); background: var(--st-background-color); color: var(--st-text-color); }
    .meeting strong, .meeting span { display: block; }
    .meeting strong { font: 600 .78rem var(--st-font); }
    .meeting span { margin-top: .2rem; font: .75rem var(--st-font); line-height: 1.2; }
    .meeting-location { color: var(--st-gray-text-color); font-size: .68rem !important; }
    .meeting-actions { position: absolute; top: .3rem; right: .25rem; display: flex; gap: .1rem; }
    .action { width: 1.55rem; min-height: 1.55rem; padding: 0; border: 0; border-radius: var(--st-button-radius); background: transparent; color: var(--st-gray-text-color); font: .72rem var(--st-font); cursor: pointer; }
    .action:hover, .action:focus-visible { background: var(--st-secondary-background-color); color: var(--st-primary-color); }
    .action:focus-visible, .confirm button:focus-visible { outline: 3px solid var(--st-primary-color); outline-offset: 2px; }
    .confirm { display: flex; align-items: center; gap: .3rem; margin-top: .45rem; padding-top: .45rem; border-top: 1px solid var(--st-border-color); }
    .confirm span { flex: 1; margin: 0; color: var(--st-gray-text-color); font-size: .68rem; }
    .confirm button { min-height: 1.7rem; padding: .2rem .35rem; border: 1px solid var(--st-widget-border-color); border-radius: var(--st-button-radius); background: var(--st-background-color); color: var(--st-text-color); font: 600 .65rem var(--st-font); cursor: pointer; }
    .confirm .confirm-delete { border-color: var(--st-primary-color); background: var(--st-primary-color); color: white; }
    @media (max-width: 768px) { .timetable-hint { display: block; } .timetable-scroll { -webkit-overflow-scrolling: touch; } .timetable { grid-template-columns: repeat(7, minmax(130px, 1fr)); min-width: 950px; } }
    ''',
    js='''
    export default function (component) {
      const { data, parentElement, setTriggerValue } = component
      const root = parentElement.querySelector("#timetable-root")
      if (!root) return
      root.replaceChildren()
      for (const day of (data?.days ?? [])) {
        const section = document.createElement("section")
        section.className = "day"
        section.setAttribute("role", "listitem")
        const heading = document.createElement("h3")
        heading.textContent = day.label
        section.appendChild(heading)
        if (!day.meetings.length) {
          const empty = document.createElement("p")
          empty.className = "empty"
          empty.textContent = "Livre"
          section.appendChild(empty)
        }
        for (const meeting of day.meetings) {
          const card = document.createElement("article")
          card.className = "meeting"
          if (meeting.color) card.style.setProperty("--meeting-color", meeting.color)
          const time = document.createElement("strong")
          time.textContent = `${meeting.start}–${meeting.end}`
          const subject = document.createElement("span")
          subject.textContent = meeting.subject
          card.append(time, subject)
          if (meeting.location) {
            const location = document.createElement("span")
            location.className = "meeting-location"
            location.textContent = meeting.location
            card.appendChild(location)
          }
          const actions = document.createElement("div")
          actions.className = "meeting-actions"
          const editButton = document.createElement("button")
          editButton.className = "action"
          editButton.type = "button"
          editButton.title = "Editar horário"
          editButton.setAttribute("aria-label", `Editar ${meeting.subject}`)
          editButton.textContent = "✎"
          editButton.onclick = () => setTriggerValue("edited", meeting.id)
          const deleteButton = document.createElement("button")
          deleteButton.className = "action"
          deleteButton.type = "button"
          deleteButton.title = "Remover horário"
          deleteButton.setAttribute("aria-label", `Remover ${meeting.subject}`)
          deleteButton.textContent = "🗑"
          deleteButton.onclick = () => {
            deleteButton.remove()
            const confirmation = document.createElement("div")
            confirmation.className = "confirm"
            const message = document.createElement("span")
            message.textContent = "Remover este horário?"
            const cancel = document.createElement("button")
            cancel.type = "button"
            cancel.textContent = "Cancelar"
            cancel.onclick = () => { confirmation.remove(); card.appendChild(deleteButton) }
            const confirm = document.createElement("button")
            confirm.className = "confirm-delete"
            confirm.type = "button"
            confirm.textContent = "Remover"
            confirm.onclick = () => setTriggerValue("deleted", meeting.id)
            confirmation.append(message, cancel, confirm)
            card.appendChild(confirmation)
          }
          actions.append(editButton, deleteButton)
          card.appendChild(actions)
          section.appendChild(card)
        }
        root.appendChild(section)
      }
    }
    ''',
)


def _safe_color(value: Any) -> str:
    return (
        value
        if isinstance(value, str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", value)
        else "#176B5D"
    )


def render_class_timetable(
    meetings: Iterable[dict[str, Any]], weekdays: Sequence[str], *, key: str
) -> tuple[str | None, str | None]:
    """Renderiza a grade e retorna IDs de aula removida e editada."""
    meetings_by_day: dict[int, list[dict[str, str]]] = {
        weekday: [] for weekday in range(len(weekdays))
    }
    for meeting in meetings:
        start = time.fromisoformat(str(meeting["start_time"]))
        end = time.fromisoformat(str(meeting["end_time"]))
        meetings_by_day[meeting["weekday"]].append(
            {
                "id": str(meeting["_id"]),
                "start": start.strftime("%H:%M"),
                "end": end.strftime("%H:%M"),
                "subject": str(meeting["subject_name"]),
                "location": str(meeting.get("location", "")),
                "color": _safe_color(meeting.get("subject_color")),
            }
        )
    days = [
        {"label": weekday_name[:3], "meetings": meetings_by_day[weekday]}
        for weekday, weekday_name in enumerate(weekdays)
    ]
    result = _TIMETABLE(
        key=key,
        data={"days": days},
        on_deleted_change=lambda: None,
        on_edited_change=lambda: None,
    )
    return getattr(result, "deleted", None), getattr(result, "edited", None)


def render_class_timetable_fallback(
    meetings: Iterable[dict[str, Any]], weekdays: Sequence[str]
) -> None:
    """Oferece uma leitura textual nativa quando o componente visual não é suportado."""
    meetings = list(meetings)
    with st.expander("Ver lista textual da grade", expanded=False):
        for weekday, weekday_name in enumerate(weekdays):
            day_meetings = [meeting for meeting in meetings if meeting["weekday"] == weekday]
            st.markdown(f"**{weekday_name}**")
            if not day_meetings:
                st.caption("Livre")
                continue
            for meeting in day_meetings:
                location = f" · {meeting['location']}" if meeting.get("location") else ""
                st.caption(
                    f"{meeting['start_time']}–{meeting['end_time']} · "
                    f"{meeting['subject_name']}{location}"
                )
