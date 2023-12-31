from django.http import JsonResponse
from .models import Graft, Category, Regulation, Profile
from django.contrib.auth.models import User
from .serializers import GraftSerializer, ProfileSerializer, UserSerializer
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from storages.backends.s3boto3 import S3Boto3Storage
import jwt
import datetime
import json
from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
import base64
from django.db import connection
import random
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from paypalrestsdk import Payment




"""

Graft API methods

"""




"""
Nethod for GETting and POSTing grafts
"""
@api_view(['GET', 'POST'])
@csrf_exempt
def graft_list(request, format=None):

    if request.method == "GET":
        grafts = Graft.objects.all()
        serializer = GraftSerializer(grafts, many=True)
        return Response(serializer.data)

    
    """
    Storing new grafts
    """
    if request.method == "POST":
        serializer = GraftSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({"message": "Invalid payload"})




"""
Approve / Deny Grafts 
Incoming payload must contain jwt and approve / decline and graft id
"""
@api_view(['POST'])
def validate_graft(request, format=None):
    
    if request.method == "POST":
           
        data = json.loads(request.body)
        token = data.get('jwt')
        graftId = data.get('graft_id')
        graft = Graft.objects.get(pk=graftId)
        
        
        if not token:
            return JsonResponse({'message': 'You are not signed in'}) 
        try:
            payload = jwt.decode(token, 'BGCcret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Invalid web token'}) 
        
        
        loggedInUserId = payload['id']
        loggedInUser = User.objects.filter(id=loggedInUserId).first()
        loggedInUserIsStaff = loggedInUser.is_staff
        
        if loggedInUserIsStaff:
            graft.validated = True
            graft.save()
            return JsonResponse({"message": "Graft validated"})
        
        else:
            return JsonResponse({"message": "You do not have permission to approve grafts"})






"""
Method for uploading images to graft

Takes in file and graft_id
Sets the image field for the Graft

There are 2 POST methods here, anmd it works so we are scared to touch it
"""
@api_view(['POST'])
def upload_image(request):
    
    if request.method == "POST":
        
        # for some reason, id returns as 1 less than actual value
        # this is so odd its almost comical. gotta love technology
        graftName = request.POST.get('graft_name')
        print(graftName)
        image = request.FILES.get('image')
        
        try:
            graft = Graft.objects.filter(name=graftName).first()
        except Graft.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        graft.image = image
        graft.save()
        return JsonResponse({"Message" : "Image succesfully added"})
    
    
    
    
    # if request.method == 'POST':
    #     image = request.FILES.get('image')  # Assuming your form has an 'image' field
    #     graftName = request.POST.get('graft_name')

    #     # Generate a unique filename (adjust as needed)
    #     filename = f"images/{graftName}_{random.randint(0,1000000)}.jpg"

    #     # Upload the image to S3
    #     file_path = default_storage.save(filename, ContentFile(image.read()))

    #     # Get the URL of the uploaded image
    #     image_url = default_storage.url(file_path)
        
    #     try:
    #         graft = Graft.objects.filter(name=graftName).first()
    #     except Graft.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

    #     graft.image = image_url
    #     graft.save()
    #     return JsonResponse({"Message" : "Image succesfully added"})
    
    
    

"""

Method for uploading documents to graft

The incoming payload must contain the graft id, 
and all of the files in seperate fields named "document"
Formdata instead of JSON since we are sending files 

"""
@api_view(['POST'])
def upload_document(request):
    
    if request.method == "POST":
        
        graftName = request.POST.get('graft_name')
        documents = request.FILES.getlist('document')
        
        try:
            graft = Graft.objects.filter(name=graftName).first()
        except Graft.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        s3_storage = S3Boto3Storage()
        documentUrls = []
        
        # adding documents 1 by 1
        for document in documents:
            s3_path = f'grafts/documents/{graftName}/{document.name}'
            s3_url = s3_storage.url(s3_path)
            s3_storage.save(s3_path, document)
            documentUrls.append(s3_url)
            # graft.documents.append(s3_url)  

        graft.documents = documentUrls
        print(graft.documents)
        graft.save()
        return JsonResponse({"Message" : "Documents succesfully added"})





