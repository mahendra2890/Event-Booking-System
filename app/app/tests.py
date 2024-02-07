from django.test import TestCase
from unittest.mock import patch
from core.tasks import send_booking_confirmation_email, send_event_update_notification


class TestCeleryTasks(TestCase):

    @patch('core.tasks.send_booking_confirmation_email')
    def test_send_booking_confirmation_email_task(self, mock_task):
        # Call the task with sample booking ID
        task_id = send_booking_confirmation_email.delay(123, "testing")

        # result = AsyncResult(task_id)

        # mock_task.assert_called_once_with(123)

    @patch('core.tasks.send_event_update_notification')
    def test_send_event_update_notification_task(self, mock_task):
        # Call the task with sample event ID
        send_event_update_notification.delay(456, "testing")

        # Assert that the task was called with the correct argument
        # mock_task.assert_called_once_with(456)
