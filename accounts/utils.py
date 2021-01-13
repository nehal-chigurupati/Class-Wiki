import datetime as dt
from .models import Message, message_reply
def messages_recency_last_updated_sort(inputList):
    n = len(inputList)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if inputList[j].last_updated < inputList[j+1].last_updated:
                inputList[j], inputList[j+1] = inputList[j+1], inputList[j]
    return inputList

def messages_reverse_recency_sort(original_input_list):
    inputList = []

    for i in original_input_list:
        inputList.append(i)

    n = len(inputList)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if inputList[j].sent_at > inputList[j+1].sent_at:
                inputList[j], inputList[j+1] = inputList[j+1], inputList[j]
    return inputList
