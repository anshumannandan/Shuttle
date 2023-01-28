from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from joblib import load
from rest_framework import status
import numpy as np

model = load('./Savedmodels/mlmodels.joblib')

# Create your views here.
class TestView(APIView):
    def get(self,request):
        fields = ([[1,12,7758.77]])
        field= np.array(fields).reshape((1,-1))
        ans = model.predict(field)
        print(ans)
        return Response(ans)