import sys
from django.conf import settings
import sys, time
import hashlib
from uuid import uuid4
import os
from care.models import User, UserProfile
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext as _

class UploadFile(object):
	"""Upload file and write to DB AccessLog"""
	def __init__(self, request=False, key=False, location=False):
		super(UploadFile, self).__init__()
		self.request = request
		self.key = key
		self.location = location
		
		self.PATH = settings.MEDIA_ROOT + 'users/' +str(request.user.id)+ '/'
		self.LOCATION_PATH = 'users/' +str(request.user.id)+ '/'
 
	def upload(self, u_id):
		try:

			upload_obj = self.request.FILES[self.key]


			if not upload_obj:
				response_data = {
					'success': False,
					'message': (_(u"No image!")),
				}
				return HttpResponse(json.dumps(response_data), content_type = 'application/json')
			elif not upload_obj.name:
				sys.exit()
			else:
				#validate content type
				main, sub = upload_obj.content_type.split('/')
				if not (main == 'image' and sub.lower() in ['jpeg', 'pjpeg', 'png', 'jpg']):
					response_data = {
						'success': False,
						'message': (_(u'Please use a JPEG or PNG image.')),
					}
					return HttpResponse(json.dumps(response_data), content_type = 'application/json')
				if len(upload_obj) > (5 * 1024 * 1024):
					response_data = {
						'success': False,
						'message': (_(u'Image file too large')),
					}
					return HttpResponse(json.dumps(response_data), content_type = 'application/json')

				from django.core.files.images import get_image_dimensions
				w, h = get_image_dimensions(upload_obj)
				#validate dimensions
				mwidth = 250 
				mheight = 250
				print("Dimensions w="+w+"; h="+h+";")
				if (w >= h and (w < mwidth and h < mheight)) or (w < h and (h < mwidth and w < mheight)):
					response_data = {
						'success': False,
						'message': (_(u'Too low image size, please use bigger!')),
					}
					return HttpResponse(json.dumps(response_data), content_type = 'application/json')
				#portaint or landscape max size check
				if (w >= h and (w > mwidth*10 and h > mheight*10)) or (w < h and (h > mwidth*10 and w > mheight*10)):
					response_data = {
						'success': False,
						'message': (_(u'Too big image size! Please use smaller.')),
					}
					return HttpResponse(json.dumps(response_data), content_type = 'application/json')
		
			ext = upload_obj.name.split('.')[-1]
			# get filename
			filename = '{}.{}'.format(uuid4().hex, ext)

			module_dir = os.path.dirname(__file__)

			now = str(int(time.time()))
			hashPath = hashlib.md5(now).hexdigest()
			path = settings.MEDIA_ROOT + 'users/'+hashPath[:2]+'/'+hashPath[2:4]+'/'+hashPath+'/'
			self.PATH = path
			self.LOCATION_PATH = 'users/'+hashPath[:2]+'/'+hashPath[2:4]+'/'+hashPath+'/'

			file_path = os.path.join(module_dir, path+filename)

			print(file_path)

			if not os.path.exists(os.path.dirname(file_path)):
				os.makedirs(os.path.dirname(file_path))

			destination = open(file_path, 'wb')
	 
			for chunk in upload_obj.chunks():
				destination.write(chunk)
	 
			destination.close()
	 
			fid = uuid4()
			
			#    filename = upload_obj.name, 
			#    location = str(self.location),
			print(u_id)
			p_author = None
			try:
				p_author = UserProfile.objects.get(user=u_id)
				try:
					print("Delete "+settings.MEDIA_ROOT + p_author.user_picture)
					os.remove(settings.MEDIA_ROOT + p_author.original_picture)
					os.remove(settings.MEDIA_ROOT + p_author.user_picture)
					os.remove(settings.MEDIA_ROOT + p_author.user_thumbnail)
				except Exception, e:
					print("New user photo!")
				if p_author:
					p_author.original_picture = ''
					p_author.user_picture = ''
					p_author.user_thumbnail = ''
			except Exception, e:
				user = User.objects.get(pk=u_id)
				up = UserProfile.create(user)
				up.user = user
				up.save()
				p_author = UserProfile.objects.get(user=user)
			finally:
				print(self.LOCATION_PATH + filename)
				p_author.original_picture = self.LOCATION_PATH + filename
				p_author.save()

	 
			response_data = {
				'success': True,
				'message': '',
				'img_url': str('http://'+self.request.META['HTTP_HOST']+settings.MEDIA_URL + p_author.original_picture),
			}
				
			response = HttpResponse(json.dumps(response_data), content_type = 'application/json')
			return response
		except Exception, e:
			response_data = {
				'success': False,
				'message': _('Some error happened'),
			}
			return HttpResponse(json.dumps(response_data), content_type = 'application/json')
 
	def delete(self):
		upload_obj = Files.objects.get(fid=self.request.POST.get('fid'))
		filename = upload_obj.filename
		location = upload_obj.location
		upload_obj.delete()
 
		if location == 'upload':
			PATH = settings.UPLOADS_PATH
		elif location == 'installer':
			PATH = settings.INSTALLERS_PATH
 
		os.remove(PATH + filename)
 
		response_data = {
			'success': True,
		}
		
		response = HttpResponse(json.dumps(response_data), mimetype = 'application/json')
		return response