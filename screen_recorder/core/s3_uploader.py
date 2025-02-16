import os
import boto3
from botocore.config import Config

class S3Uploader:
    """Handles S3 upload functionality"""
    
    def __init__(self):
        self.s3_config = Config(
            region_name='us-east-2',
            signature_version='s3v4',
            retries={'max_attempts': 3}
        )
        
        self.s3_client = self._create_s3_client()
        self.bucket_name = "ghaymah-course-bucket"

    def _create_s3_client(self):
        """Create and configure S3 client"""
        return boto3.client(
            's3',
            config=self.s3_config,
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )

    def upload_file(self, file_path):
        """Upload file to S3 and return presigned URL"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            s3_key = f"lasheen-team/recording/{os.path.basename(file_path)}"
            self._upload_with_progress(file_path, s3_key)
            return self._generate_presigned_url(s3_key)
        except Exception as e:
            raise Exception(f"S3 upload failed: {str(e)}")

    def _upload_with_progress(self, file_path, s3_key):
        """Upload file with progress tracking"""
        file_size = os.path.getsize(file_path)
        with open(file_path, "rb") as f:
            self.s3_client.upload_fileobj(
                f,
                self.bucket_name,
                s3_key,
                ExtraArgs={'ServerSideEncryption': 'AES256'},
                Callback=lambda bytes_transferred: print(
                    f"Upload progress: {bytes_transferred/file_size*100:.1f}%"
                )
            )

    def _generate_presigned_url(self, s3_key):
        """Generate presigned URL for uploaded file"""
        return self.s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': self.bucket_name,
                'Key': s3_key
            },
            ExpiresIn=120
        ) 