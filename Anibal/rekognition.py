import botocore
import boto3
from datetime import datetime

class text_detector():
    def __init__(self, local):
        self.client = boto3.client('rekognition')
        self.confidence = 97
        self.log = "log_anibal.log"
        self.local = local

    def write_log(self, test_id, line, p1, p2):
        with open(self.log, 'a') as file:
            file.write("{}: running test {}\n".format(datetime.now(),test_id))
            file.write("inputs: {}, {}\n".format(p1,p2))
            file.write("{}\n".format(line))

    def normalize_text(self, detections):
        #Vuelve las detecciones de texto a minusculas y separa las cadenas con espacios
        text_list = []
        for detection in detections:
            if detection['Type'] == 'LINE' or detection['Confidence'] < self.confidence:
                continue
            lword = detection['DetectedText'].lower()
            if lword in text_list:
                continue
            text_list.append(lword)
        return text_list

    def detect_text(self, test_id, bucket, photo):
        try:
            if self.local:
                photo_bytes = open(photo,'rb')
                response = self.client.detect_text(Image={'Bytes':photo_bytes.read()})
                photo_bytes.close()
            else:
                response=self.client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
            textDetections=response['TextDetections']
            return textDetections
        except botocore.exceptions.ClientError as e:
            self.write_log(test_id,"Exception:{}".format(e.response['Error']['Message']), photo, "")
            return "ERROR"
        
    
    def compare_text(self, test_id, control_text, test_text, p1, p2):
        ctrl_text_copy = control_text
        for word in test_text:
            if word in ctrl_text_copy:
                ctrl_text_copy.remove(word)
        if not ctrl_text_copy:
            self.write_log(test_id,"Success", p1, p2)
            return True
        self.write_log(test_id,"Fail", p1, p2)
        return False

def main(test_id, bucket, control_photo, test_photo, isLocal):
    bucket=bucket
    control_photo = control_photo
    test_photo = test_photo
    detector = text_detector(isLocal)
    control_detections = detector.detect_text(test_id, bucket, control_photo)
    if control_detections == "ERROR":
        print("ERROR")
        return
    test_detections = detector.detect_text(test_id, bucket, test_photo)
    if test_detections == "ERROR":
        print("ERROR")
        return
    normalized_control_text = detector.normalize_text(control_detections)
    normalized_test_text = detector.normalize_text(test_detections)
    print(normalized_control_text)
    print(normalized_test_text)
    if detector.compare_text(test_id,normalized_control_text, normalized_test_text,control_photo,test_photo):
        print("Exito")
    else:
        print("Fallo")

#if __name__ == "__main__":
    #main('111', "pruebasdesoftware", "monday.png", "monday.png", True)