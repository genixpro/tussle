import datetime
from tussle.general.testing.test_case_base import ArticulonTestCaseBase
from. custom_id_field import CustomIDField
import re
import concurrent.futures

class CustomIDFieldTests(ArticulonTestCaseBase):

    def test_generated_id_format(self):
        test_reference_time = datetime.datetime.now()
        test_owner = "test_owner"

        generated_id = CustomIDField.generate_id(
            model_name="TestingModel",
            owner=test_owner,
            reference_time=test_reference_time,
            mongo_db_connection=self.container.mongo_db_connection(),
        )

        # Count the number of dashes in the generated_id, there should be 4, one inbetween each of the 5 segments.
        count = generated_id.count("-")
        self.assertEqual(count, 4)

        # Split the generated_id by dashes.
        parts = generated_id.split("-")

        # The first segment should be the model name and be 4 characters long.
        self.assertEqual(parts[0], "test")
        self.assertEqual(len(parts[0]), 4)

        # The second segment is the random entropy segment. It should be 8 characters long.
        random_entropy_segment = parts[1]
        self.assertEqual(len(random_entropy_segment), 8)

        # The third segment is the time of creation segment. It should be 6 characters long.
        time_segment = parts[2]
        self.assertEqual(len(time_segment), 6)
        # First digit is the second code.
        self.assertEqual(time_segment[0], CustomIDField.generate_second_code(test_reference_time))
        # Second digit is the minute code.
        self.assertEqual(time_segment[1], CustomIDField.generate_minute_code(test_reference_time))
        # Third digit is the hour code.
        self.assertEqual(time_segment[2], CustomIDField.generate_hour_code(test_reference_time))
        # Fourth digit is the day code.
        self.assertEqual(time_segment[3], CustomIDField.generate_day_code(test_reference_time))
        # Fifth digit is the month code.
        self.assertEqual(time_segment[4], CustomIDField.generate_month_code(test_reference_time))
        # Sixth digit is the year code.
        self.assertEqual(time_segment[5], CustomIDField.generate_year_code(test_reference_time))

        # The fourth segment is the owner & environment segment. It should be 4 characters long.
        self.assertEqual(len(parts[3]), 4)
        owner_environment_segment = parts[3]
        environment_piece = owner_environment_segment[0]
        self.assertEqual(environment_piece, CustomIDField.generate_environment_shorthand())
        owner_piece = owner_environment_segment[1:]
        self.assertEqual(owner_piece, CustomIDField.generate_user_code(test_owner))

        # The last segment is the users object counter segment. It should be 4 characters long.
        self.assertEqual(len(parts[4]), 4)
        object_counter_segment = parts[4]
        # It should just be an integer that is incremented every time a new object is created.
        self.assertTrue(re.match(r"^\d+$", object_counter_segment))

    def test_compute_short_hash(self):
        test_string = "test_string"
        test_salt = "12345"
        result = CustomIDField.compute_short_hash(test_string, test_salt, 4)

        # The result should be 4 characters long.
        self.assertEqual(len(result), 4)

        # The result should be the same every time.
        self.assertEqual(result, CustomIDField.compute_short_hash(test_string, test_salt, 4))

        # The result should change if we change the user hash.
        self.assertNotEqual(result, CustomIDField.compute_short_hash(test_string, "different_salt", 4))

    def test_generate_random_code(self):
        generated = CustomIDField.generate_random_code()

        self.assertEqual(len(generated), 8)

    def test_test_generate_random_code_parallelism(self):
        # Try and generate a whole bunch of random codes in parallel. Make sure they're all unique.
        test_count = 1000

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for n in range(test_count):
                futures.append(executor.submit(CustomIDField.generate_random_code))

            unique_id_set = set([future.result() for future in futures])

            # Check that the unique_id_set has the correct number of items in it, which means all the ids got generated uniquely
            self.assertEqual(len(unique_id_set), test_count)

    def test_generate_object_counter_value_code(self):
        generated = CustomIDField.generate_object_counter_value_code("TestingModel", "test_owner", 4, mongo_db_connection=self.container.mongo_db_connection())

        self.assertEqual(len(generated), 4)

    def test_generate_object_counter_value_code_parallelism(self):
        # Try and generate a whole bunch of counter portions in parallel. They should all come out as unique.
        test_count = 100

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for n in range(test_count):
                futures.append(executor.submit(CustomIDField.generate_object_counter_value_code, "TestingModel", "test_owner", 4, mongo_db_connection=self.container.mongo_db_connection()))

            unique_id_set = set([future.result() for future in futures])

            # Check that the unique_id_set has the correct number of items in it, which means all the ids got generated uniquely
            self.assertEqual(len(unique_id_set), test_count)

    def test_generate_id_parallelism(self):
        # Try and generate a whole bunch of counter portions in parallel. They should all come out as unique.
        test_count = 100

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for n in range(test_count):
                futures.append(executor.submit(CustomIDField.generate_id, "TestingModel", "test_owner", reference_time=datetime.datetime.now(), mongo_db_connection=self.container.mongo_db_connection()))

            unique_id_set = set([future.result() for future in futures])

            # Check that the unique_id_set has the correct number of items in it, which means all the ids got generated uniquely
            self.assertEqual(len(unique_id_set), test_count)

    def test_generate_model_name_shorthand(self):
        # Here we test what the shorthand is for several model names.
        test_cases = {
            # It should take the first two characters of the first two words
            "PromptChart": "prch",
            # The system should ignore the words mongo and model
            "PromptChartMongo": "prch",
            "PromptChartModel": "prch",
            "PromptChartMongoModel": "prch",
            "BulkChartEvaluationMongoModel": "buce",
            # The system should ignore the words mongo and model
            "SingleChartEvaluationMongoModel": "sice",
            # If there is only one word, take the first four letters
            "File": "file",
            "FileModel": "file",
            "Awesome": "awes",
            "AwesomeModel": "awes",
            # If there are four words in the model name, use first letter of all four
            "SuperAwesomeTestingSystemModel": "sats",
        }

        for test_model_name, expected_shorthand in test_cases.items():
            with self.subTest(model_name=test_model_name):
                result = CustomIDField.generate_model_name_shorthand(model_name=test_model_name)
                self.assertEqual(expected_shorthand, result)