"""
Get graft by { whatever } views
"""

@api_view(['GET', 'PUT', 'DELETE'])
def graft_detail_by_id(request, id, format=None):

    try:
        graft = Graft.objects.get(pk=id)
    except Graft.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = GraftSerializer(graft)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = GraftSerializer(graft, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # when user deletes graft
    # delete graft, and increase profile credits by 1
    # first we check and decode jwt
    # make sure user can only delete THEIR grafts 
    elif request.method == "DELETE":
        
        data = json.loads(request.body)
        token = data.get('jwt')
        
        if not token:
            return JsonResponse({'message': 'You are not signed in'}) 
        try:
            payload = jwt.decode(token, 'BGCcret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Invalid web token'}) 
        
        # get user data and profile data using id within token
        user = User.objects.filter(username=graft.created_by).first()
        profile = Profile.objects.filter(user_id=user.id).first()
        
        loggedInUserId = payload['id']
        loggedInUser = User.objects.filter(id=loggedInUserId).first()
        loggedInUserIsStaff = loggedInUser.is_staff
        
        if user.id != loggedInUserId and not loggedInUserIsStaff:
            return JsonResponse({"message": "You do not have permission to delete this graft"})

        profile.num_credits += 1
        profile.save()
        graft.delete()
        return JsonResponse({"message": "Graft succesfully deleted"})



# This method will be utilized by the dynamic routing of SingleProductPage
@api_view(['GET', 'PUT', 'DELETE'])
def graft_detail_by_name(request, name, format=None):
    
    try:
        graft = Graft.objects.get(name=name)
    except Graft.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = GraftSerializer(graft)
        return Response(serializer.data)




@api_view(['GET'])
def graft_detail_by_category(request, category, format=None):
    try:
        graft = Graft.objects.filter(category=category)
    except Graft.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = GraftSerializer(graft, many=True)
        return Response(serializer.data)




@api_view(['GET'])
def graft_detail_by_regulation(request, regulation, format=None):
    try:
        graft = Graft.objects.filter(regulation=regulation)
    except Graft.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = GraftSerializer(graft, many=True)
        return Response(serializer.data)



@api_view(['GET'])
def get_cat_name(request, category, format=None):
    try:
        cat_id = Category.objects.get(id=category)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return Response(Category.__str__(cat_id))


@api_view(['GET'])
def get_reg_name(request, regulation, format=None):
    try:
        cat_id = Regulation.objects.get(id=regulation)
    except Regulation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return Response(Regulation.__str__(cat_id))


"""
Returns a list of grafts posted by a particular user
"""
@api_view(['POST'])
def graft_detail_by_username(request):
    
    if request.method == "POST":  
        data = json.loads(request.body)
        username = data.get('username')
        grafts = Graft.objects.filter(created_by=username)
        serializers = GraftSerializer(grafts, many=True)
        return Response(serializers.data)




"""
Returns graft image
"""
@api_view(['GET'])
def get_image(request, format=None):
    image_file = request.FILES['image'].file.read()
    Graft.objects.create(image=image_file)





"""

User / Profile API Methods 

"""


# methods to check is username or email is taken
def is_email_taken(email):
    try:
        user = User.objects.get(email=email)
        return True
    except User.DoesNotExist:
        return False

def is_username_taken(username):
    try:
        user = User.objects.get(username=username)
        return True
    except User.DoesNotExist:
        return False



@api_view(['GET', 'POST'])
def user_list(request, format=None):

    if request.method == "GET":
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    """Creating new users"""
    if request.method == "POST":  
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        hashed_password = make_password(password)  # hashes password
        
        if is_email_taken(email):
            return JsonResponse({'message': "Email is already taken"})  
        if is_username_taken(username):
            return JsonResponse({'message': "Username is already taken"})
        
        new_user = User.objects.create(username=username, email=email, password=hashed_password)
        return JsonResponse({'id': new_user.id})

        
        



    

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_by_id(request, id, format=None):

    try:
        user = User.objects.get(pk=id)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_by_username(request, username, format=None):

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_by_email(request, email, format=None):

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
@api_view(['GET', 'POST'])
def profile_list(request, format=None):

    if request.method == "GET":
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)



