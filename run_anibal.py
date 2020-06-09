import pathlib
import Anibal.rekognition

testcases_dir_path = pathlib.Path('TestCases')
for testcase_path in testcases_dir_path.iterdir():
    control_image_path = testcase_path / 'control.jpg'
    test_image_path = testcase_path / 'test.jpg'
    Anibal.rekognition.main(testcase_path.name, "pruebasdesoftware", control_image_path, test_image_path, True)