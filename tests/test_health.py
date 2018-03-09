from tests.test_base import BasicTestCase

class TestHealth(BasicTestCase):
    def test_health(self):
        response = self.client.get(self.url_for('health'))
        self.assertEqual(response.status_code,300)
        # self.assertTrue(response.get_data(as_text=True))

    def test_health1(self):
        '''

        :return:
        '''
        response = self.client.get(self.url_for('health'))
        self.assertEqual(response.status_code,200)
        # self.assertTrue(response.get_data(as_text=True))