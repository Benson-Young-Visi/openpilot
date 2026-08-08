from openpilot.starpilot.common.theme_asset_names import (
  canonicalize_theme_asset_name,
  find_matching_theme_asset_file,
  find_matching_theme_asset_name,
)


def test_canonicalize_theme_asset_name_normalizes_boot_logo_variants():
  assert canonicalize_theme_asset_name("new-years.jpg") == canonicalize_theme_asset_name("New Years")
  assert canonicalize_theme_asset_name("frog's_day.png") == canonicalize_theme_asset_name("Frogs Day")
  assert canonicalize_theme_asset_name("foo~creator.jpeg") == canonicalize_theme_asset_name("Foo - by: creator")


def test_find_matching_theme_asset_name_handles_display_name_variants():
  candidates = ["new-years", "frog's_day", "foo~creator"]

  assert find_matching_theme_asset_name(candidates, "New Years") == "new-years"
  assert find_matching_theme_asset_name(candidates, "Frogs Day") == "frog's_day"
  assert find_matching_theme_asset_name(candidates, "Foo - by: creator") == "foo~creator"


def test_find_matching_theme_asset_file_handles_non_exact_boot_logo_names(tmp_path):
  expected = tmp_path / "new-years.jpg"
  expected.write_bytes(b"jpg")
  (tmp_path / "frog's_day.png").write_bytes(b"png")

  assert find_matching_theme_asset_file(tmp_path, "New Years") == expected
  assert find_matching_theme_asset_file(tmp_path, "Frogs Day").name == "frog's_day.png"
