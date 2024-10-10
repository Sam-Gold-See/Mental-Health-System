from app.core.image.Emotion import Emotion
from PIL import ImageFile

class Image:
    def __init__(self):
        self.emotion = Emotion()

    def get_emotion(self, image: ImageFile.ImageFile):
        return self.emotion.Get_emotion_by_picture(image)

ImageController = Image()