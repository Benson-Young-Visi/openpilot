from __future__ import annotations

from openpilot.starpilot.common.maps_selection import COUNTRY_PREFIX, STATE_PREFIX, normalize_maps_selected

MAP_SCHEDULE_LABELS = {
  0: "Manually",
  1: "Weekly",
  2: "Monthly",
}
MAP_SCHEDULE_VALUE_BY_LABEL = {label: value for value, label in MAP_SCHEDULE_LABELS.items()}
MAP_SCHEDULE_OPTIONS = [
  {"value": value, "label": label}
  for value, label in MAP_SCHEDULE_LABELS.items()
]

COUNTRY_REGION_GROUPS = (
  {"key": "africa", "title": "Africa", "regions": {"DZ": "Algeria", "AO": "Angola", "BJ": "Benin", "BW": "Botswana", "BF": "Burkina Faso", "BI": "Burundi", "CM": "Cameroon", "CF": "Central African Republic", "TD": "Chad", "KM": "Comoros", "CG": "Congo (Brazzaville)", "CD": "Congo (Kinshasa)", "DJ": "Djibouti", "EG": "Egypt", "GQ": "Equatorial Guinea", "ER": "Eritrea", "ET": "Ethiopia", "GA": "Gabon", "GM": "Gambia", "GH": "Ghana", "GN": "Guinea", "GW": "Guinea-Bissau", "CI": "Ivory Coast", "KE": "Kenya", "LS": "Lesotho", "LR": "Liberia", "LY": "Libya", "MG": "Madagascar", "MW": "Malawi", "ML": "Mali", "MR": "Mauritania", "MA": "Morocco", "MZ": "Mozambique", "NA": "Namibia", "NE": "Niger", "NG": "Nigeria", "RW": "Rwanda", "SN": "Senegal", "SL": "Sierra Leone", "SO": "Somalia", "ZA": "South Africa", "SS": "South Sudan", "SD": "Sudan", "SZ": "Swaziland", "TZ": "Tanzania", "TG": "Togo", "TN": "Tunisia", "UG": "Uganda", "ZM": "Zambia", "ZW": "Zimbabwe"}},
  {"key": "antarctica", "title": "Antarctica", "regions": {"AQ": "Antarctica"}},
  {"key": "asia", "title": "Asia", "regions": {"AF": "Afghanistan", "AM": "Armenia", "AZ": "Azerbaijan", "BH": "Bahrain", "BD": "Bangladesh", "BT": "Bhutan", "BN": "Brunei", "KH": "Cambodia", "CN": "China", "CY": "Cyprus", "TL": "East Timor", "HK": "Hong Kong", "IN": "India", "ID": "Indonesia", "IR": "Iran", "IQ": "Iraq", "IL": "Israel", "JP": "Japan", "JO": "Jordan", "KZ": "Kazakhstan", "KW": "Kuwait", "KG": "Kyrgyzstan", "LA": "Laos", "LB": "Lebanon", "MY": "Malaysia", "MV": "Maldives", "MO": "Macao", "MN": "Mongolia", "MM": "Myanmar", "NP": "Nepal", "KP": "North Korea", "OM": "Oman", "PK": "Pakistan", "PS": "Palestine", "PH": "Philippines", "QA": "Qatar", "RU": "Russia", "SA": "Saudi Arabia", "SG": "Singapore", "KR": "South Korea", "LK": "Sri Lanka", "SY": "Syria", "TW": "Taiwan", "TJ": "Tajikistan", "TH": "Thailand", "TR": "Turkey", "TM": "Turkmenistan", "AE": "United Arab Emirates", "UZ": "Uzbekistan", "VN": "Vietnam", "YE": "Yemen"}},
  {"key": "europe", "title": "Europe", "regions": {"AL": "Albania", "AT": "Austria", "BY": "Belarus", "BE": "Belgium", "BA": "Bosnia and Herzegovina", "BG": "Bulgaria", "HR": "Croatia", "CZ": "Czech Republic", "DK": "Denmark", "EE": "Estonia", "FI": "Finland", "FR": "France", "GE": "Georgia", "DE": "Germany", "GR": "Greece", "HU": "Hungary", "IS": "Iceland", "IE": "Ireland", "IT": "Italy", "KZ": "Kazakhstan", "LV": "Latvia", "LT": "Lithuania", "LU": "Luxembourg", "MK": "Macedonia", "MD": "Moldova", "ME": "Montenegro", "NL": "Netherlands", "NO": "Norway", "PL": "Poland", "PT": "Portugal", "RO": "Romania", "RS": "Serbia", "SK": "Slovakia", "SI": "Slovenia", "ES": "Spain", "SE": "Sweden", "CH": "Switzerland", "TR": "Turkey", "UA": "Ukraine", "GB": "United Kingdom"}},
  {"key": "north_america", "title": "North America", "regions": {"BS": "Bahamas", "BZ": "Belize", "CA": "Canada", "CR": "Costa Rica", "CU": "Cuba", "DO": "Dominican Republic", "SV": "El Salvador", "GL": "Greenland", "GD": "Grenada", "GT": "Guatemala", "HT": "Haiti", "HN": "Honduras", "JM": "Jamaica", "MX": "Mexico", "NI": "Nicaragua", "PA": "Panama", "TT": "Trinidad and Tobago", "US": "United States"}},
  {"key": "oceania", "title": "Oceania", "regions": {"AU": "Australia", "FJ": "Fiji", "TF": "French Southern Territories", "NC": "New Caledonia", "NZ": "New Zealand", "PG": "Papua New Guinea", "SB": "Solomon Islands", "VU": "Vanuatu"}},
  {"key": "south_america", "title": "South America", "regions": {"AR": "Argentina", "BO": "Bolivia", "BR": "Brazil", "CL": "Chile", "CO": "Colombia", "EC": "Ecuador", "FK": "Falkland Islands", "GY": "Guyana", "PY": "Paraguay", "PE": "Peru", "SR": "Suriname", "UY": "Uruguay", "VE": "Venezuela"}},
)

