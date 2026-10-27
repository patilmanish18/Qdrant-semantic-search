
import csv
from pathlib import Path

OUTPUT_FILE = Path("data/products.csv")

# Fictional product catalog for semantic-search development.
# These are synthetic listings, not verified commercial products.

CATALOG = {
    "Laptops": [
        ("AeroBook Pro 14", "Lightweight developer laptop with 16 GB memory and a sharp display, designed for Python programming and everyday software development."),
        ("CodeStation 16", "Performance-focused laptop with a large screen and ample memory for running IDEs, containers, and multiple development tools."),
        ("CampusMate Air", "Affordable student laptop for online lectures, assignments, web browsing, and working on documents between classes."),
        ("PixelCraft Studio", "Creative workstation laptop suited to photo editing, graphic design, visual content creation, and color-focused workflows."),
        ("NomadBook 13", "Compact travel laptop with a lightweight chassis for remote workers who frequently commute or work from different locations."),
        ("LedgerBook Business", "Professional laptop for spreadsheets, business applications, email, video calls, and office productivity."),
        ("RenderCore X15", "High-performance notebook intended for demanding graphics applications, 3D design, and intensive computing tasks."),
        ("EverydayBook 15", "General-purpose laptop for browsing, streaming, document editing, online shopping, and household computing."),
    ],
    "Phones": [
        ("LumaCam Pro", "Camera-focused smartphone for taking detailed photographs, recording travel videos, and capturing portraits for social media."),
        ("WorkLink One", "Business smartphone for professional email, calendar management, secure work applications, messaging, and conference calls."),
        ("PocketLite A5", "Budget-friendly phone for everyday calls, messaging, navigation, and commonly used mobile applications."),
        ("GamePulse X", "Gaming-oriented smartphone designed for responsive controls, extended gaming sessions, and smooth mobile entertainment."),
        ("TrailFinder S", "Travel smartphone for using maps, translating text, checking bookings, and documenting journeys with photographs."),
        ("ClearCall Max", "Communication-focused phone for frequent callers who need clear voice conversations, messaging, and reliable everyday usability."),
        ("ViewStream Plus", "Entertainment smartphone for watching films, streaming video, browsing social media, and reading digital content."),
        ("FamilyConnect M", "Easy-to-use smartphone for family communication, video calling, sharing photos, and managing daily reminders."),
    ],
    "Office Furniture": [
        ("FlexiSeat Ergo Mesh", "Breathable mesh office chair with adjustable lumbar support and armrests for people working long hours at a desk."),
        ("ExecutiveForm Leatherette", "Padded executive chair for a home office, management workspace, or professional desk setup."),
        ("StandWell Electric Desk", "Height-adjustable standing desk for alternating between seated and standing work throughout the day."),
        ("CompactCorner Study Desk", "Space-saving desk with a practical work surface for a small bedroom, student study area, or compact home office."),
        ("PosturePlus Task Chair", "Adjustable task chair with a supportive backrest for focused computer work, reading, and daily desk activities."),
        ("StudioLift Monitor Riser", "Monitor stand that raises a screen to help organize a workstation and create additional space underneath."),
        ("Oakline Writing Desk", "Minimal wooden writing desk for journaling, studying, laptop work, and a tidy home workspace."),
        ("MeetingPoint Conference Table", "Large meeting table for collaborative discussions, team planning, presentations, and shared office work."),
    ],
    "Audio": [
        ("QuietSphere ANC", "Wireless noise-cancelling headphones for concentrating in busy offices, travelling on trains, and attending online meetings."),
        ("ClearVoice Meeting Headset", "Work headset with a boom microphone for video conferences, remote customer support, and frequent professional calls."),
        ("RoamBeat Mini", "Compact portable Bluetooth speaker for listening to music in a bedroom, picnic area, or small gathering."),
        ("StudioTone Reference", "Over-ear headphones intended for audio monitoring, music production, mixing, and detailed listening."),
        ("GameArena Surround", "Gaming headset with a microphone for multiplayer communication, team coordination, and immersive gameplay."),
        ("OpenAir Run Buds", "Lightweight wireless earbuds for workouts, walking, commuting, and listening to audio on the move."),
        ("BassTrail Portable", "Portable wireless speaker designed for energetic music playback during outdoor activities and casual gatherings."),
        ("PodCast USB Mic", "USB microphone for recording podcasts, voiceovers, online lessons, streaming, and remote presentations."),
    ],
    "Accessories": [
        ("TypeCraft Mechanical Keyboard", "Mechanical keyboard for programmers and writers who want tactile feedback during extended typing sessions."),
        ("SwiftGlide Wireless Mouse", "Wireless computer mouse for navigating spreadsheets, browser tabs, documents, and everyday desktop applications."),
        ("ConnectPro USB-C Hub", "USB-C hub for connecting laptop accessories such as USB devices, external displays, and compatible peripherals."),
        ("TransitGuard Laptop Backpack", "Padded laptop backpack with compartments for chargers, notebooks, and accessories during daily commuting."),
        ("RapidVault Portable SSD", "Portable solid-state drive for backing up project files, transferring large datasets, and carrying work between computers."),
        ("ErgoRise Laptop Stand", "Adjustable laptop stand that elevates a notebook for a more organized desk setup and improved screen positioning."),
        ("PrecisionPad XL", "Large desk mat for smooth mouse movement and a consistent surface for keyboard and mouse use."),
        ("PowerDock 100", "Multiport charging station for powering compatible phones, tablets, and other personal electronic devices."),
    ],
}

# Five distinct buyer needs per product create 200 unique listings.
# Each listing keeps a meaningful product identity and use-case description.
VARIANTS = [
    (
        "Home Office Edition",
        "A practical choice for a dedicated home workspace and everyday productivity.",
    ),
    (
        "Travel Edition",
        "Designed for people who work, study, or stay productive while travelling.",
    ),
    (
        "Professional Edition",
        "Suited to demanding workdays, professional tasks, and organized workflows.",
    ),
    (
        "Compact Workspace Edition",
        "A useful option for smaller rooms, limited desk space, or minimalist setups.",
    ),
    (
        "Everyday Essentials Edition",
        "A versatile option for regular daily use, convenience, and general productivity.",
    ),
]

def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    product_id = 1

    for category, products in CATALOG.items():
        for base_name, base_description in products:
            for variant_name, use_case in VARIANTS:
                rows.append({
                    "id": product_id,
                    "name": f"{base_name} - {variant_name}",
                    "category": category,
                    "description": f"{base_description} {use_case}",
                })
                product_id += 1

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["id", "name", "category", "description"],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} product listings: {OUTPUT_FILE}")
    print(f"Unique names: {len({r['name'] for r in rows})}")
    print(f"Unique descriptions: {len({r['description'] for r in rows})}")
    print("\nProducts per category:")

    for category in CATALOG:
        count = sum(r["category"] == category for r in rows)
        print(f"  {category}: {count}")

if __name__ == "__main__":
    main()
