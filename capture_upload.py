from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from cloudinary.api import delete_resources_by_tag, resources_by_tag
import picamera
import time
import sys
import os

DEFAULT_TAG = "raspberry_pi_capture"


def dump_response(response):
    print("Upload response:")
    for key in sorted(response.keys()):
        print("  %s: %s" % (key, response[key]))


def upload_files(public_id):
    print("--- Upload a local file")
    response = upload("upload.jpg", tags=DEFAULT_TAG, public_id=public_id + "!")
    self.dump_response(response)
    url, options = cloudinary_url(response['public_id'],
                                  format=response['format'],
                                  width=200,
                                  height=150,
                                  crop="fill"
                                  )
    print("Fill 200x150 url: " + url)
    print("")


def cleanup_cloudinary():
    response = resources_by_tag(DEFAULT_TAG)
    resources = response.get('resources', [])
    if not resources:
        print("No images found")
        return
    print("Deleting {0:d} images...".format(len(resources)))
    delete_resources_by_tag(DEFAULT_TAG)
    print("Done!")
    pass


def capture_image(public_id):
    print ("Capturing image, say cheese!")
    camera = picamera.PiCamera()
    camera.capture('upload.jpg')
    time.sleep(1)
    camera.close()

    if len(sys.argv) > 1:
        if sys.argv[1] == 'upload':
            upload_files(public_id)
        if sys.argv[1] == 'cleanup':
            cleanup_cloudinary()
    else:
        print("--- Uploading files and then cleaning up")
        print("    you can only one instead by passing 'upload' or 'cleanup' as an argument")
        print("")
        upload_files(public_id)
        os.remove("upload.jpg")

if __name__ == '__main__':
    capture_image(public_id='sample_capture')

