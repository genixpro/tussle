import base64
import re
import datetime
import hashlib
import random
import os
from dependency_injector.wiring import Provide, inject


class CustomIDField:
    def __init__(self, **kwargs):
        kwargs['primary_key'] = True
        super(CustomIDField, self).__init__(**kwargs)

    def validate(self, value):
        return True

    def to_mongo(self, value):
        return str(value)

    def to_python(self, value):
        return str(value)


    @classmethod
    @inject
    def generate_id(cls, model_name, owner, reference_time: datetime.datetime=None, mongo_db_connection=Provide['mongo_db_connection']):
        if reference_time is None:
            reference_time = datetime.datetime.now()

        generatedId = cls.generate_model_name_shorthand(model_name) + "-" + \
                      cls.generate_random_code() + "-" + \
                      cls.generate_second_code(reference_time) + \
                      cls.generate_minute_code(reference_time) + \
                      cls.generate_hour_code(reference_time) + \
                      cls.generate_day_code(reference_time) + \
                      cls.generate_month_code(reference_time) + \
                      cls.generate_year_code(reference_time) + "-" + \
                      cls.generate_environment_shorthand() + \
                      cls.generate_user_code(owner) + "-" + \
                      cls.generate_object_counter_value_code(model_name, owner, length=4, mongo_db_connection=mongo_db_connection)

        return generatedId

    @classmethod
    def generate_random_code(cls):
        return cls.generate_random_lowercase_letter() + \
        cls.generate_random_alphanum() + \
        cls.generate_random_alphanum() + \
        cls.generate_random_alphanum() + \
        cls.generate_random_alphanum() + \
        cls.generate_random_alphanum() + \
        cls.generate_random_alphanum() + \
        cls.generate_random_alphanum()


    @classmethod
    def generate_random_lowercase_letter(cls):
        return random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])

    @classmethod
    def generate_random_alphanum(cls):
        return random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                              's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])

    @classmethod
    def generate_random_digit(cls):
        return random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'])


    @classmethod
    def generate_model_name_shorthand(cls, model_name: str):
        assert model_name

        ignore_words = [
            'Model',
            'model',
            'Mongo',
            'mongo',
        ]

        for word in ignore_words:
            model_name = model_name.replace(word, "")

        pattern = '([A-Z][a-z])'
        matches = re.findall(pattern, model_name)
        result = ''.join(matches).lower()

        if len(result) < 4:
            pattern = '([A-Z][a-z][a-z][a-z])'
            matches = re.findall(pattern, model_name)
            result = ''.join(matches).lower()
        elif len(result) == 6:
            # Take first two characters of the first word,
            # then first character of second and third words.
            result = result[0] + result[1] + result[2] + result[4]
        elif len(result) >= 8:
            # Take first character of all four words. Ignore remaining words.
            result = result[0] + result[2] + result[4] + result[6]

        return result


    @classmethod
    def generate_environment_shorthand(cls):
        environment = os.environ.get("FLOWTHOUGHT_ENV", "development")
        return environment[0]


    @classmethod
    def generate_year_code(cls, reference_time: datetime.datetime):
        year = reference_time.year
        companyFoundingYear = 2023
        yearDigit = year - companyFoundingYear
        return cls.get_one_digit_code(yearDigit)

    @classmethod
    def generate_month_code(cls, reference_time: datetime.datetime):
        return cls.get_one_digit_code(reference_time.month)

    @classmethod
    def generate_day_code(cls, reference_time: datetime.datetime):
        return cls.get_one_digit_code(reference_time.day)

    @classmethod
    def generate_hour_code(cls, reference_time: datetime.datetime):
        hour = reference_time.hour

        if hour >= 12:
            hour -= 12

        return cls.get_one_digit_code(hour)

    @classmethod
    def generate_minute_code(cls, reference_time: datetime.datetime):
        # We don't want to generate codes that use capital letters, so
        # the one digital code value can not exceed 36. Since seconds
        # go between 0 and 59, we have to cut in half and count
        # only every other second in the code.
        return cls.get_one_digit_code(round(reference_time.minute / 2.0))

    @classmethod
    def generate_second_code(cls, reference_time: datetime.datetime):
        # We don't want to generate codes that use capital letters, so
        # the one digital code value can not exceed 36. Since seconds
        # go between 0 and 59, we have to cut in half and count
        # only every other second in the code.
        return cls.get_one_digit_code(round(reference_time.second / 2.0))


    one_digit_code_characters = '0123456789abcdefghijklmnopqrstuvwxyz'
    @classmethod
    def get_one_digit_code(cls, value):
        assert 0 <= value < 36
        return cls.one_digit_code_characters[value]


    @classmethod
    @inject
    def generate_object_counter_value_code(cls, model_name, owner, length, mongo_db_connection=Provide['mongo_db_connection']):
        query_parameters = {}
        query_parameters['className'] = model_name
        query_parameters['owner'] = owner

        # We have to bypass MongoEngine here because it doesn't handle the $inc operator in a properly
        # atomic way.
        counter_object = mongo_db_connection['counter_model'].find_one_and_update(
            filter=query_parameters,
            update={'$inc': {'counter': 1}},
            upsert=True,
            return_document=True
        )

        counter_str = str(counter_object['counter'])

        while len(counter_str) < length:
            counter_str = "0" + counter_str

        return counter_str[-length:]

    userSalt = "V#id9mZAT$gDy5"

    @classmethod
    def generate_user_code(cls, owner):
        return cls.compute_short_hash(data=str(owner), salt=cls.userSalt, length=3)



    @classmethod
    def compute_short_hash(cls, data, salt, length):
        hasher = hashlib.sha256()
        hasher.update(bytes(data, 'utf8'))
        hasher.update(bytes(salt, 'utf8'))

        base64ExtraCharacters = bytes("--", 'utf8')
        longHash = str(base64.b64encode(hasher.digest(), altchars=base64ExtraCharacters), 'utf8')
        longHash = longHash.replace("-", "")
        longHash = longHash.replace("=", "")

        shortHash = longHash[::int(len(longHash) / length)].lower()

        while len(shortHash) < length:
            shortHash += "0"

        return shortHash[:length]


