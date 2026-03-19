#!/usr/bin/env python3
"""
Inject collapsible State/City location links section into all service pages.
Scans for existing location HTML pages and adds organized links before Related Services nav.
"""
import os
import glob
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- Location classifications ---
STATES = {
    "andhra-pradesh": "Andhra Pradesh",
    "arunachal-pradesh": "Arunachal Pradesh",
    "assam": "Assam",
    "bihar": "Bihar",
    "chhattisgarh": "Chhattisgarh",
    "goa": "Goa",
    "gujarat": "Gujarat",
    "haryana": "Haryana",
    "himachal-pradesh": "Himachal Pradesh",
    "jharkhand": "Jharkhand",
    "karnataka": "Karnataka",
    "kerala": "Kerala",
    "madhya-pradesh": "Madhya Pradesh",
    "maharashtra": "Maharashtra",
    "manipur": "Manipur",
    "meghalaya": "Meghalaya",
    "mizoram": "Mizoram",
    "nagaland": "Nagaland",
    "odisha": "Odisha",
    "punjab": "Punjab",
    "rajasthan": "Rajasthan",
    "sikkim": "Sikkim",
    "tamil-nadu": "Tamil Nadu",
    "telangana": "Telangana",
    "tripura": "Tripura",
    "uttar-pradesh": "Uttar Pradesh",
    "uttarakhand": "Uttarakhand",
    "west-bengal": "West Bengal",
}

UTS = {
    "delhi": "Delhi",
    "chandigarh": "Chandigarh",
    "puducherry": "Puducherry",
    "jammu-and-kashmir": "Jammu & Kashmir",
    "ladakh": "Ladakh",
    "andaman-and-nicobar": "Andaman & Nicobar",
    "dadra-nagar-haveli-daman-diu": "Dadra & Nagar Haveli and Daman & Diu",
    "lakshadweep": "Lakshadweep",
}

# All state/UT slugs combined
ALL_REGIONS = set(STATES.keys()) | set(UTS.keys())

# Service slug -> display name
SERVICE_NAMES = {
    "auditors-audit-services": "Audit Services",
    "business-valuation-services": "Business Valuation Services",
    "company-registration": "Company Registration",
    "company-registration-consultant": "Company Registration Consultant",
    "company-secretary-services": "Company Secretary Services",
    "fema-compliance-fdi-advisory": "FEMA Compliance & FDI Advisory",
    "forensic-accounting-fraud-investigation": "Forensic Accounting",
    "gst-services": "GST Services",
    "income-tax-filing-services": "Income Tax Filing Services",
    "private-limited-company-registration": "Pvt Ltd Registration",
    "startup-due-diligence": "Startup Due Diligence",
    "transfer-pricing-services": "Transfer Pricing Services",
}


def slug_to_title(slug):
    """Convert a slug like 'new-delhi' to 'New Delhi'."""
    words = slug.split("-")
    # Handle special abbreviations
    small_words = {"and", "of", "in"}
    result = []
    for i, w in enumerate(words):
        if i > 0 and w in small_words:
            result.append(w)
        else:
            result.append(w.capitalize())
    return " ".join(result)


def find_location_pages(service_slug):
    """Find all -in-{location}.html pages for a service and classify them."""
    pattern = os.path.join(ROOT, f"{service_slug}-in-*.html")
    files = glob.glob(pattern)

    states_found = {}
    uts_found = {}
    cities_found = {}

    for f in files:
        basename = os.path.basename(f).replace(".html", "")
        # Extract location part after service-in-
        prefix = f"{service_slug}-in-"
        location_slug = basename[len(prefix):]

        if location_slug in STATES:
            states_found[location_slug] = STATES[location_slug]
        elif location_slug in UTS:
            uts_found[location_slug] = UTS[location_slug]
        else:
            # It's a city
            cities_found[location_slug] = slug_to_title(location_slug)

    return states_found, uts_found, cities_found


