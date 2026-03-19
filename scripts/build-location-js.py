#!/usr/bin/env python3
"""
build-location-js.py
Scans location HTML files per service, classifies them as state/UT/city,
and generates js/location-links.js with embedded data.
Also generates a shell script to inject the <script> tag into all HTML files.
"""

import os, glob, json, re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS_DIR = os.path.join(BASE_DIR, "js")
os.makedirs(JS_DIR, exist_ok=True)

SERVICES = [
    "auditors-audit-services",
    "business-valuation-services",
    "company-registration",
    "company-registration-consultant",
    "company-secretary-services",
    "fema-compliance-fdi-advisory",
    "forensic-accounting-fraud-investigation",
    "gst-services",
    "income-tax-filing-services",
    "private-limited-company-registration",
    "startup-due-diligence",
    "transfer-pricing-services",
]

# Friendly display names for each service (used in subtitle)
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
    "dadra-nagar-haveli-daman-diu": "Dadra Nagar Haveli & Daman Diu",
    "lakshadweep": "Lakshadweep",
}

# Slug-to-display for cities (auto-generated from slug)
def slug_to_name(slug):
    """Convert a slug like 'anna-salai-chennai' to 'Anna Salai, Chennai'."""
    # Special multi-word city names with parent city
    # Patterns: xxx-mumbai, xxx-chennai, xxx-bangalore
    parent_cities = {
        "mumbai": "Mumbai",
        "chennai": "Chennai",
        "bangalore": "Bangalore",
    }
    for parent_slug, parent_name in parent_cities.items():
        suffix = f"-{parent_slug}"
        if slug.endswith(suffix) and slug != parent_slug:
            area = slug[: -len(suffix)]
            area_name = area.replace("-", " ").title()
            # Fix common abbreviations
            area_name = area_name.replace("Bkc", "BKC").replace("Omr", "OMR").replace("Hsr", "HSR").replace("Mg ", "MG ")
            return f"{area_name}, {parent_name}"
    # Otherwise just title-case the slug
    name = slug.replace("-", " ").title()
    name = name.replace("New Delhi", "New Delhi")
    return name


def scan_service(service_slug):
    """Scan HTML files for a service and classify locations."""
    pattern = os.path.join(BASE_DIR, f"{service_slug}-in-*.html")
    files = glob.glob(pattern)
    prefix = f"{service_slug}-in-"

    states = {}
    uts = {}
    cities = {}

    for f in sorted(files):
        basename = os.path.basename(f)
        location_slug = basename.replace(prefix, "").replace(".html", "")

        if location_slug in STATES:
            states[location_slug] = STATES[location_slug]
        elif location_slug in UTS:
            uts[location_slug] = UTS[location_slug]
        else:
            cities[location_slug] = slug_to_name(location_slug)

    return states, uts, cities


