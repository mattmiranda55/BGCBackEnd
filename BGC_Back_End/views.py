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
import jwt
import datetime
import json



"""

Graft API methods

"""




"""
Nethod for GETting and POSTing grafts
"""
@api_view(['GET', 'POST'])
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









"""
Method for uploading images to graft

This is seperated from the graft POST request since the 
"""
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_image(request, id, format=None):
    if request.method == "POST":
        try:
            graft = Graft.objects.get(pk=id)
        except Graft.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        image = request.data.get('image')
        graft.image = image
        
        
        return JsonResponse({"Message" : "Image succesfully added"})
    
    
    




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
    elif request.method == "DELETE":
        graft.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def graft_detail_by_category(request, category, format=None):
    try:
        graft = Graft.objects.filter(category=category)
    except Graft.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = GraftSerializer(graft, many=True)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = GraftSerializer(graft, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        graft.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def graft_detail_by_regulation(request, regulation, format=None):
    try:
        graft = Graft.objects.filter(regulation=regulation)
    except Graft.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = GraftSerializer(graft, many=True)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = GraftSerializer(graft, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        graft.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
Returns graft mage
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
            return JsonResponse({'message': 'Invalid email or password'})
        
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


"""

PayPal Payment Views

"""

