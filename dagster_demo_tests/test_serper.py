import unittest
import os

from dotenv import load_dotenv
load_dotenv()

from dagster_demo.app.serper import Serper


class TestSerper(unittest.TestCase):
    def setUp(self): # define seUp function
        self.serper = Serper(api_key=os.getenv('SERPER_API_KEY'))

    def test_lookUp_text(self): # test function for lookUp
        brands_list = ["tesla", "lucid"]
        result_list = self.serper.search(brands_list)
        assert len(result_list) == len(brands_list)
        assert len(result_list[0]['topStories']) == 10


if __name__ == "__main__":
    unittest.main()


