from django.core.exceptions import ValidationError
import os 

def allow_only_images_validators(value):
    ext = os.path.splitext(value.name)[1] #cover_photo.jpg
    print(ext)
    valid_extensions = [".jpg", ".png", ".jpeg"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("unsupported file extensions. Allowed extensions are : "+str(valid_extensions))
    
    
    
    