def generate_location_html(service_slug, service_name, states, uts, cities):
    """Generate the collapsible location links HTML section."""
    if not states and not uts and not cities:
        return ""

    lines = []
    lines.append('<section class="location-links-section" aria-label="Service available across India">')
    lines.append(f'<h2>Available Across India</h2>')
    lines.append(f'<p class="location-subtitle">{service_name} in every state and major city. Click to view location-specific details, fees, and regulatory information.</p>')

    # States
    if states:
        lines.append('<details class="location-group" open>')
        lines.append(f'<summary>States ({len(states)})</summary>')
        lines.append('<div class="location-grid">')
        for slug in sorted(states.keys(), key=lambda s: states[s]):
            name = states[slug]
            href = f"/{service_slug}-in-{slug}"
            lines.append(f'<a href="{href}">{name}</a>')
        lines.append('</div>')
        lines.append('</details>')

    # Union Territories
    if uts:
        lines.append('<details class="location-group">')
        lines.append(f'<summary>Union Territories ({len(uts)})</summary>')
        lines.append('<div class="location-grid">')
        for slug in sorted(uts.keys(), key=lambda s: uts[s]):
            name = uts[slug]
            href = f"/{service_slug}-in-{slug}"
            lines.append(f'<a href="{href}">{name}</a>')
        lines.append('</div>')
        lines.append('</details>')

    # Cities
    if cities:
        lines.append('<details class="location-group">')
        lines.append(f'<summary>Cities ({len(cities)})</summary>')
        lines.append('<div class="location-grid">')
        for slug in sorted(cities.keys(), key=lambda s: cities[s]):
            name = cities[slug]
            href = f"/{service_slug}-in-{slug}"
            lines.append(f'<a href="{href}">{name}</a>')
        lines.append('</div>')
        lines.append('</details>')

    lines.append('</section>')
    return "\n".join(lines)


def inject_into_page(html_path, location_html):
    """Inject the location links section into the HTML page before Related Services nav."""
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if already injected
    if 'class="location-links-section"' in content:
        # Remove old injection first
        content = re.sub(
            r'<section class="location-links-section".*?</section>\s*',
            '',
            content,
            flags=re.DOTALL
        )

    # Try to inject before Related Services nav
    marker = '<nav aria-label="Related Services">'
    if marker in content:
        content = content.replace(marker, location_html + "\n" + marker)
    else:
        # Try before closing </article>
        content = content.replace('</article>', location_html + "\n</article>")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    total_injected = 0

    for service_slug, service_name in SERVICE_NAMES.items():
        states, uts, cities = find_location_pages(service_slug)
        total_locations = len(states) + len(uts) + len(cities)

        if total_locations == 0:
            print(f"  SKIP {service_slug}: no location pages found")
            continue

        print(f"  {service_slug}: {len(states)} states, {len(uts)} UTs, {len(cities)} cities = {total_locations} locations")

        location_html = generate_location_html(service_slug, service_name, states, uts, cities)

        # Inject into main service page
        main_page = os.path.join(ROOT, f"{service_slug}.html")
        if os.path.exists(main_page):
            inject_into_page(main_page, location_html)
            total_injected += 1
            print(f"    -> Injected into {service_slug}.html")

        # Also inject into city-level pages (Chennai, Mumbai, Bangalore)
        for city_suffix in ["-chennai", "-mumbai", "-bangalore"]:
            city_page = os.path.join(ROOT, f"{service_slug}{city_suffix}.html")
            if os.path.exists(city_page):
                inject_into_page(city_page, location_html)
                total_injected += 1

        # Inject into all -in-{location}.html pages too
        pattern = os.path.join(ROOT, f"{service_slug}-in-*.html")
        for loc_page in glob.glob(pattern):
            inject_into_page(loc_page, location_html)
            total_injected += 1

    print(f"\nDone. Injected location links into {total_injected} pages.")


if __name__ == "__main__":
    main()
