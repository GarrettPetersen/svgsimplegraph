import unittest
import urllib.request
import json
from unittest.mock import patch, MagicMock
from simplegraph import CategoricalGraph


class TestUploadToGithubGist(unittest.TestCase):
    @patch("urllib.request.urlopen")
    @patch("time.time", return_value=12345)  # this will mock the time function
    def test_upload_to_github_gist(self, mock_time, mock_urlopen):
        # Define a mock response that simulates a successful upload to GitHub Gist
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(
            {
                "files": {
                    "simplegraph_test_12345.svg": {
                        "raw_url": "https://gist.github.com/mock_raw_url"
                    }
                }
            }
        ).encode("utf-8")
        mock_urlopen.return_value = mock_response

        # Create an instance of a graph
        graph = CategoricalGraph(
            width=600,
            height=400,
            bar_width=30,
            x_left_padding=60,
            x_right_padding=80,
            y_top_padding=20,
            y_bottom_padding=40,
            stacked=False,
            background_color="#404040",
        )

        graph.x_labels = ["A", "B", "C", "D", "E"]
        graph.x_axis_label = "X Axis"
        graph.primary_y_axis_label = "Primary Y Axis"

        graph.add_series([10, 20, 30, 40, 50], legend_label="Series 1")

        actual = graph.upload_to_github_gist("mock_token", "simplegraph_test")

        # Check that the mock GitHub Gist URL was returned
        expected = "https://gist.github.com/mock_raw_url"
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
