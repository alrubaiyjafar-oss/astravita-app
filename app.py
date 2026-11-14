"""
ASTRAVITA - Astronaut Health Monitoring Platform
Main interface file (UI). Run with:  streamlit run app.py
"""

from pathlib import Path

import plotly.express as px
import streamlit as st

import data  # team file: get_astronauts(), get_health_data()
import ui_theme  # UI file: colors, logo, styles
import health_analysis  # team file: calculate_baseline(), detect_alerts()
import equipment_guide  # team file: get_equipment_list()
# 1) Page settings (must be the first Streamlit command)
st.set_page_config(
    page_title="ASTRAVITA",
    page_icon="images/logo_mark.png",
    layout="wide",
)
ui_theme.apply_theme()

# 2) List of the program's sections (pages)
PAGES = [
    "Dashboard",
    "Astronaut Profile",
    "Health Alerts",
    "Equipment Guide",
    "Health Reports",
]

# 3) How each health metric is displayed
METRICS = {
    "heart_rate":       {"label": "Heart Rate",   "unit": "bpm", "higher_is_bad": True,  "small_change": 3},
    "sleep_hours":      {"label": "Sleep",        "unit": "h",   "higher_is_bad": False, "small_change": 0.5},
    "activity_minutes": {"label": "Activity",     "unit": "min", "higher_is_bad": False, "small_change": 15},
    "spo2":             {"label": "Blood Oxygen", "unit": "%",   "higher_is_bad": False, "small_change": 1},
    "body_temp":        {"label": "Body Temp",    "unit": "°C",  "higher_is_bad": True,  "small_change": 0.3},
}

BLUE = ui_theme.BRIGHT_BLUE
GREY = "#8A94A6"


# 4) Helper functions for the UI
def show_avatar(astronaut, size=140):
    """Show the astronaut's photo. If there is no photo file, show initials."""
    photo = astronaut.get("photo")
    if photo and Path(photo).exists():
        st.image(photo, width=size)
    else:
        initials = "".join(part[0] for part in astronaut["name"].split()[:2])
        st.markdown(
            f'<div class="astra-avatar" style="width:{size}px; height:{size}px; '
            f'font-size:{size // 3}px;">{initials}</div>',
            unsafe_allow_html=True,
        )


def page_header(title, subtitle):
    st.title(title)
    st.caption(subtitle)
    st.divider()


def show_metric_cards(df):
    """Show one card per metric: today's value and change vs. average."""
    today = df.iloc[-1]
    history = df.iloc[:-1]

    columns = st.columns(len(METRICS))
    for col, (key, info) in zip(columns, METRICS.items()):
        value = today[key]
        change = value - history[key].mean()

        if abs(change) < info["small_change"]:
            color = "off"
        elif info["higher_is_bad"]:
            color = "inverse"
        else:
            color = "normal"

        col.metric(
            label=info["label"],
            value=f"{value:g} {info['unit']}",
            delta=f"{change:+.1f} vs avg",
            delta_color=color,
        )


def trend_chart(df, key):
    """Line chart of one metric with a dashed average line."""
    info = METRICS[key]
    fig = px.line(df, x="date", y=key, markers=True)
    fig.update_traces(line_color=BLUE, line_width=2, marker_size=5)
    fig.add_hline(
        y=df[key].mean(),
        line_dash="dash",
        line_color=GREY,
        annotation_text="30-day average",
        annotation_font_color=GREY,
    )
    fig.update_layout(
        title=f"{info['label']} ({info['unit']})",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis_title=None,
        yaxis_title=None,
    )
    st.plotly_chart(fig)


# 5) Top navigation bar (logo + pages + astronaut selector)
astronauts = data.get_astronauts()
names = [a["name"] for a in astronauts]

with st.container(key="topbar"):
    brand_col, menu_col, astro_col = st.columns([2.3, 5.2, 1.9], vertical_alignment="center")
    with brand_col:
        ui_theme.brand()
    with menu_col:
        page = st.segmented_control(
            "Navigation", PAGES, default="Dashboard", label_visibility="collapsed"
        )
    with astro_col:
        chosen_name = st.selectbox("Astronaut", names, label_visibility="collapsed")

page = page or "Dashboard"

astronaut = next(a for a in astronauts if a["name"] == chosen_name)
health_df = data.get_health_data(astronaut["id"])
baseline = health_analysis.calculate_baseline(health_df)
alerts = health_analysis.detect_alerts(health_df, baseline)


