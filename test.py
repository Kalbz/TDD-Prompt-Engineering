"""
Unit tests for the Concert Itinerary Builder.

This file contains unit tests for the ItineraryBuilder class in main.py.
Participants will implement tests based on the system specifications.
"""

import unittest
from main import Concert, ItineraryBuilder
from concerts_data import get_all_concerts

class ItineraryBuilderTest(unittest.TestCase):
    """Test cases for the ItineraryBuilder class."""
    
    def setUp(self):
        """Set up for the tests."""
        self.builder = ItineraryBuilder()
        
        self.all_concerts = get_all_concerts()


    # ----- Manual Test Cases -----
    # Participants will implement their manual test cases here. 
    
    def test_manual_1(self):
        """First manually written test case."""
        # TODO: Implement this test
        all_concerts = self.builder.build_itinerary(self.all_concerts)
        self.assertIsInstance(all_concerts, list, "Expected a list of concerts")
        self.assertEqual(len(all_concerts), 26, "Expected 26 concerts in the itinerary")
        self.assertIsInstance(all_concerts[0], Concert, "Expected the first item to be a Concert object")
        self.assertEqual(all_concerts[0].artist, "Taylor Swift", "Expected the first concert to be by Taylor Swift")
        self.assertEqual(all_concerts[0].date, "2025-06-10", "Expected the first concert date to be 2025-06-10")
        self.assertEqual(all_concerts[0].location, "Stockholm", "Expected the first concert location to be Stockholm")
        self.assertAlmostEqual(all_concerts[0].latitude, 59.3293, "Expected the first concert latitude to be 59.3293")
        self.assertAlmostEqual(all_concerts[0].longitude, 18.0686, "Expected the first concert longitude to be 18.0686")

        pass
    
    def test_manual_2(self):
        """First manually written test case."""
        all_concerts = self.builder.build_itinerary(self.all_concerts)

        dates = [concert.date for concert in all_concerts]
        self.assertEqual(len(dates), len(set(dates)), "Expected all concert dates to be unique")
        
        numeric_dates = [int(date.replace("-", "")) for date in dates]
        self.assertEqual(numeric_dates, sorted(numeric_dates), "Expected concerts to be sorted chronologically by date")

        artists = [concert.artist for concert in all_concerts]
        self.assertIn("Kendrick Lamar", artists, "Artist with only one concert (Kendrick Lamar) was not prioritized")

        test_concerts = [
        Concert("Concert A", "2025-06-09", "Stockholm", 59.3293, 18.0686),
        Concert("Concert B", "2025-06-10", "Berlin", 52.5200, 13.4050),
        Concert("Concert C", "2025-06-10", "Uppsala", 59.8586, 17.6389),
    ]
        self.assertEqual(len(itinerary), 2, "Expected 2 concerts in the itinerary")
        self.assertEqual(itinerary[0].artist, "Concert A", "First concert should be Concert A")
        self.assertEqual(itinerary[1].artist, "Concert C", "Expected Concert C to be chosen as its closer to Concert A")

    def test_manual_3(self):
        """Third manually written test case."""
        all_concerts = self.builder.build_itinerary(self.all_concerts)
        list_of_artists = []

        for concert in all_concerts:
            artist = concert.artist
            self.assertNotIn(artist, list_of_artists, f"Artist '{artist}' appears more than once in the itinerary")
            list_of_artists.append(artist)

            artist_concerts = [c for c in self.all_concerts if c.artist == artist]
            artist_concerts.sort(key=lambda c: int(c.date.replace("-", "")))
            earliest_concert = artist_concerts[0]

            self.assertEqual(
                concert.date,
                earliest_concert.date,
                f"The concert for '{artist}' is not their earliest one (expected {earliest_concert.date}, got {concert.date})"
            )

        all_artists = set(c.artist for c in self.all_concerts)
        artists_in_itinerary = set(list_of_artists)
        self.assertEqual(artists_in_itinerary, all_artists, f"Some artists are missing from the itinerary: {all_artists - artists_in_itinerary}")



    # ----- AI-Assisted Test Cases -----
    # Participants will implement their AI-assisted test cases here.
    # Please name your test in a way which indicates that these are AI-assisted test cases.
    def test_ai_single_concert_per_artist_and_chronological_order(self):
        """
        Covers:
        - Only earliest concert per artist (Constraint 3)
        - Sorted in chronological order (Constraint 2)
        - Each concert includes artist, date, and location (Constraint 1)
        """
        concerts = [
            Concert("Taylor Swift", "2025-07-15", "Copenhagen", 55.6761, 12.5683),
            Concert("Taylor Swift", "2025-05-20", "Oslo", 59.9139, 10.7522),
            Concert("Ed Sheeran", "2025-06-05", "Gothenburg", 57.7089, 11.9746),
        ]
        itinerary = self.builder.build_itinerary(concerts)
        self.assertEqual(len(itinerary), 2)
        self.assertEqual(itinerary[0].artist, "Taylor Swift")
        self.assertEqual(itinerary[0].date, "2025-05-20")
        self.assertEqual(itinerary[1].artist, "Ed Sheeran")
        self.assertEqual(itinerary[1].location, "Gothenburg")

    def test_ai_conflict_same_day_concerts_pick_closest_to_last(self):
        """
        Covers:
        - No two concerts on same day (Constraint 5)
        - Resolve conflict by choosing one closest to the last concert
        """
        concerts = [
            Concert("Adele", "2025-06-10", "Berlin", 52.5200, 13.4050),
            Concert("Beyoncé", "2025-06-10", "Copenhagen", 55.6761, 12.5683),
            Concert("Dua Lipa", "2025-06-05", "Oslo", 59.9139, 10.7522),
        ]
        itinerary = self.builder.build_itinerary(concerts)
        self.assertEqual(len(itinerary), 2)
        self.assertEqual(itinerary[0].artist, "Dua Lipa")  # 06-05
        self.assertIn(itinerary[1].artist, ["Adele", "Beyoncé"])  # Closest to Oslo

    def test_ai_prioritize_single_concert_artists_and_handle_missing(self):
        """
        Covers:
        - Prioritize artists with only one concert (Constraint 6)
        - Artists not in the concert list are not added (Constraint 4)
        """
        concerts = [
            Concert("BTS", "2025-07-01", "Copenhagen", 55.6761, 12.5683),
            Concert("Dua Lipa", "2025-07-01", "Oslo", 59.9139, 10.7522),
            Concert("Justin Bieber", "2025-07-01", "Malmö", 55.6050, 13.0038),
        ]
        itinerary = self.builder.build_itinerary(concerts)
        self.assertEqual(len(itinerary), 1)
        self.assertEqual(itinerary[0].artist, "Justin Bieber")  # Only artist with one concert

        # Make sure an artist not in the list is not included
        self.assertNotIn("Rihanna", [c.artist for c in itinerary])



if __name__ == "__main__":
    unittest.main()