def build_js():
    """Build the location-links.js file."""
    # Collect data for all services
    service_data = {}
    for svc in SERVICES:
        states, uts, cities = scan_service(svc)
        if states or uts or cities:
            service_data[svc] = {
                "name": SERVICE_NAMES.get(svc, svc.replace("-", " ").title()),
                "s": states,   # states
                "u": uts,      # union territories
                "c": cities,   # cities
            }

    # Build compact JSON data
    data_json = json.dumps(service_data, separators=(",", ":"))

    js_code = f"""'use strict';
(function(){{
var D={data_json};
var SVC_KEYS=Object.keys(D);

function detect(){{
  var p=location.pathname.replace(/\\.html$/,"").replace(/^\\/+/,"");
  for(var i=0;i<SVC_KEYS.length;i++){{
    var k=SVC_KEYS[i];
    if(p===k||p.indexOf(k+"-in-")===0) return k;
  }}
  return null;
}}

function slugToHref(svc,loc){{return "/"+svc+"-in-"+loc;}}

function buildGroup(title,map,svc,open){{
  var keys=Object.keys(map);
  if(!keys.length) return "";
  var h='<details class="location-group"'+(open?' open':'')+'>'+
    '<summary>'+title+' ('+keys.length+')</summary>'+
    '<div class="location-grid">';
  for(var i=0;i<keys.length;i++){{
    h+='<a href="'+slugToHref(svc,keys[i])+'">'+map[keys[i]]+'</a>';
  }}
  h+='</div></details>';
  return h;
}}

function buildSection(svc){{
  var d=D[svc];
  if(!d) return null;
  var html='<section class="location-links-section" aria-label="Service available across India">'+
    '<h2>Available Across India</h2>'+
    '<p class="location-subtitle">'+d.name+' in every state and major city. Click to view location-specific details, fees, and regulatory information.</p>'+
    buildGroup("States",d.s,svc,true)+
    buildGroup("Union Territories",d.u,svc,false)+
    buildGroup("Cities",d.c,svc,false)+
    '</section>';
  var el=document.createElement("div");
  el.innerHTML=html;
  return el.firstChild;
}}

function inject(){{
  var svc=detect();
  if(!svc) return;
  // Don't double-inject
  if(document.querySelector(".location-links-section")) return;
  var section=buildSection(svc);
  if(!section) return;
  // Try to insert before Related Services nav or FAQ
  var nav=document.querySelector('nav[aria-label*="Related"]');
  if(nav){{nav.parentNode.insertBefore(section,nav);return;}}
  var faq=document.querySelector('[class*="faq"],[id*="faq"]');
  if(faq){{faq.parentNode.insertBefore(section,faq);return;}}
  // Fallback: append to article or #root content
  var article=document.querySelector("article");
  if(article){{article.appendChild(section);return;}}
  var root=document.getElementById("root");
  if(root&&root.firstElementChild){{root.firstElementChild.appendChild(section);}}
}}

// Wait for React to hydrate by observing #root mutations
var root=document.getElementById("root");
if(!root){{document.addEventListener("DOMContentLoaded",function(){{
  root=document.getElementById("root");
  if(root) observe(root); else inject();
}});}} else {{observe(root);}}

function observe(r){{
  // If React already rendered (article exists), inject immediately
  if(r.querySelector("article")){{inject();return;}}
  var mo=new MutationObserver(function(muts,obs){{
    if(r.querySelector("article")){{
      obs.disconnect();
      inject();
    }}
  }});
  mo.observe(r,{{childList:true,subtree:true}});
  // Safety timeout: try anyway after 5s
  setTimeout(function(){{mo.disconnect();inject();}},5000);
}}
}})();
"""

    js_path = os.path.join(JS_DIR, "location-links.js")
    with open(js_path, "w") as f:
        f.write(js_code)

    size_kb = os.path.getsize(js_path) / 1024
    print(f"Generated {js_path}")
    print(f"  Size: {size_kb:.1f} KB")
    print(f"  Services: {len(service_data)}")
    for svc, data in service_data.items():
        print(f"    {svc}: {len(data['s'])}S + {len(data['u'])}U + {len(data['c'])}C = {len(data['s'])+len(data['u'])+len(data['c'])} locations")

    return js_path


def build_inject_script():
    """Generate a shell script to inject <script> tags into all HTML files."""
    script_path = os.path.join(BASE_DIR, "scripts", "inject-location-js-tag.sh")

    sh = """#!/bin/bash
# inject-location-js-tag.sh
# Adds <script src="/js/location-links.js"></script> before </body> in all HTML files
# that don't already have it.

DIR="$(cd "$(dirname "$0")/.." && pwd)"
COUNT=0
SKIP=0

for f in "$DIR"/*.html; do
  if grep -q 'location-links\\.js' "$f" 2>/dev/null; then
    SKIP=$((SKIP+1))
    continue
  fi
  # Insert the script tag before </body>
  sed -i '' 's|</body>|<script src="/js/location-links.js" defer></script>\\n</body>|' "$f"
  COUNT=$((COUNT+1))
done

echo "Injected script tag into $COUNT HTML files ($SKIP already had it)"
"""

    with open(script_path, "w") as f:
        f.write(sh)
    os.chmod(script_path, 0o755)
    print(f"\nGenerated {script_path}")
    return script_path


if __name__ == "__main__":
    build_js()
    build_inject_script()
