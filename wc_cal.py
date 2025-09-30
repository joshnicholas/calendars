
from datetime import datetime, timezone

prompts = [
    (1, "MUSTACHE"),
    (2, "WEAVE"),
    (3, "CROWN"),
    (4, "MURKY"),
    (5, "DEER"),
    (6, "PIERCE"),
    (7, "STARFISH"),
    (8, "RECKLESS"),
    (9, "HEAVY"),
    (10, "SWEEP"),
    (11, "STING"),
    (12, "SHREDDED"),
    (13, "DRINK"),
    (14, "TRUNK"),
    (15, "RAGGED"),
    (16, "BLUNDER"),
    (17, "ORNATE"),
    (18, "DEAL"),
    (19, "ARCTIC"),
    (20, "RIVALS"),
    (21, "BLAST"),
    (22, "BUTTON"),
    (23, "FIREFLY"),
    (24, "ROWDY"),
    (25, "INFERNO"),
    (26, "PUZZLING"),
    (27, "ONION"),
    (28, "SKELETAL"),
    (29, "LESSON"),
    (30, "VACANT"),
    (31, "AWARD")
]

def create_ics():
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Word Calendar//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Word Prompts October 2025",
        "X-WR-TIMEZONE:America/New_York"
    ]

    for day, prompt in prompts:
        start_date = f"202510{day:02d}"
        if day < 31:
            end_date = f"202510{day+1:02d}"
        else:
            end_date = "20251101"

        lines.extend([
            "BEGIN:VEVENT",
            f"UID:wc-2025-10-{day:02d}@wordcalendar",
            f"DTSTAMP:{timestamp}",
            f"DTSTART;VALUE=DATE:{start_date}",
            f"DTEND;VALUE=DATE:{end_date}",
            f"SUMMARY:{prompt}",
            "DESCRIPTION:Official Inktober prompts from https://inktober.com/rules",
            "TRANSP:TRANSPARENT",
            "END:VEVENT"
        ])

    lines.append("END:VCALENDAR")

    ics_content = "\r\n".join(lines) + "\r\n"

    with open("out/cals/wc_cal.ics", "w", newline='') as f:
        f.write(ics_content)

    print("Calendar file created: wc_cal.ics")

if __name__ == "__main__":
    create_ics()

