import unittest
from unittest.mock import patch

from prediction_model import predict_message_mood


class TestPredictMessageMood(unittest.TestCase):

    @patch('prediction_model.SomeModel.predict')
    def test_mood_no_borders(self, mock_predict):
        mock_predict.side_effect = [0.6, 0.9, 0.2]
        self.assertEqual(predict_message_mood('Чапаев и Пустота'), 'норм')
        self.assertEqual(predict_message_mood('Круть'), 'отл')
        self.assertEqual(predict_message_mood('Война и Мир'), 'неуд')

    @patch('prediction_model.SomeModel.predict')
    def test_mood_with_borders(self, mock_predict):
        mock_predict.side_effect = [0.99, 0.5, 0.2]
        self.assertEqual(predict_message_mood('Какой-то', 0.8, 0.9), 'отл')
        self.assertEqual(predict_message_mood('Текст', 0.4, 0.6), 'норм')
        self.assertEqual(predict_message_mood('Вот', 0.7, 0.95), 'неуд')

    def test_invalid_borders(self):
        with self.assertRaises(ValueError) as err:
            predict_message_mood('Неправильные границы', 0.7, 0.6)
        self.assertEqual(str(err.exception), 'Incorrect thresholds')

        with self.assertRaises(ValueError) as err:
            predict_message_mood('Неправильная граница слева', -1, 0.6)
        self.assertEqual(str(err.exception), 'Incorrect thresholds')

        with self.assertRaises(ValueError) as err:
            predict_message_mood('Неправильная граница cправа', 0.4, 2)
        self.assertEqual(str(err.exception), 'Incorrect thresholds')

    @patch('prediction_model.SomeModel.predict')
    def test_invalid_prediction(self, mock_predict):
        mock_predict.side_effect = [-10, 10, None]
        with self.assertRaises(ValueError) as err:
            predict_message_mood('Предсказание меньше нуля')
        self.assertEqual(str(err.exception), 'Prediction not between 0 and 1')

        with self.assertRaises(ValueError) as err:
            predict_message_mood('Предсказание меньше нуля')
        self.assertEqual(str(err.exception), 'Prediction not between 0 and 1')

        with self.assertRaises(ValueError) as err:
            predict_message_mood('Модель ничего не вернула')
        self.assertEqual(str(err.exception), 'No prediction')


if __name__ == '__main__':
    unittest.main()
