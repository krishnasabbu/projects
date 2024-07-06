import unittest
from io import BytesIO
from deepfakedetection import app


class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    # def test_health_route(self):
    #     response = self.app.get('/health')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data.decode('utf-8'), 'It is alive!\n')

    def test_upload_route_no_file(self):
        response = self.app.post('/upload')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"No file part", response.data)

    def test_upload_route_invalid_file_format(self):
        data = {'file': (BytesIO(b'test'), 'test.txt')}
        response = self.app.post('/upload', content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Invalid file format", response.data)

    def test_upload_route_valid_file_wav(self):
        test_audio_path = '../audio/human/Speaker_0000_00000.wav'  # Path to a valid audio file
        with open(test_audio_path, 'rb') as audio_file:
            data = {'file': (audio_file, 'test_audio.wav')}
            response = self.app.post('/upload', content_type='multipart/form-data', data=data)
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertEqual(json_response["status"], "success")
            self.assertIn(b"detectedVoice", response.data)
            self.assertIn(b"voiceType", response.data)
            self.assertIn(b"confidenceScore", response.data)
            self.assertIn(b"aiProbability", response.data)
            self.assertIn(b"humanProbability", response.data)
            self.assertIn(b"additionalInfo", response.data)
            self.assertIn(b"emotionalTone", response.data)
            self.assertIn(b"backgroundNoiseLevel", response.data)
            self.assertIn(b"responseTime", response.data)

    def test_upload_route_valid_file_mp3(self):
        test_audio_path = '../audio/human/human_voice_Script2.mp3'  # Path to a valid audio file
        with open(test_audio_path, 'rb') as audio_file:
            data = {'file': (audio_file, 'test_audio.wav')}
            response = self.app.post('/upload', content_type='multipart/form-data', data=data)
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertEqual(json_response["status"], "success")
            self.assertIn(b"detectedVoice", response.data)
            self.assertIn(b"voiceType", response.data)
            self.assertIn(b"confidenceScore", response.data)
            self.assertIn(b"aiProbability", response.data)
            self.assertIn(b"humanProbability", response.data)
            self.assertIn(b"additionalInfo", response.data)
            self.assertIn(b"emotionalTone", response.data)
            self.assertIn(b"backgroundNoiseLevel", response.data)
            self.assertIn(b"responseTime", response.data)

    def test_upload_route_valid_file_ai_mp3(self):
        test_audio_path = '../audio/ai/AI_Voice_Script1.mp3'  # Path to a valid audio file
        with open(test_audio_path, 'rb') as audio_file:
            data = {'file': (audio_file, 'test_audio.wav')}
            response = self.app.post('/upload', content_type='multipart/form-data', data=data)
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertEqual(json_response["status"], "success")
            self.assertIn(b"detectedVoice", response.data)
            self.assertIn(b"voiceType", response.data)
            self.assertIn(b"confidenceScore", response.data)
            self.assertIn(b"aiProbability", response.data)
            self.assertIn(b"humanProbability", response.data)
            self.assertIn(b"additionalInfo", response.data)
            self.assertIn(b"emotionalTone", response.data)
            self.assertIn(b"backgroundNoiseLevel", response.data)
            self.assertIn(b"responseTime", response.data)

    def test_upload_route_invalid_file_mp3(self):
        test_audio_path = '../audio/human/human_voice_Script2.mp3'  # Path to a valid audio file
        with open(test_audio_path, 'rb') as audio_file:
            data = {'file': ''}
            response = self.app.post('/upload', content_type='multipart/form-data', data=data)
            self.assertEqual(response.status_code, 400)

# if __name__ == '__main__':
#     unittest.main()