@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def profile_detail_by_user_id(request, user_id, format=None):

    try:
        profile = Profile.objects.get(user_id=user_id)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    

@api_view(['GET', 'PUT', 'DELETE'])
def profile_detail_by_business_name(request, business_name, format=None):

    try:
        profile = Profile.objects.get(business_name=business_name)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def profile_detail_by_username(request, username, format=None):

    try:
        profile = Profile.objects.get(username=username)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'PUT', 'DELETE'])
def profile_detail_by_phone_number(request, phone_number, format=None):

    try:
        profile = Profile.objects.get(phone_number=phone_number)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    




"""

Authentication Endpoints ==============================================================================


"""



@api_view(['POST'])
@csrf_exempt
def loginUser(request):
    if request.method == 'POST':
        
        # Get the request data as a dictionary
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        # find user by email in request payload
        user = User.objects.filter(email=email).first()
        
        # if user not found
        if user is None:
            return JsonResponse({'message': 'Invalid email'})
        
        # checking password match, check_passwords checks hashed passwords
        if not user.check_password(password):
            return JsonResponse({'message': 'Incorrect Password'})
        
        # creating jwt token
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'BGCcret', algorithm='HS256')  # second param is secret key for hashing
    
        
        # if succesful login 
        print("Login Successful")
        
        # returning jwt token
        # frontend will store token into localstorage
        return JsonResponse({'jwt': token})
        
            
    else:
        return JsonResponse({'message': 'Invalid authentication request'}, status=405)





"""

This method takes the current authenticated user and returns their data as cookies to the client
Username, email etc

"""
@api_view(['POST'])
def userInfo(request):
    
    if request.method == 'POST':
    
        # pull token from cookies 
        data = json.loads(request.body)
        token = data.get('jwt')
        
        # checks for jwt token (credentials)
        if not token:
            return JsonResponse({'message': 'You are not signed in'}) 

        # decode jwt
        try:
            payload = jwt.decode(token, 'BGCcret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Invalid web token'}) 
        
        # get user data and profile data using id within token
        user = User.objects.filter(id=payload['id']).first()
        profile = Profile.objects.filter(user_id=payload['id']).first()
        user_serializer = UserSerializer(user)
        profile_serializer = ProfileSerializer(profile)
        
        return Response([user_serializer.data, profile_serializer.data]) 



@api_view(['POST'])
def logout(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        token = data.get('jwt')
        
        if not token:
            return JsonResponse({"message": "You are not logged in!"})
    
        # delete cookie from session 
        response = Response()
        response.data = {
            "message": "Successfully Logged Out"
        }
        
        return response
    

    
@api_view(['POST'])
def change_password(request):
    if request.method == 'POST':

        # pulling data from request
        data = json.loads(request.body)
        token = data.get('jwt')
        email = data.get('email')
        password = data.get('password')
        new_password = data.get('new_password')


        if not token:
            return JsonResponse({"message": "You are not logged in!"})

        # validating jwt token
        try:
            payload = jwt.decode(token, 'BGCcret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Invalid web token'})  
        
        # find user by id, using jwt
        user = User.objects.filter(id=payload['id']).first()

        # if user not found
        if user is None:
            return JsonResponse({'message': 'User not found'})
        

        # Check if the current password is correct
        # Change password if correct
        if authenticate(username=user.username, password=password):
            user.set_password(new_password)
            user.save()
            return JsonResponse({'message': 'Password changed successfully'}, status=200)
        else:
            return JsonResponse({'message': 'Current password is incorrect'}, status=400)




@api_view(['POST'])
def change_username(request):
    if request.method == 'POST':

        # pulling data from request
        data = json.loads(request.body)
        token = data.get('jwt')
        email = data.get('email')
        password = data.get('password')
        new_username = data.get('new_username')


        if not token:
            return JsonResponse({"message": "You are not logged in!"})

        # validating and decoding jwt token
        try:
            payload = jwt.decode(token, 'BGCcret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Invalid web token'})  
        
        # find user by id, using jwt
        user = User.objects.filter(id=payload['id']).first()

        existingUser = User.objects.filter(username=new_username).first()
        if existingUser:
            return JsonResponse({'message': 'Username already taken'})

        # if user not found
        if user is None:
            return JsonResponse({'message': 'User not found'})
        

        # Check if the current password is correct
        # Change password if correct
        if authenticate(username=user.username, password=password):
            user.username = new_username 
            user.save()
            return JsonResponse({'message': 'Username changed successfully'}, status=200)
        else:
            return JsonResponse({'message': 'User info is incorrect'}, status=400)


        return JsonResponse({"message": "Username changed successfully"})



    
    
