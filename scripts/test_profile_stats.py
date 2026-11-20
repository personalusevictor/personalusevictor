import unittest
from datetime import date, timedelta
from unittest.mock import patch

from profile_stats import Calendar, snapshot, streaks


class ProfileStatsTests(unittest.TestCase):
    def test_calendar_pairs_dates_with_exact_counts_instead_of_color_levels(self):
        calendar = Calendar()
        calendar.feed(
            """<td id="day-a" data-date="2026-11-14" data-level="4"></td>
        <tool-tip for="day-a">1,024 contributions on November 14th.</tool-tip>
        <td id="day-b" data-date="2026-11-13"></td>
        <tool-tip for="day-b">No contributions on November 13th.</tool-tip>"""
        )
        self.assertEqual(calendar.counts, {"2026-11-14": 1024, "2026-11-13": 0})

    def test_yesterday_keeps_current_streak_alive_when_today_is_empty(self):
        today = date(2026, 11, 14)
        days = {str(today - timedelta(days=n)): 1 for n in [1, 2, 3, 8, 9]}
        self.assertEqual(streaks(days, today), (3, 3))

    def test_gap_ends_current_streak_but_preserves_longest(self):
        today = date(2026, 11, 14)
        days = {str(today - timedelta(days=n)): 1 for n in [3, 4, 5, 6]}
        self.assertEqual(streaks(days, today), (0, 4))

    def test_streak_does_not_claim_days_outside_measured_year(self):
        today = date(2026, 11, 14)
        days = {str(today - timedelta(days=n)): 1 for n in range(400)}
        self.assertEqual(streaks(days, today), (365, 365))

    def test_incomplete_calendar_fails_instead_of_fabricating_zeroes(self):
        with patch(
            "profile_stats.fetch", side_effect=["[]", "<html>Unavailable</html>"]
        ):
            with self.assertRaisesRegex(ValueError, "Calendario incompleto"):
                snapshot("personalusevictor", date(2026, 11, 14))


if __name__ == "__main__":
    unittest.main()
