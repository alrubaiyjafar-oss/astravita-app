"""
health_analysis.py - ASTRAVITA health analysis (TEMPORARY VERSION)
-----------------------------------------------------------
Written by the UI team so the interface can work now.
The analysis team can improve the logic freely, but please keep:

    calculate_baseline(df)          -> dict
    detect_alerts(df, baseline)     -> list of dicts

All thresholds here are simple statistical rules for a DEMO with
SIMULATED data. They are NOT medical criteria.
-----------------------------------------------------------
"""

# Metrics we analyse, with a readable name and unit
METRIC_INFO = {
    "heart_rate":       ("Heart rate", "bpm"),
    "sleep_hours":      ("Sleep", "h"),
    "activity_minutes": ("Activity", "min"),
    "spo2":             ("Blood oxygen", "%"),
    "body_temp":        ("Body temperature", "°C"),
}

RECENT_DAYS = 7      # the last 7 days are checked for alerts
WARNING_Z = 2.0      # 2 standard deviations away  -> warning
CRITICAL_Z = 3.0     # 3 standard deviations away  -> critical


def calculate_baseline(df):
    """
    Personal baseline = the astronaut's own normal values,
    measured on the days BEFORE the recent window.

    Returns: {metric: {"mean", "std", "low", "high"}}
    """
    history = df.iloc[:-RECENT_DAYS] if len(df) > RECENT_DAYS else df
    baseline = {}
    for metric in METRIC_INFO:
        mean = float(history[metric].mean())
        std = float(history[metric].std())
        if std == 0:
            std = 0.01   # avoid division by zero
        baseline[metric] = {
            "mean": round(mean, 2),
            "std": round(std, 2),
            "low": round(mean - WARNING_Z * std, 2),
            "high": round(mean + WARNING_Z * std, 2),
        }
    return baseline


def detect_alerts(df, baseline):
    """
    Check the last RECENT_DAYS days against the personal baseline.

    A metric creates an alert when:
      - today is 3+ std away from normal         -> "critical"
      - 2 of the last 3 days are 2+ std away      -> "warning"

    Returns a list of dicts:
      date, metric, value, severity, message, explanation, baseline_mean
    """
    recent = df.iloc[-RECENT_DAYS:]
    alerts = []

    for metric, (name, unit) in METRIC_INFO.items():
        mean = baseline[metric]["mean"]
        std = baseline[metric]["std"]

        z_scores = (recent[metric] - mean) / std
        last3 = z_scores.iloc[-3:]
        days_out = int((last3.abs() >= WARNING_Z).sum())

        today_value = float(recent[metric].iloc[-1])
        today_z = float(z_scores.iloc[-1])

        if abs(today_z) >= CRITICAL_Z:
            severity = "critical"
        elif days_out >= 2:
            severity = "warning"
        else:
            continue  # normal -> no alert

        direction = "above" if today_z > 0 else "below"
        diff = abs(today_value - mean)

        message = f"{name} is {direction} personal baseline"
        explanation = (
            f"Today's {name.lower()} is {today_value:g} {unit}. "
            f"This astronaut's normal value is {mean:g} {unit} "
            f"(usual range {baseline[metric]['low']:g}-{baseline[metric]['high']:g} {unit}). "
            f"Today is {diff:.1f} {unit} {direction} normal, which is "
            f"{abs(today_z):.1f} standard deviations away. "
            f"{days_out} of the last 3 days were outside the usual range."
        )

        alerts.append({
            "date": recent["date"].iloc[-1],
            "metric": metric,
            "value": today_value,
            "severity": severity,
            "message": message,
            "explanation": explanation,
            "baseline_mean": mean,
        })

    # Critical alerts first
    alerts.sort(key=lambda a: 0 if a["severity"] == "critical" else 1)
    return alerts