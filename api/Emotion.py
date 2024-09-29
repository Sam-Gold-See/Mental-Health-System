from deepface import DeepFace
import cv2

class Emotion:
    def __init__(self, analysis_interval=30):
        '''
        :param analysis_interval: 默认每30帧分析一次情绪
        '''
        self.analysis_interval = analysis_interval

    def Get_emotion_by_picture(self, path):
        '''
        函数通过传入的图片返回识别出来的表情
        :param path: 图片的地址
        :return: 识别出来的表情
        '''
        img = cv2.imread(path)
        emotion_result = DeepFace.analyze(img, actions=['emotion'])

        dominant_emotion = emotion_result[0]['dominant_emotion']
        return dominant_emotion

    def Get_emotion_by_video(self, path):
        '''
        函数通过传入的视频逐帧输出识别出来的表情
        :param path: 视频的地址
        '''
        cap = cv2.VideoCapture(path)
        frame_count = 0
        dominant_emotion = None

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # 每隔指定的帧数进行情绪分析
            if frame_count % self.analysis_interval == 0:
                emotion_result = DeepFace.analyze(frame, actions=['emotion'])
                dominant_emotion = emotion_result[0]['dominant_emotion']

            # 打印每隔间隔的情绪识别结果
            if dominant_emotion:
                print(f"Frame {frame_count}: {dominant_emotion}")

            # 显示视频帧
            cv2.imshow("emotion", frame)

            # 按下 q 键退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            frame_count += 1

        cap.release()
        cv2.destroyAllWindows()

    def check_camera_available(self, camera_index=0):
        '''
        检查对应索引的摄像头是否正常工作
        :param camera_index: 摄像头对应的索引，默认为0
        :return:
        '''
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            return False
        else:
            cap.release()
            return True

    def Get_emotion_by_camera(self, camera_index=0):
        '''
        函数通过摄像头逐帧输出识别出来的表情
        :param camera_index: 摄像头对应的索引，默认为0
        '''
        if self.check_camera_available(camera_index):
            cap = cv2.VideoCapture(camera_index)
            frame_count = 0
            dominant_emotion = None

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # 每隔指定的帧数进行情绪分析
                if frame_count % self.analysis_interval == 0:
                    emotion_result = DeepFace.analyze(frame, actions=['emotion'])
                    dominant_emotion = emotion_result[0]['dominant_emotion']

                # 打印每隔间隔的情绪识别结果
                if dominant_emotion:
                    print(f"Frame {frame_count}: {dominant_emotion}")

                # 显示视频帧
                cv2.imshow("emotion", frame)

                # 按下 q 键退出
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                frame_count += 1

            cap.release()
            cv2.destroyAllWindows()
        else:
            print("没有找到指定索引的摄像头")