# 6) Show the selected page
if page == "Dashboard":
    page_header("Mission Health Dashboard", "Overview of crew health status")

    pic, info = st.columns([1, 6])
    with pic:
        show_avatar(astronaut, size=90)
    with info:
        st.markdown(f"### {astronaut['name']}")
        st.caption(f"{astronaut['role']}  |  {astronaut['mission']}  |  "
                   f"Mission day {astronaut['mission_day']}")

    st.subheader("Today's vital signs")
    show_metric_cards(health_df)
    st.caption("Change is compared with this astronaut's own average "
               "over the previous days. Grey = small, normal change. "
               "Simulated data.")

    st.subheader("Mission trends")
    trend_chart(health_df, "heart_rate")
    col1, col2 = st.columns(2)
    with col1:
        trend_chart(health_df, "sleep_hours")
    with col2:
        trend_chart(health_df, "activity_minutes")

elif page == "Astronaut Profile":
    page_header("Astronaut Profile", "Personal information and health baseline")

    left, right = st.columns([1, 2])
    with left:
        with st.container(border=True):
            show_avatar(astronaut, size=160)
            st.markdown(f"### {astronaut['name']}")
            st.write(f"**ID:** {astronaut['id']}")
            st.write(f"**Role:** {astronaut['role']}")
            st.write(f"**Age:** {astronaut['age']}")
            st.write(f"**Mission:** {astronaut['mission']}")
            st.write(f"**Mission day:** {astronaut['mission_day']}")
    with right:
        with st.container(border=True):
            st.markdown("### Personal Health Baseline")
            st.caption("This astronaut's own normal values, measured on "
                       "earlier mission days. Simulated data.")
            rows = []
            for key, b in baseline.items():
                info = METRICS[key]
                rows.append({
                    "Metric": info["label"],
                    "Normal (average)": f"{b['mean']:g} {info['unit']}",
                    "Usual range": f"{b['low']:g} - {b['high']:g} {info['unit']}",
                })
            st.dataframe(rows, hide_index=True)

elif page == "Health Alerts":
    page_header("Health Alerts", "Explainable alerts based on personal baseline")

    critical = [a for a in alerts if a["severity"] == "critical"]
    warnings = [a for a in alerts if a["severity"] == "warning"]

    c1, c2, c3 = st.columns(3)
    c1.metric("Critical alerts", len(critical))
    c2.metric("Warnings", len(warnings))
    c3.metric("Metrics checked", len(health_analysis.METRIC_INFO))

    if not alerts:
        st.success(f"All clear: {astronaut['name']}'s readings are inside "
                   "the personal baseline.", icon=":material/check_circle:")

    for alert in alerts:
        info = METRICS[alert["metric"]]
        show_box = st.error if alert["severity"] == "critical" else st.warning
        show_box(
            f"**{alert['severity'].upper()}: {alert['message']}**  \n"
            f"Today: {alert['value']:g} {info['unit']}  |  "
            f"Personal normal: {alert['baseline_mean']:g} {info['unit']}",
            icon=":material/warning:",
        )
        with st.expander("Why this alert?"):
            st.write(alert["explanation"])
            b = baseline[alert["metric"]]
            fig = px.line(health_df, x="date", y=alert["metric"], markers=True)
            fig.update_traces(line_color=BLUE, line_width=2, marker_size=5)
            fig.add_hrect(y0=b["low"], y1=b["high"], fillcolor=BLUE,
                          opacity=0.12, line_width=0,
                          annotation_text="Usual range",
                          annotation_font_color=GREY)
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=260,
                margin=dict(l=10, r=10, t=30, b=10),
                xaxis_title=None,
                yaxis_title=None,
            )
            st.plotly_chart(fig)

    st.caption("Alerts use simple statistical rules on SIMULATED data. "
               "They are not medical advice.")

