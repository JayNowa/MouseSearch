import unittest

from app import build_relative_path_from_template, relative_path_tokens_from_metadata


SHELFMARK_STYLE = "{Author}/{Title}{ - Series}{ #SeriesNumber}{ (Year)}"


def tokens(**overrides):
    values = {
        "{Author}": "",
        "{Series}": "",
        "{SeriesNumber}": "",
        "{Title}": "",
        "{Genre}": "",
        "{Format}": "",
        "{Category}": "",
        "{Year}": "",
    }
    values.update({f"{{{key}}}": value for key, value in overrides.items()})
    return values


class RelativePathTemplateTests(unittest.TestCase):
    def test_plain_tokens_collapse_empty_levels(self):
        values = tokens(Author="Frank Herbert", Title="Dune")
        self.assertEqual(build_relative_path_from_template("{Author}/{Series}/{Title}", values), "Frank Herbert/Dune")
        self.assertEqual(build_relative_path_from_template("/{Author}//{Title}/", values), "Frank Herbert/Dune")

    def test_optional_groups_render_with_values(self):
        values = tokens(
            Author="Brandon Sanderson",
            Title="Oathbringer",
            Series="The Stormlight Archive",
            SeriesNumber="3",
            Year="2017",
        )
        self.assertEqual(
            build_relative_path_from_template(SHELFMARK_STYLE, values),
            "Brandon Sanderson/Oathbringer - The Stormlight Archive #3 (2017)",
        )

    def test_optional_groups_drop_when_empty(self):
        self.assertEqual(
            build_relative_path_from_template(
                SHELFMARK_STYLE, tokens(Author="Andy Weir", Title="Project Hail Mary", Year="2021")
            ),
            "Andy Weir/Project Hail Mary (2021)",
        )
        self.assertEqual(
            build_relative_path_from_template(SHELFMARK_STYLE, tokens(Author="Andy Weir", Title="Project Hail Mary")),
            "Andy Weir/Project Hail Mary",
        )

    def test_series_number_is_not_read_as_series(self):
        values = tokens(Title="T", Series="S", SeriesNumber="")
        self.assertEqual(build_relative_path_from_template("{Title}{ #SeriesNumber}", values), "T")

    def test_optional_group_can_add_a_folder(self):
        template = "{Author}/{Series/}{Title}"
        self.assertEqual(
            build_relative_path_from_template(template, tokens(Author="A", Series="S", Title="T")), "A/S/T"
        )
        self.assertEqual(build_relative_path_from_template(template, tokens(Author="A", Title="T")), "A/T")

    def test_segments_are_trimmed(self):
        self.assertEqual(
            build_relative_path_from_template("{Author}/{Title} {(Year)}", tokens(Author="A", Title="T")), "A/T"
        )

    def test_unknown_groups_are_left_alone(self):
        self.assertEqual(
            build_relative_path_from_template("{Author}/{Unknown}", tokens(Author="A")), "A/{Unknown}"
        )

    def test_backslashes_are_normalized(self):
        self.assertEqual(
            build_relative_path_from_template("{Author}\\{Title}", tokens(Author="A", Title="T")), "A/T"
        )


class RelativePathTokensFromMetadataTests(unittest.TestCase):
    def test_year_token_from_metadata(self):
        meta = {"author": "Andy Weir", "title": "Project Hail Mary", "year": "2021"}
        self.assertEqual(relative_path_tokens_from_metadata(meta)["{Year}"], "2021")
        self.assertEqual(
            build_relative_path_from_template(SHELFMARK_STYLE, relative_path_tokens_from_metadata(meta)),
            "Andy Weir/Project Hail Mary (2021)",
        )

    def test_missing_or_invalid_year_is_blank(self):
        self.assertEqual(relative_path_tokens_from_metadata({})["{Year}"], "")
        self.assertEqual(relative_path_tokens_from_metadata({"year": "unknown"})["{Year}"], "")
        self.assertEqual(relative_path_tokens_from_metadata({"year": 2017})["{Year}"], "2017")
        self.assertEqual(relative_path_tokens_from_metadata({"year": "2017-11-14"})["{Year}"], "2017")


if __name__ == "__main__":
    unittest.main()
