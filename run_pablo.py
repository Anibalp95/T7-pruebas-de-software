import pathlib
import logging
import Pablo.rekognition


logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s", "%Y-%m-%d %H:%M:%S")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def main():
    testcases_dir_path = pathlib.Path('TestCases')
    for testcase_path in testcases_dir_path.iterdir():
        logger.info(f'Running test case {testcase_path.name}')
        control_image_path = testcase_path / 'control.jpg'
        test_image_path = testcase_path / 'test.jpg'
        try:
            Pablo.rekognition.main(control_image_path=control_image_path,
                                   test_image_path=test_image_path,
                                   confidence=97)
        except Exception as ex:
            logger.exception(ex)


if __name__ == '__main__':
    main()
