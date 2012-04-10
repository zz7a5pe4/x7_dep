# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack, LLC
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Tests a Glance API server which uses an S3 backend by default

This test requires that a real S3 account is available. It looks
in a file specified in the GLANCE_TEST_S3_CONF environ variable
for the credentials to use.

Note that this test clears the entire bucket from the S3 account
for use by the test case, so make sure you supply credentials for
test accounts only.

If a connection cannot be established, all the test cases are
skipped.
"""

import hashlib
import json
import tempfile
import unittest

import httplib2

from glance.common import crypt
from glance.common import utils
from glance.tests.functional import test_api
from glance.tests.utils import (execute,
                                skip_if_disabled,
                                requires,
                                minimal_headers)
from glance.tests.functional.store_utils import (setup_s3,
                                                 teardown_s3,
                                                 get_s3_uri,
                                                 setup_swift,
                                                 teardown_swift,
                                                 get_swift_uri,
                                                 setup_http,
                                                 teardown_http,
                                                 get_http_uri)


FIVE_KB = 5 * 1024


class TestS3(test_api.TestApi):

    """Functional tests for the S3 backend"""

    def setUp(self):
        """
        Test a connection to an S3 store using the credentials
        found in the environs or /tests/functional/test_s3.conf, if found.
        If the connection fails, mark all tests to skip.
        """
        if self.disabled:
            return

        setup_s3(self)

        self.default_store = 's3'

        super(TestS3, self).setUp()

    def tearDown(self):
        teardown_s3(self)
        super(TestS3, self).tearDown()

    @skip_if_disabled
    def test_remote_image(self):
        """Verify an image added using a 'Location' header can be retrieved"""
        self.cleanup()
        self.start_servers(**self.__dict__.copy())

        # 1. POST /images with public image named Image1
        image_data = "*" * FIVE_KB
        headers = minimal_headers('Image1')
        path = "http://%s:%d/v1/images" % ("0.0.0.0", self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'POST', headers=headers,
                                         body=image_data)
        self.assertEqual(response.status, 201)
        data = json.loads(content)
        self.assertEqual(data['image']['checksum'],
                         hashlib.md5(image_data).hexdigest())
        self.assertEqual(data['image']['size'], FIVE_KB)

        image_id1 = data['image']['id']

        # 2. GET first image
        # Verify all information on image we just added is correct
        path = "http://%s:%d/v1/images/%s"
        args = ("0.0.0.0", self.api_port, image_id1)

        http = httplib2.Http()
        response, content = http.request(path % args, 'GET')
        self.assertEqual(response.status, 200)
        self.assertEqual(response['content-length'], str(FIVE_KB))
        self.assertEqual(content, "*" * FIVE_KB)

        # 3. GET first image from registry in order to find S3 location
        path = "http://%s:%d/images/%s"
        args = ("0.0.0.0", self.registry_port, image_id1)

        http = httplib2.Http()
        response, content = http.request(path % args, 'GET')
        if hasattr(self, 'metadata_encryption_key'):
            key = self.metadata_encryption_key
        else:
            key = self.api_server.metadata_encryption_key
        loc = json.loads(content)['image']['location']
        s3_store_location = crypt.urlsafe_decrypt(key, loc)

        # 4. POST /images using location generated by Image1
        image_id2 = utils.generate_uuid()
        image_data = "*" * FIVE_KB
        headers = minimal_headers('Image2')
        headers['X-Image-Meta-Id'] = image_id2
        headers['X-Image-Meta-Location'] = s3_store_location
        path = "http://%s:%d/v1/images" % ("0.0.0.0", self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'POST', headers=headers)
        self.assertEqual(response.status, 201)
        # ensure data is refreshed, previously the size assertion
        # applied to the metadata returned from the previous GET
        data = json.loads(content)
        self.assertEqual(data['image']['size'], FIVE_KB)
        # checksum is not set for a remote image, as the image data
        # is not yet retrieved
        self.assertEqual(data['image']['checksum'], None)

        # 5. GET second image and make sure it can stream the image
        path = "http://%s:%d/v1/images/%s"
        args = ("0.0.0.0", self.api_port, image_id2)

        http = httplib2.Http()
        response, content = http.request(path % args, 'GET')
        self.assertEqual(response.status, 200)
        self.assertEqual(response['content-length'], str(FIVE_KB))
        self.assertEqual(content, "*" * FIVE_KB)

        # 6. DELETE first and second images
        path = "http://%s:%d/v1/images/%s"
        args = ("0.0.0.0", self.api_port, image_id1)

        http = httplib2.Http()
        http.request(path % args, 'DELETE')

        path = "http://%s:%d/v1/images/%s"
        args = ("0.0.0.0", self.api_port, image_id2)

        http = httplib2.Http()
        http.request(path % args, 'DELETE')

        self.stop_servers()

    def _do_test_copy_from(self, from_store, get_uri):
        """
        Ensure we can copy from an external image in from_store.
        """
        self.cleanup()

        self.start_servers(**self.__dict__.copy())

        api_port = self.api_port
        registry_port = self.registry_port

        # POST /images with public image to be stored in from_store,
        # to stand in for the 'external' image
        image_data = "*" * FIVE_KB
        headers = minimal_headers('external')
        headers['X-Image-Meta-Store'] = from_store
        path = "http://%s:%d/v1/images" % ("0.0.0.0", self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'POST', headers=headers,
                                         body=image_data)
        self.assertEqual(response.status, 201, content)
        data = json.loads(content)

        original_image_id = data['image']['id']

        copy_from = get_uri(self, original_image_id)

        # POST /images with public image copied from_store (to Swift)
        headers = {'X-Image-Meta-Name': 'copied',
                   'X-Image-Meta-Is-Public': 'True',
                   'X-Image-Meta-disk_format': 'raw',
                   'X-Image-Meta-container_format': 'ovf',
                   'X-Glance-API-Copy-From': copy_from}
        path = "http://%s:%d/v1/images" % ("0.0.0.0", self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'POST', headers=headers)
        self.assertEqual(response.status, 201, content)
        data = json.loads(content)

        copy_image_id = data['image']['id']
        self.assertNotEqual(copy_image_id, original_image_id)

        # GET image and make sure image content is as expected
        path = "http://%s:%d/v1/images/%s" % ("0.0.0.0", self.api_port,
                                              copy_image_id)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(response.status, 200)
        self.assertEqual(response['content-length'], str(FIVE_KB))

        self.assertEqual(content, "*" * FIVE_KB)
        self.assertEqual(hashlib.md5(content).hexdigest(),
                         hashlib.md5("*" * FIVE_KB).hexdigest())
        self.assertEqual(data['image']['size'], FIVE_KB)
        self.assertEqual(data['image']['name'], "copied")

        # DELETE original image
        path = "http://%s:%d/v1/images/%s" % ("0.0.0.0", self.api_port,
                                              original_image_id)
        http = httplib2.Http()
        response, content = http.request(path, 'DELETE')
        self.assertEqual(response.status, 200)

        # GET image again to make sure the existence of the original
        # image in from_store is not depended on
        path = "http://%s:%d/v1/images/%s" % ("0.0.0.0", self.api_port,
                                              copy_image_id)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(response.status, 200)
        self.assertEqual(response['content-length'], str(FIVE_KB))

        self.assertEqual(content, "*" * FIVE_KB)
        self.assertEqual(hashlib.md5(content).hexdigest(),
                         hashlib.md5("*" * FIVE_KB).hexdigest())
        self.assertEqual(data['image']['size'], FIVE_KB)
        self.assertEqual(data['image']['name'], "copied")

        # DELETE copied image
        path = "http://%s:%d/v1/images/%s" % ("0.0.0.0", self.api_port,
                                              copy_image_id)
        http = httplib2.Http()
        response, content = http.request(path, 'DELETE')
        self.assertEqual(response.status, 200)

        self.stop_servers()

    @skip_if_disabled
    def test_copy_from_s3(self):
        """
        Ensure we can copy from an external image in S3.
        """
        self._do_test_copy_from('s3', get_s3_uri)

    @requires(setup_swift, teardown_swift)
    @skip_if_disabled
    def test_copy_from_swift(self):
        """
        Ensure we can copy from an external image in Swift.
        """
        self._do_test_copy_from('swift', get_swift_uri)

    @requires(setup_http, teardown_http)
    @skip_if_disabled
    def test_copy_from_http(self):
        """
        Ensure we can copy from an external image in HTTP.
        """
        self.cleanup()

        self.start_servers(**self.__dict__.copy())

        api_port = self.api_port
        registry_port = self.registry_port

        copy_from = get_http_uri(self, 'foobar')

        # POST /images with public image copied HTTP (to S3)
        headers = {'X-Image-Meta-Name': 'copied',
                   'X-Image-Meta-disk_format': 'raw',
                   'X-Image-Meta-container_format': 'ovf',
                   'X-Image-Meta-Is-Public': 'True',
                   'X-Glance-API-Copy-From': copy_from}
        path = "http://%s:%d/v1/images" % ("0.0.0.0", self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'POST', headers=headers)
        self.assertEqual(response.status, 201, content)
        data = json.loads(content)

        copy_image_id = data['image']['id']

        # GET image and make sure image content is as expected
        path = "http://%s:%d/v1/images/%s" % ("0.0.0.0", self.api_port,
                                              copy_image_id)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(response.status, 200)
        self.assertEqual(response['content-length'], str(FIVE_KB))

        self.assertEqual(content, "*" * FIVE_KB)
        self.assertEqual(hashlib.md5(content).hexdigest(),
                         hashlib.md5("*" * FIVE_KB).hexdigest())
        self.assertEqual(data['image']['size'], FIVE_KB)
        self.assertEqual(data['image']['name'], "copied")

        # DELETE copied image
        path = "http://%s:%d/v1/images/%s" % ("0.0.0.0", self.api_port,
                                              copy_image_id)
        http = httplib2.Http()
        response, content = http.request(path, 'DELETE')
        self.assertEqual(response.status, 200)

        self.stop_servers()
