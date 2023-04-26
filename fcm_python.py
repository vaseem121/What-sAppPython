from pyfcm import FCMNotification
 
push_service = FCMNotification(api_key="AAAA9pbV5wQ:APA91bHNjMMs-0R-vkYU6R8VWdMrY27ogjoTC1S1dpOXUMlcPU9bkYb6jZtGgwLwylhlR4slXZAFscALWxDEG1rwyvPO5L64QiIfp4p84MpwmYWukFqA9U8rVPaQuH9BDwTKnwajj5VZ")

def sendOnlineNotification(device_key,data):
 message_title = "Online Status"
 message_body = data[0]['contact_name']+" is online now"
 push_service.notify_single_device(registration_id=device_key, message_title=message_title, message_body=message_body)