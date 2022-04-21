import unittest
import Git_Fresh

class SimpleTest(unittest.TestCase):

    def test_frehdesk_user_info_email(self):
        github_user_info = {
            'login': 'test',
            'id': '123',
            'email': 'null',
            'twitter_username': 'null'
        }
        user_info = Git_Fresh.create_freshdesk_user_info(github_user_info)
        self.assertEqual(user_info['email'], 'N/A')

    def test_frehdesk_user_info_twitter_username(self):
        github_user_info = {
            'login': 'user',
            'id': '113424',
            'email': 'user@abv.bg',
            'twitter_username': 'null'
        }
        user_info = Git_Fresh.create_freshdesk_user_info(github_user_info)
        self.assertEqual(user_info['twitter_id'], 'N/A')
    
    def test_not_authenticated_github_user(self):
        github_token = 'some_wrong_token'
        github_user_info = Git_Fresh.get_authenticated_github_user('https://api.github.com/user', github_token)
        self.assertEqual(github_user_info, None)

    def test_freshdesk_user_existance(self):
        freshdesk_subdomain = 'test'
        freshdesk_token = 'some_wrong_token'
        freshdesk_user_info = {
            'name': 'test',
            'unique_external_id': '123',
            'email': 'null',
            'twitter_id': 'null'
        }
        self.assertEqual(Git_Fresh.check_if_freshdesk_user_exists(freshdesk_subdomain, freshdesk_token, freshdesk_user_info), -3)


if __name__ == '__main__':
    unittest.main()