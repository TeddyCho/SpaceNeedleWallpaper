from PIL import Image
import boto3
from botocore.client import Config

def stitchStills(aFolder='morning'):
    tempFile = "/tmp/" + aFolder + ".jpg"
    tempFile_WP = "/tmp/" + aFolder + "_wp.jpg"
    
    ACCESS_KEY_ID = ''
    ACCESS_SECRET_KEY = ''
    BUCKET_NAME='spaceneedlewebcamslices'
    BUCKET_NAME_WP='spaceneedlewebcamwallpaper'
    KEY = aFolder + "/" + str(6) + ".jpg"
    KEY_WP = aFolder + ".jpg"
    
    s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        config=Config(signature_version='s3v4')
    )

    for i in range(6,10):
        s3.Bucket(BUCKET_NAME).download_file(aFolder + "/" + str(i) + ".jpg", '/tmp/slice_' + str(i) + '.jpg')
    
    stills = [Image.open('/tmp/slice_' + str(i) + '.jpg') for i in range(6,10)]
    widths, heights = zip(*(s.size for s in stills))
    total_width= sum(widths)
    max_height = max(heights)
    fullStill = Image.new('RGB', (total_width, max_height))
    
    x_offset = 0
    for s in stills:
        fullStill.paste(s, (x_offset, 0))
        x_offset += s.size[0]
    fullStill.save(tempFile_WP)
    s3.Bucket(BUCKET_NAME_WP).upload_file(tempFile_WP, KEY_WP, ExtraArgs={'ACL':'public-read'})

def lambda_handler(event, context):
    stitchStills('morning')
    stitchStills('timestitch')
