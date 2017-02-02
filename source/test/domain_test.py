import os.path
import unittest
import uuid
from flask import current_app, json
from emis_domain import create_app, db
from emis_domain.api.schema import *


class DomainTestCase(unittest.TestCase):


    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        self.user1 = uuid.uuid4()
        self.user2 = uuid.uuid4()
        self.user3 = uuid.uuid4()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def post_domains(self):

        # user1: two domains
        # user2: one domain
        # user3: no domain
        payloads = [
                {
                    "user": self.user1,
                    "name": "domain1",
                    "pathname": "/some_path/domain1.csv",
                },
                {
                    "user": self.user2,
                    "name": "domain2",
                    "pathname": "/some_path/domain2.csv",
                },
                {
                    "user": self.user1,
                    "name": "domain3",
                    "pathname": "/some_path/domain3.csv",
                },
            ]

        for payload in payloads:
            response = self.client.post("/domains",
                data=json.dumps({"domain": payload}),
                content_type="application/json")
            data = response.data.decode("utf8")

            self.assertEqual(response.status_code, 201, "{}: {}".format(
                response.status_code, data))

    def do_test_get_domains_by_user(self,
            user_id,
            nr_results_required):

        self.post_domains()

        response = self.client.get("/domains/{}".format(user_id))
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("domains" in data)

        domains = data["domains"]

        self.assertEqual(len(domains), nr_results_required)


    def test_get_domains_by_user1(self):
        self.do_test_get_domains_by_user(self.user1, 2)


    def test_get_domains_by_user2(self):
        self.do_test_get_domains_by_user(self.user2, 1)


    def test_get_domains_by_user3(self):
        self.do_test_get_domains_by_user(self.user3, 0)


    def test_get_all_domains1(self):
        # No domains posted.
        response = self.client.get("/domains")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("domains" in data)
        self.assertEqual(data["domains"], [])


    def test_get_all_domains2(self):
        # Some domains posted.
        self.post_domains()

        response = self.client.get("/domains")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("domains" in data)

        domains = data["domains"]

        self.assertEqual(len(domains), 3)


    def test_get_domain(self):
        self.post_domains()

        response = self.client.get("/domains")
        data = response.data.decode("utf8")
        data = json.loads(data)
        domains = data["domains"]
        domain = domains[0]
        uri = domain["_links"]["self"]
        response = self.client.get(uri)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("domain" in data)

        self.assertEqual(data["domain"], domain)

        self.assertTrue("id" not in domain)

        self.assertTrue("posted_at" in domain)

        self.assertTrue("name" in domain)
        self.assertEqual(domain["name"], "domain1")

        self.assertTrue("pathname" in domain)
        self.assertEqual(domain["pathname"], "/some_path/domain1.csv")

        self.assertTrue("_links" in domain)

        links = domain["_links"]

        self.assertTrue("self" in links)
        self.assertEqual(links["self"], uri)

        self.assertTrue("collection" in links)


    def test_get_invalid_user_domain(self):
        self.post_domains()

        response = self.client.get("/domains")
        data = response.data.decode("utf8")
        data = json.loads(data)
        domains = data["domains"]
        domain = domains[0]
        uri = domain["_links"]["self"]
        # Invalidate user-id
        uri, domain_id = os.path.split(uri)
        uri, user_id = os.path.split(uri)
        uri = os.path.join(uri, str(uuid.uuid4()), domain_id)
        response = self.client.get(uri)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 400, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


    def test_get_unexisting_domain(self):
        self.post_domains()

        response = self.client.get("/domains")
        data = response.data.decode("utf8")
        data = json.loads(data)
        domains = data["domains"]
        domain = domains[0]
        uri = domain["_links"]["self"]
        # Invalidate uri
        uri = os.path.join(os.path.split(uri)[0], str(uuid.uuid4()))
        response = self.client.get(uri)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 400, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


    def test_post_domain(self):
        user_id = uuid.uuid4()
        payload = {
                "user": user_id,
                "name": "domain",
                "pathname": "/some_path/domain.csv",
            }
        response = self.client.post("/domains",
            data=json.dumps({"domain": payload}),
            content_type="application/json")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 201, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("domain" in data)

        domain = data["domain"]

        self.assertTrue("id" not in domain)

        self.assertTrue("posted_at" in domain)

        self.assertTrue("name" in domain)
        self.assertEqual(domain["name"], "domain")

        self.assertTrue("pathname" in domain)
        self.assertEqual(domain["pathname"], "/some_path/domain.csv")

        self.assertTrue("_links" in domain)

        links = domain["_links"]

        self.assertTrue("self" in links)
        self.assertTrue("collection" in links)

        self.do_test_get_domains_by_user(user_id, 1)


    def test_post_bad_request(self):
        response = self.client.post("/domains")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 400, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


    def test_post_unprocessable_entity(self):
        payload = ""
        response = self.client.post("/domains",
            data=json.dumps({"domain": payload}),
            content_type="application/json")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 422, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


if __name__ == "__main__":
    unittest.main()
