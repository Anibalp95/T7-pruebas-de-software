import logging
import pathlib
import typing

import boto3

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


client = boto3.client('rekognition')


def process(image_byes: bytes) -> typing.Mapping:
    try:
        response = client.detect_text(Image=dict(Bytes=image_byes))
    except Exception as ex:
        logger.exception(ex)
    else:
        return response['TextDetections']


def clean_text(data: typing.Collection[typing.Mapping], confidence: float = 97) -> typing.Iterable[str]:
    for datum in data:
        if datum['Type'] != 'WORD' or datum['Confidence'] < confidence:
            continue
        detected_text = datum['DetectedText']
        yield detected_text.lower().strip()


def detect_words(image_path: pathlib.Path) -> typing.Set[str]:
    image_bytes = image_path.read_bytes()
    response = process(image_byes=image_bytes)
    return set([x for x in clean_text(response)])


def main():
    control_image_path = pathlib.Path('control.png')
    test_image_path = pathlib.Path('test.jpg')

    control_words = detect_words(control_image_path)
    logger.debug(f'control words are: {control_words}')

    test_words = detect_words(test_image_path)
    logger.debug(f'test words are: {test_words}')

    if control_words.issubset(test_words):
        logger.debug('PASS')
    else:
        logger.debug('FAIL')


if __name__ == '__main__':
    main()