from django import forms
from .models import UserData
from .models import challengeData
from .models import detail
from .models import detailResponse
#from .models import Post
#from django.contrib.auth.models import User
class userForm(forms.ModelForm):
	class Meta:
		model = UserData
		fields = ['username','password','email']

class challengeForm(forms.ModelForm):
	class Meta:
		model = challengeData
		fields = ['urlnum','username','title','detail','stTime','endTime','mancount','permission']

class detailForm(forms.ModelForm):
	class Meta:
		model = detail
		fields = ['urlnumber','username','title','detail','startTime','endTime','mancount','video','isFinish']

class detailResponseForm(forms.ModelForm):
	class Meta:
		model = detailResponse
		fields = ['urlnumber','username','postTime','response']
		
#class AddPost(forms.ModelForm):
#	class Meta:
#		model = Post
#		fields = ['text',]