"""
When user posts graft, we need to subtract 1 credit
"""
@api_view(['POST'])
def user_post_graft(request):
    
    if request.method == 'POST':
        
        data = json.loads(request.body)
        token = data.get('jwt')
        
        if not token:
            return JsonResponse({"message": "You are not logged in!"})
        
        # decode jwt
        try:
            payload = jwt.decode(token, 'BGCcret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Invalid web token'}) 
        
        # get user data and profile data using id within token
        profile = Profile.objects.filter(user_id=payload['id']).first()
        profile.num_credits -= 1
        profile.save()
        return JsonResponse({'message': 'You have used one token'}) 
    



"""
When user deletes graft, we need to add 1 credit
"""
@api_view(['POST'])
def user_delete_graft(request):
    
    if request.method == 'POST':
        
        data = json.loads(request.body)
        token = data.get('jwt')
        
        if not token:
            return JsonResponse({"message": "You are not logged in!"})
        
        # decode jwt
        try:
            payload = jwt.decode(token, 'BGCcret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Invalid web token'}) 
        
        # get user data and profile data using id within token
        profile = Profile.objects.filter(user_id=payload['id']).first()
        profile.num_credits += 1
        return JsonResponse({'message': 'You have added one token'}) 



@api_view(['POST'])
def user_purchase_credits(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        token = data.get('jwt')

        if not token:
            return JsonResponse({'message': 'You are not logged in!'})
        
        try:
            payload = jwt.decode(token, 'BGCcret', algorithms=['HS256'])
        except:
            return JsonResponse({'message': 'Invalid web token'})
        
        profile = Profile.object.filter(user_id=payload['id']).first()

        if data.get('purchasetype') == 'single':
            profile.num_credits += 1
            return JsonResponse({'message': 'You have added one token'}) 
        elif data.get('purchasetype') == 'multiple':
            profile.num_credits += 8
            return JsonResponse({'message': 'You have added eight tokens'}) 
        elif data.get('purchasetype') == 'unlimited':
            profile.num_credits += 9999
            return JsonResponse({'message': 'You have added unlimited tokens'}) 
    
            





"""

PayPal Payment Views

1. We receive request that contains payment info and item purchased
2. This info is used to fill out paypal payment 
3. Successful payment returned

Make sure the request copntains the item they are purchasing as well
"""



def create_payment(request):
    
    data = json.loads(request.body)
    item = data.get('item_purchased')
    
    description = ""
    price = 0
    
    
    # Handling price and description based on the item purchased
    
    if item == "1 credit":
        price = 5000
        description = "Ability to post one graft. Includes customer support"
        
    elif item == "8 credits":
        price = 25000
        description = "Ability to post 8 grafts. Includes a large saving per post and direct contact to developers"
    
    elif item == "unlimited credits":
        price = 35000
        description = "Ability to post unlimited grafts. Best long term deal. Includes direct developer and CEO contact"
        
    
    
    if price != 0:

        # payment form
        payment = Payment({
            "intent": "sale",                                   # The payment intent, set to "sale" for a regular payment
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "http://localhost:3000/success",  # URL to redirect to on successful payment
                "cancel_url": "http://localhost:3000/cancel"    # URL to redirect to on canceled payment
            },
            "transactions": [{
                "amount": {
                    "total": price,                             # Total amount of the payment
                    "currency": "USD"                           # Currency code for the total amount
                },
                "description": description                      # Description of your product or item
            }]
        })


        # processing payment and returning response
        if payment.create():
            return JsonResponse({"payment_id": payment.id})
        else:
            return JsonResponse({"error": payment.error})