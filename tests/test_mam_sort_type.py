import unittest

from app import RESULTS_SORT_MODES, mam_sort_type_for_results_sort_mode


class MamSortTypeTests(unittest.TestCase):
    def test_maps_stat_sorts_to_mam_sort_types(self):
        self.assertEqual(mam_sort_type_for_results_sort_mode("snatches_desc"), "snatchedDesc")
        self.assertEqual(mam_sort_type_for_results_sort_mode("snatches_asc"), "snatchedAsc")
        self.assertEqual(mam_sort_type_for_results_sort_mode("seeders_desc"), "seedersDesc")
        self.assertEqual(mam_sort_type_for_results_sort_mode("size_asc"), "sizeAsc")
        self.assertEqual(mam_sort_type_for_results_sort_mode("date_uploaded_desc"), "dateDesc")
        self.assertEqual(mam_sort_type_for_results_sort_mode("title_asc"), "titleAsc")

    def test_client_only_sorts_use_mam_default(self):
        for mode in ("quality_desc", "author_asc", "author_desc"):
            self.assertEqual(mam_sort_type_for_results_sort_mode(mode), "default")

    def test_unknown_or_missing_sort_uses_mam_default(self):
        self.assertEqual(mam_sort_type_for_results_sort_mode("bogus"), "default")
        self.assertEqual(mam_sort_type_for_results_sort_mode(None), "default")

    def test_every_sort_mode_maps_to_a_value(self):
        for mode in RESULTS_SORT_MODES:
            self.assertTrue(mam_sort_type_for_results_sort_mode(mode))


if __name__ == "__main__":
    unittest.main()
