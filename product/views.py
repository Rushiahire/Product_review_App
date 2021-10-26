
from django.shortcuts import render,redirect
from django.views import View
from . import forms
import dbinfo
import gridfs
import string
import random
from bson.objectid import ObjectId
import base64
from django.contrib import messages



class NewProduct(View):
    def get(self,request):
        content = {
            'page_title': 'Add New Product',
            'new_product_form':forms.NewProductForm()
        }
        return render(request,'new_product.html',content)

    def get_random_string(self):
        length = 10
        collection = dbinfo.database['fs.files']
        chars = string.ascii_letters + '0123456789'
        while(True):
            file_name = ''.join(random.choices(chars,k = length))
            if file_name not in collection.find():
                break
        
        return file_name

    def post(self,request):
        product_name = request.POST['product_name']
        description = request.POST['description']
        price = request.POST['price']

        image = request.FILES['product_image']
        file_name,extension = image.name.split('.')
        fs = gridfs.GridFS(dbinfo.database)
        collection = dbinfo.database['product_info']
        uid = self.get_random_string()
        image_name = f'{uid}.{extension}'        
        file_id = fs.put(image,file_name = image_name)
        new_product = {
            'uid':uid,
            'product_name': product_name,
            'description': description,
            'price': price,
            'image_id' : file_id,
            'reviews' : []
            
        }
        collection.insert(new_product)
        messages.success(request,"New Product added")
        return redirect('/')


class ProductInfo(View):
    def get(self, request):
        collection = dbinfo.database['product_info']
        fs = gridfs.GridFS(dbinfo.database)
        uid = request.GET['uid']
        product_info = collection.find_one({'uid': uid})
        image_id = product_info['image_id'] 
        image_path = fs.get(ObjectId(image_id))
        
        content = {
            'page_title': 'Product Info',
            'product_info': product_info,
            'image_path': base64.b64encode(image_path.read()).decode('utf-8'),
            'review_form' : forms.NewReviewform(),
            'reviews' : product_info['reviews']
        }

        return render(request, 'product_info.html', content)

class NewReview(View):
    def post(self,request):
        uid = request.POST['uid']
        rating = request.POST['rating']
        feedback = request.POST['feedback']
        collection = dbinfo.database['product_info']
        product = collection.find_one({'uid':uid})
        old_data = product['reviews']

        data_to_add = {
            'user_name' : request.user.username,
            'rating' : rating,
            'feedback' : feedback
        }

        new_data = []
        new_data.append(data_to_add)
        new_data = new_data + old_data
        collection.update_one(
            
            {
                'uid':uid
            },
            {
                '$set':{
                    'reviews':new_data
                }
            },
            upsert=False,
        )
        messages.success(request,"Your review added Successfully")
        return redirect('/')