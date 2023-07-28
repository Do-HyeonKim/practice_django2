from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from .models import *
from django.http import JsonResponse
from multiprocessing import Pool
import multiprocessing as mp
import time


# 멀티프로세스 예제에서 사용할 인자 x값에 대한 제곱을 실행하는 메소드 
def square(x):
    return x * x

# 1. apply() 사용 example
@api_view(['post'])
def multi_apply_view(request) :
    start = time.time()
    with Pool(processes=4) as pool:
        result = pool.apply(square, (5,))
        print("result = ", result)
        result = pool.apply(square, (6,))
        print("result = " ,result)
        result = pool.apply(square, (10,))
        print("result = ",result)
    end = time.time()

    print("총 소요시간 : " , end - start)
    return JsonResponse(result, safe=False)


# 2. map() 사용 example
@api_view(['post'])
def multi_map_view(request) :
    number_list = []
    for i in range(1,101) :
        number_list.append(i) 
    start = time.time()
    with Pool(processes=4) as pool:
        numbers = number_list
        results = pool.map(square, numbers)
        print("result =", results)   
    end = time.time()

    print("총 소요시간 : " , end - start)
    return JsonResponse(results, safe=False)
  

# 3. imap() 사용 example
@api_view(['post'])
def multi_imap_view(request) :
    number_list = []
    for i in range(1,101) :
        number_list.append(i) 
    start = time.time()
    with Pool(processes=4) as pool:
        numbers = number_list
        results = pool.imap(square, numbers)
        results_list = list(results)

        for result in results_list : 
            print("result =", result)

    end = time.time()

    print("총 소요시간 : " , end - start)
    return JsonResponse(results_list, safe=False)

# 멀티프로세싱 example (1)
def square_wrapper(chunk):
    return [square(num) for num in chunk]

@api_view(['POST'])
def example_multi_view(request):
    number_list = []
    for i in range(1, 101):
        number_list.append(i)

    numbers = number_list
    num_processes = 4
    chunk_size = len(numbers) // num_processes
    chunks = []
    for i in range(0, len(numbers), chunk_size):
        chunk = numbers[i:i+chunk_size]
        chunks.append(chunk)
  

    start = time.time()
    with Pool(processes=num_processes) as pool:
        results = pool.map(square_wrapper, chunks)
        pool.close()
        pool.join()

    final_result = []
    print("results=", results)
    for sublist in results:
        print("sublist=",sublist)
        for result in sublist:
            final_result.append(result)
    
    end = time.time()
    
    print("총 소요시간 =", end - start)

    return JsonResponse(final_result, safe=False)
