from flask import jsonify, request
from werkzeug.utils import secure_filename
from supabase import create_client
from dotenv import load_dotenv
import uuid, os

class User:
    def __init__(self):
        load_dotenv()
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        self.supabase = create_client(url, key)
        self.BUCKET_NAME = "photos"
        self.public_url = ""

    def add_image(self,file,user) :
        BUCKET_NAME = "photos"
        load_dotenv()
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        supabase = create_client(url, key)
        ext = secure_filename(file.filename).rsplit('.', 1)[1].lower()
        unique_name = f"{uuid.uuid4().hex}.{ext}"
        
        # Read file contents
        contents = file.read()
        # Upload to Supabase Storage
        supabase.storage.from_(BUCKET_NAME).upload(unique_name, contents)

        # Get public URL (string)
        self.public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(unique_name)

        # Insert record into database
        if not user.picture :
            print('add')
            supabase.table(BUCKET_NAME).\
                insert({"title": "IMG_"+ str(user.id), "image_url": self.public_url}).execute()
        else:
            print('update')
            supabase.table(BUCKET_NAME).\
            update({"title": "IMG_"+ str(user.id) , "image_url": self.public_url}).eq("id", user.id).execute()
    
    def get_public_url(self):
        return self.public_url