STATE_REGION_GROUPS = (
  {"key": "midwest", "title": "Midwest", "regions": {"IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "MI": "Michigan", "MN": "Minnesota", "MO": "Missouri", "NE": "Nebraska", "ND": "North Dakota", "OH": "Ohio", "SD": "South Dakota", "WI": "Wisconsin"}},
  {"key": "northeast", "title": "Northeast", "regions": {"CT": "Connecticut", "ME": "Maine", "MA": "Massachusetts", "NH": "New Hampshire", "NJ": "New Jersey", "NY": "New York", "PA": "Pennsylvania", "RI": "Rhode Island", "VT": "Vermont"}},
  {"key": "south", "title": "South", "regions": {"AL": "Alabama", "AR": "Arkansas", "DE": "Delaware", "DC": "District of Columbia", "FL": "Florida", "GA": "Georgia", "KY": "Kentucky", "LA": "Louisiana", "MD": "Maryland", "MS": "Mississippi", "NC": "North Carolina", "OK": "Oklahoma", "SC": "South Carolina", "TN": "Tennessee", "TX": "Texas", "VA": "Virginia", "WV": "West Virginia"}},
  {"key": "west", "title": "West", "regions": {"AK": "Alaska", "AZ": "Arizona", "CA": "California", "CO": "Colorado", "HI": "Hawaii", "ID": "Idaho", "MT": "Montana", "NV": "Nevada", "NM": "New Mexico", "OR": "Oregon", "UT": "Utah", "WA": "Washington", "WY": "Wyoming"}},
  {"key": "territories", "title": "Territories", "regions": {"AS": "American Samoa", "GU": "Guam", "MP": "Northern Mariana Islands", "PR": "Puerto Rico", "VI": "Virgin Islands"}},
)

MAP_SECTIONS = (
  {"key": "countries", "title": "Countries", "prefix": COUNTRY_PREFIX, "groups": COUNTRY_REGION_GROUPS},
  {"key": "states", "title": "U.S. States", "prefix": STATE_PREFIX, "groups": STATE_REGION_GROUPS},
)


def normalize_schedule_value(value) -> int:
  if isinstance(value, bytes):
    value = value.decode("utf-8", errors="ignore")

  if isinstance(value, str):
    value = value.strip()
    if not value:
      return 2
    if value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
      value = int(value)
    else:
      value = MAP_SCHEDULE_VALUE_BY_LABEL.get(value, 2)

  try:
    normalized = int(value)
  except (TypeError, ValueError):
    return 2

  return normalized if normalized in MAP_SCHEDULE_LABELS else 2


def schedule_label(value) -> str:
  return MAP_SCHEDULE_LABELS[normalize_schedule_value(value)]


def schedule_param_value(value) -> str:
  return str(normalize_schedule_value(value))


def _sorted_regions(regions):
  return sorted(regions.items(), key=lambda item: item[1])


def get_maps_catalog():
  sections = []
  for section in MAP_SECTIONS:
    groups = []
    for group in section["groups"]:
      regions = [
        {
          "code": code,
          "label": label,
          "token": f"{section['prefix']}{code}",
        }
        for code, label in _sorted_regions(group["regions"])
      ]
      groups.append({
        "key": group["key"],
        "title": group["title"],
        "prefix": section["prefix"],
        "regions": regions,
      })
    sections.append({
      "key": section["key"],
      "title": section["title"],
      "prefix": section["prefix"],
      "groups": groups,
    })
  return sections


MAPS_CATALOG = get_maps_catalog()
MAP_TOKEN_LABELS = {
  region["token"]: region["label"]
  for section in MAPS_CATALOG
  for group in section["groups"]
  for region in group["regions"]
}
VALID_MAP_TOKENS = frozenset(MAP_TOKEN_LABELS)


def get_selected_map_tokens(selected_raw) -> list[str]:
  normalized = normalize_maps_selected(selected_raw)
  return [token for token in normalized.split(",") if token and token in VALID_MAP_TOKENS]


def sanitize_selected_locations_csv(values) -> str:
  if isinstance(values, str):
    raw = values
  elif values is None:
    raw = ""
  else:
    raw = ",".join(str(value).strip() for value in values if str(value).strip())

  tokens = get_selected_map_tokens(raw)
  return ",".join(tokens)


def get_selected_map_entries(selected_raw) -> list[dict[str, str]]:
  return [
    {"token": token, "label": MAP_TOKEN_LABELS[token]}
    for token in get_selected_map_tokens(selected_raw)
  ]
