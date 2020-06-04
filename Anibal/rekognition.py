import botocore
import boto3
from datetime import datetime

class text_detector():
    def __init__(self, control_photo, test_photo):
        self.client = boto3.client('rekognition')
        self.confidence = 97
        self.control_photo = control_photo
        self.test_photo = test_photo
        self.log = "log.txt"

    def write_log(self, line):
        with open(self.log, 'a') as file:
            file.write("{}: {}, {}\n".format(datetime.now(),self.control_photo, self.test_photo))
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

    def detect_text(self, bucket, photo):
        try:
            response=self.client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
            textDetections=response['TextDetections']
            return textDetections
        except botocore.exceptions.ClientError as e:
            print(e)
            return 
        #print ('Detected text\n----------')
        #for text in textDetections:
        #        print ('Detected text:' + text['DetectedText'])
        #        print ('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
        #        print ('Id: {}'.format(text['Id']))
        #        if 'ParentId' in text:
        #            print ('Parent Id: {}'.format(text['ParentId']))
        #        print ('Type:' + text['Type'])
        #        print()
        
    
    def compare_text(self, control_text, test_text):
        ctrl_text_copy = control_text
        for word in test_text:
            if word in ctrl_text_copy:
                ctrl_text_copy.remove(word)
        if not ctrl_text_copy:
            self.write_log("Success")
            return True
        self.write_log("Fail")
        return False

def main():
    bucket='pruebasdesoftware'
    control_photo='monday.png'
    test_photo='monday.png'
    detector = text_detector(control_photo,test_photo)
    control_detections = detector.detect_text(bucket, control_photo)
    if not control_detections:
        print("Hubo un error")
        return
    test_detections = detector.detect_text(bucket, test_photo)
    if not test_detections:
        print("Hubo un error")
        return
    normalized_control_text = detector.normalize_text(control_detections)
    normalized_test_text = detector.normalize_text(test_detections)
    print(normalized_control_text)
    print(normalized_test_text)
    if detector.compare_text(normalized_control_text, normalized_test_text):
        print("Exito")
    else:
        print("Fallo")

if __name__ == "__main__":
    main()