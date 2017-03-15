import datetime
import unittest
import uuid
from emis_domain import create_app
from emis_domain.api.schema import *


class DomainSchemaTestCase(unittest.TestCase):


    def setUp(self):
        self.app = create_app("test")

        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()
        self.schema = DomainSchema()


    def tearDown(self):
        self.schema = None

        self.app_context.pop()


    def test_empty1(self):
        client_data = {
            }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
                "_schema": ["Input data must have a domain key"]
            })


    def test_empty2(self):
        client_data = {
                "domain": {}
            }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
                "user": ["Missing data for required field."],
                "name": ["Missing data for required field."],
                "pathname": ["Missing data for required field."],
            })


    def test_invalid_user(self):
        client_data = {
                "domain": {
                    "user": "blah",
                    "name": "my_domain",
                    "pathname": "my_path/blah_domain.csv",
                }
            }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
                "user": ["Not a valid UUID."],
            })


    def test_empty_name(self):
        client_data = {
                "domain": {
                    "user": uuid.uuid4(),
                    "name": "",
                    "pathname": "my_path/blah_domain.csv",
                }
            }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
                "name": ["Shorter than minimum length 1."]
            })


    def test_empty_pathname(self):
        client_data = {
                "domain": {
                    "user": uuid.uuid4(),
                    "name": "my_domain",
                    "pathname": "",
                }
            }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
                "pathname": ["Shorter than minimum length 1."]
            })


    def test_usecase1(self):

        client_data = {
                "domain": {
                    "user": uuid.uuid4(),
                    "name": "my_domain",
                    "pathname": "my_path/blah_domain.csv",
                }
            }
        data, errors = self.schema.load(client_data)

        self.assertFalse(errors)

        self.assertTrue(hasattr(data, "id"))
        self.assertTrue(isinstance(data.id, uuid.UUID))

        self.assertTrue(hasattr(data, "user"))
        self.assertTrue(isinstance(data.user, uuid.UUID))

        self.assertTrue(hasattr(data, "name"))
        self.assertEqual(data.name, "my_domain")

        self.assertTrue(hasattr(data, "pathname"))
        self.assertEqual(data.pathname, "my_path/blah_domain.csv")

        self.assertTrue(hasattr(data, "posted_at"))
        self.assertTrue(isinstance(data.posted_at, datetime.datetime))


        data.id = uuid.uuid4()
        data, errors = self.schema.dump(data)

        self.assertFalse(errors)
        self.assertTrue("domain" in data)

        domain = data["domain"]

        self.assertTrue("id" not in domain)
        self.assertTrue("name" in domain)
        self.assertTrue("pathname" in domain)
        self.assertTrue("posted_at" in domain)

        self.assertTrue("_links" in domain)

        links = domain["_links"]

        self.assertTrue("self" in links)
        self.assertTrue("collection" in links)


if __name__ == "__main__":
    unittest.main()
