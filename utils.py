from datetime import datetime
                                                                                                                                         
def convert_time(time):
    date = datetime.fromtimestamp(time)                                                                                                    
    formatted_date = date.strftime('%d-%m-%Y')
    return formatted_date
                                                                                                                                         
def format_time(time):
    date = datetime.fromtimestamp(time).strftime('%H:%M %d-%m-%Y')
    return date
                                                                                                                                         
def convert_to_time(time):
    data = datetime.fromtimestamp(time).strftime('%H:%M')
    return data
                                                                                                                                         
# Chuỗi thời gian ban đầu
time_string = "11 Oct 2023 13:57:00"
                                                                                                                                         
def convert_datetime():
    time_format = "%d %b %Y %H:%M:%S"
                                                                                                                                            
    date_created = datetime.strptime(time_string, time_format)                                                                             
    timestamp = date_created.timestamp()                                                                                                   
                                                                                                                                            
    print("Timestamp:", timestamp)
    print(format_time(timestamp))  