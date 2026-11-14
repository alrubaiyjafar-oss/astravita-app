"""
equipment_guide.py - ASTRAVITA medical equipment guide (TEMPORARY VERSION)
-----------------------------------------------------------
Written by the UI team so the interface can work now.
The equipment team can edit the content freely, but please keep:

    get_equipment_list()  -> list of dicts with:
        name, category, purpose, steps (list), safety_notes, metrics (list)

"metrics" links a device to the health metrics it measures,
so the app can suggest it when there is an alert.

Content is a simplified reference for a DEMO. It is NOT an official
procedure. Crews must follow mission procedures and the flight surgeon.
-----------------------------------------------------------
"""


def get_equipment_list():
    """Return the onboard medical equipment (simplified demo content)."""
    return [
        {
            "name": "Pulse Oximeter",
            "category": "Monitoring",
            "purpose": "Measures blood oxygen (SpO2) and heart rate.",
            "steps": [
                "Make sure the finger is clean, warm and without nail polish.",
                "Clip the sensor on the index finger.",
                "Stay still until the reading is stable.",
                "Record the SpO2 and heart rate values in ASTRAVITA.",
            ],
            "safety_notes": "Cold hands or movement can give wrong readings. Repeat if unsure.",
            "metrics": ["spo2", "heart_rate"],
        },
        {
            "name": "Digital Thermometer",
            "category": "Monitoring",
            "purpose": "Measures body temperature.",
            "steps": [
                "Clean the tip with an alcohol wipe.",
                "Turn the device on and wait for the ready signal.",
                "Place it as shown in the device instructions.",
                "Wait for the beep and record the temperature.",
            ],
            "safety_notes": "Clean before and after each use. Do not share without cleaning.",
            "metrics": ["body_temp"],
        },
        {
            "name": "Blood Pressure Monitor",
            "category": "Monitoring",
            "purpose": "Measures blood pressure and pulse.",
            "steps": [
                "Rest calmly for a few minutes before measuring.",
                "Wrap the cuff on the upper arm at heart level.",
                "Press start and keep the arm relaxed and still.",
                "Record the result and repeat once if it looks unusual.",
            ],
            "safety_notes": "A wrong cuff size or position changes the result.",
            "metrics": ["heart_rate"],
        },
        {
            "name": "Activity & Sleep Tracker",
            "category": "Wearables",
            "purpose": "Tracks exercise minutes and sleep duration.",
            "steps": [
                "Wear the tracker on the wrist, snug but comfortable.",
                "Keep it on during exercise and sleep.",
                "Sync it with ASTRAVITA once a day.",
            ],
            "safety_notes": "Charge daily. Remove if the skin becomes irritated.",
            "metrics": ["activity_minutes", "sleep_hours"],
        },
        {
            "name": "Portable Ultrasound",
            "category": "Imaging",
            "purpose": "Basic internal imaging with remote guidance from the ground.",
            "steps": [
                "Contact the ground medical team before starting.",
                "Apply gel and follow the operator instructions step by step.",
                "Save the images and send them to the ground team.",
            ],
            "safety_notes": "Use only with remote guidance from qualified medical staff.",
            "metrics": [],
        },
        {
            "name": "Automated External Defibrillator (AED)",
            "category": "Emergency",
            "purpose": "Emergency device for sudden cardiac arrest.",
            "steps": [
                "Turn the AED on and follow its voice prompts.",
                "Attach the pads as shown on the pictures.",
                "Make sure nobody touches the patient during analysis or shock.",
                "Inform the ground medical team immediately.",
            ],
            "safety_notes": "Emergency use only. Follow the mission emergency procedure.",
            "metrics": [],
        },
    ]