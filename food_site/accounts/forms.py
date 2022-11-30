from django import forms
from .models import User, UserProfile
from .validators import allow_only_images_validators

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email','phone_number', 'password']
    
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password!= confirm_password:
            raise forms.ValidationError('Passwords do not match')


class UserProfileForm(forms.ModelForm):
    
    address=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'start typing ..', 'required':'required'}))
    
    # css style for input fields
    profile_picture = forms.FileField(widget = forms.FileInput(attrs={'class': 'btn btn-info'}),validators=[allow_only_images_validators])
    cover_photo = forms.FileField(widget = forms.FileInput(attrs={'class': 'btn btn-info'}),validators=[allow_only_images_validators])
    
    #one method to do readonly
    #latitude = forms.CharField(widget = forms.TextInput(attrs={'readonly': 'readonly'}))
    #longitude = forms.CharField(widget = forms.TextInput(attrs={'readonly': 'readonly'}))
    
    
    class Meta:
        model=UserProfile
        fields= ['profile_picture','cover_photo','address','country','state','city','pin_code','latitude','latitude','longitude']
        
    #other method to do readonly
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field  in self.fields:
            if field == 'latitude' and field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'
                
            
        