elif page == "Equipment Guide":
    page_header("Medical Equipment Guide", "How to use onboard medical equipment")

    equipment = equipment_guide.get_equipment_list()
    alert_metrics = {a["metric"] for a in alerts}

    search_col, cat_col = st.columns([2, 1])
    with search_col:
        query = st.text_input("Search", placeholder="Try: oxygen, sleep, emergency")
    with cat_col:
        categories = ["All"] + sorted({e["category"] for e in equipment})
        category = st.selectbox("Category", categories)

    shown = [
        e for e in equipment
        if (category == "All" or e["category"] == category)
        and query.lower() in (e["name"] + " " + e["purpose"]).lower()
    ]

    if not shown:
        st.info("No equipment matches your search.")

    cols = st.columns(2)
    for i, item in enumerate(shown):
        with cols[i % 2]:
            with st.container(border=True):
                st.markdown(f"#### {item['name']}")
                if alert_metrics & set(item["metrics"]):
                    st.markdown(":orange-badge[Suggested for a current alert]")
                st.caption(f"{item['category']}  |  {item['purpose']}")
                with st.expander("How to use"):
                    for n, step in enumerate(item["steps"], start=1):
                        st.write(f"{n}. {step}")
                st.caption(f"Safety: {item['safety_notes']}")
    st.caption("Simplified reference for demonstration. Always follow official "
               "mission procedures and the flight surgeon's instructions.")
elif page == "Health Reports":
    page_header("Health Reports", "Generate and download health reports")

    first_day = health_df["date"].iloc[0].strftime("%Y-%m-%d")
    last_day = health_df["date"].iloc[-1].strftime("%Y-%m-%d")
    status = "Needs attention" if alerts else "Stable"

    c1, c2, c3 = st.columns(3)
    c1.metric("Astronaut", astronaut["name"])
    c2.metric("Period", f"{len(health_df)} days")
    c3.metric("Status", status)

    # Table of the report (one row per metric)
    rows = []
    for key, info in METRICS.items():
        b = baseline[key]
        rows.append({
            "Metric": info["label"],
            "Today": f"{health_df[key].iloc[-1]:g} {info['unit']}",
            "Personal normal": f"{b['mean']:g} {info['unit']}",
            "Usual range": f"{b['low']:g} - {b['high']:g}",
        })
    st.subheader("Report preview")
    st.dataframe(rows, hide_index=True)

    if alerts:
        for alert in alerts:
            st.write(f"- **{alert['severity'].upper()}**: {alert['explanation']}")
    else:
        st.write("No active alerts. All readings are inside the personal baseline.")

    # Build a simple printable HTML report
    table_rows = "".join(
        f"<tr><td>{r['Metric']}</td><td>{r['Today']}</td>"
        f"<td>{r['Personal normal']}</td><td>{r['Usual range']}</td></tr>"
        for r in rows
    )
    alert_items = "".join(
        f"<li><b>{a['severity'].upper()}</b>: {a['explanation']}</li>" for a in alerts
    ) or "<li>No active alerts.</li>"
    report_html = f"""<html><head><meta charset="utf-8"><title>ASTRAVITA report</title>
<style>body{{font-family:Arial,sans-serif;margin:40px;color:#111}}
table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ccc;padding:8px;text-align:left}}
th{{background:#f0f3f8}}.note{{color:#666;font-size:12px}}</style></head><body>
<h1>ASTRAVITA Health Report</h1>
<p><b>Astronaut:</b> {astronaut['name']} ({astronaut['id']}) - {astronaut['role']}<br>
<b>Mission:</b> {astronaut['mission']} - day {astronaut['mission_day']}<br>
<b>Period:</b> {first_day} to {last_day}<br><b>Status:</b> {status}</p>
<h2>Vital signs</h2><table><tr><th>Metric</th><th>Today</th>
<th>Personal normal</th><th>Usual range</th></tr>{table_rows}</table>
<h2>Alerts</h2><ul>{alert_items}</ul>
<p class="note">SIMULATED DATA - for demonstration only. Not medical advice.
ASTRAVITA SpaceLab | NASA Space Apps Challenge 2026</p></body></html>"""

    file_name = f"ASTRAVITA_{astronaut['id']}_{last_day}"
    d1, d2 = st.columns(2)
    with d1:
        st.download_button("Download report (HTML)", report_html,
                           file_name=file_name + ".html", mime="text/html",
                           type="primary", icon=":material/description:")
    with d2:
        st.download_button("Download data (CSV)", health_df.to_csv(index=False),
                           file_name=file_name + ".csv", mime="text/csv",
                           icon=":material/table:")
    st.caption("Tip: open the HTML report in the browser and press Ctrl + P "
               "to save it as PDF.")

# 7) Footer (shown on every page)
st.divider()
st.caption("SIMULATED DATA - for demonstration only  |  "
           "ASTRAVITA SpaceLab  |  NASA Space Apps Challenge 2026")