from django.test import TestCase
from django.shortcuts import reverse
from unittest.mock import patch, call
from accounts.models import Token
from django.conf import settings


class SendLoginEmailViewTest(TestCase):
    def test_redirects_to_home_page(self):
        response = self.client.post(
            reverse("accounts:send_login_email"), data={"email": "edith@example"}
        )
        self.assertRedirects(response, reverse("home"))

    @patch("accounts.views.send_mail")
    def test_sends_mail_to_address_from_post(self, mock_send_mail):

        for email in ["edith@example.com", "georg@example.com"]:
            self.client.post(
                reverse("accounts:send_login_email"), data={"email": email}
            )

            self.assertTrue(mock_send_mail.called)
            (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
            correct_subject = (
                "Dein Login Link für 'Programmieren für Sozialwissenschaftler*innen'"
            )
            self.assertEqual(subject, correct_subject)
            self.assertEqual(from_email, settings.EMAIL_HOST_USER)
            self.assertEqual(to_list, [email])

    def test_adds_success_message(self):
        response = self.client.post(
            reverse("accounts:send_login_email"),
            data={"email": "edith@example.com"},
            follow=True,
        )
        message = list(response.context["messages"])[0]
        self.assertEqual(
            message.message,
            "Dein Login Link ist soeben in deinem Email Postfach angekommen.",
        )
        self.assertEqual(message.tags, "success")

    @patch("accounts.views.send_mail")
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        self.client.post(
            reverse("accounts:send_login_email"), data={"email": "edith@example"}
        )
        token = Token.objects.first()
        expected_url = f"http://testserver/accounts/login?token={token.uid}"
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)

    def test_creates_token_associated_with_email(self):
        self.client.post(
            reverse("accounts:send_login_email"), data={"email": "edith@example.com"}
        )
        token = Token.objects.first()
        self.assertEqual(token.email, "edith@example.com")


@patch("accounts.views.auth")
class LoginViewTest(TestCase):
    def test_redirects_to_home_page(self, mock_auth):
        response = self.client.get("/accounts/login?token=abcd123")
        self.assertRedirects(response, reverse("home"))

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        for token in ["abcd123", "efgh456"]:
            self.client.get(f"/accounts/login?token={token}")
            self.assertEqual(mock_auth.authenticate.call_args, call(uid=token))

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        for token in ["abcd123", "efgh456"]:
            response = self.client.get(f"/accounts/login?token={token}")
            self.assertEqual(
                mock_auth.login.call_args,
                call(response.wsgi_request, mock_auth.authenticate.return_value),
            )

    def test_does_not_login_if_user_is_not_autenticated(self, mock_auth):
        for token in ["abcd123", "efgh456"]:
            mock_auth.authenticate.return_value = None
            self.client.get(f'/accounts/login?token={token}')
            self.assertEqual(mock_auth.login.called, False)
