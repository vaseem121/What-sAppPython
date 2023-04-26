import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import fcm_python as notify
# Fetch the service account key JSON file contents
cred = credentials.Certificate('utils/whatstracker-2c129-firebase-adminsdk-mizvy-2d0f2865ae.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://whatstracker-2c129-default-rtdb.firebaseio.com/"
})
accounts = 'accounts'
indexing = ''
def deleteNodeFromDB(ref):
    build_id = "OPJ28.111-22-1"
    refs = ref.order_by_child('build_id').equal_to(build_id).get()
    print(refs)

def getAndUpdateDB():
    ref = db.reference('accounts').order_by_key().limit_to_last(1).get()
    listSnap = list(ref.items())
    indexing = listSnap[0][0]
    pathName = indexing+'/name'
    pathImg = indexing+'/profile_pic'
    #snapshot = ref.order_by_key().limit_to_last(1)
    db.reference(accounts).update({
        pathName: 'Bansh Sir Cool',
        pathImg: 'Yahi milo bahar kyu milna hai'
    })
def saveUserProfileInfo(data):
    ref = db.reference('accounts').get()
    #listSnap = list(ref.items())
    indexing = len(ref) - 1
    indexing = str(indexing)
    pathName = indexing+'/name'
    pathBuildId = indexing+'/build_id'
    pathImg = indexing+'/profile_pic'
    pathContact = indexing+'/contact_number'
    pathendDate = indexing+'/end_date_time'
    pathFollowing = indexing+'/following'
    pathIsSleep = indexing+'/is_sleep'
    pathStatus = indexing+'/status'
    pathContactList = indexing+'/contact_list'
    pathUniqueCode = indexing+'/unique_code'
    actData = db.reference('accounts/'+indexing).get()
    if actData['status'] == 'Active':
        status = 'Active'
    else:
        status = 'Awaiting Action'
    db.reference(accounts).update({
        pathName: data[0]['user_name'],
        pathImg: data[0]['user_photo'],
        pathStatus: 'Awaiting action'
    })

def saveContactList(data,i):
    print(">>>> My No",data[0]['contact_phone'])
    ref = db.reference('accounts').get()
    indexing = len(ref) - 1
    matchedIndex = ''
    indexing = str(indexing)
    contactLists = db.reference('accounts/'+indexing+'/contact_list').get()
    if contactLists:
        totalContact = len(contactLists)
        flag = 0
        for i in range(len(contactLists)):
            if contactLists[i]['contact_number'] == data[0]['contact_phone']:
                db.reference('accounts/'+indexing+'/contact_list/'+str(i)).update({
                    'contact_active': contactLists[i]['contact_active'],
                    'contact_number': data[0]['contact_phone'],
                    'name': data[0]['contact_name'],
                    'profile_pic': data[0]['contact_photo'],
                    'online_status': data[0]['online_status']
                })
                flag = 1
                singleContact = db.reference('accounts/'+indexing+'/contact_list/'+str(i)).get()
                print("Single Contact",singleContact)
                if singleContact['online_status'] == 'offline':
                    device_token = getUserProfileInfo()
                    if device_token != '':
                        notify.sendOnlineNotification(device_token,data)
                break
            contactIndexLast = i+1
        if flag == 0:
            db.reference('accounts/'+indexing+'/contact_list/'+str(totalContact)).update({
                'id': int(contactIndexLast),
                'contact_active': 'no',
                'contact_number': data[0]['contact_phone'],
                'name': data[0]['contact_name'],
                'profile_pic': data[0]['contact_photo'],
                'online_status': data[0]['online_status']
            })
    else:
        db.reference('accounts/'+indexing+'/contact_list/0').update({
            'id': 1,
            'contact_active': 'no',
            'contact_number': data[0]['contact_phone'],
            'name': data[0]['contact_name'],
            'profile_pic': data[0]['contact_photo'],
            'online_status': data[0]['online_status']
        })
    # if i != 0:
    #     for i in range(len(contactLists)):
    #         if contactLists[i]['contact_active'] == 'yes':
    #             if data[0]['online_status'] == 'online':
    #                 device_token = getUserProfileInfo()
    #                 if device_token != '':
    #                     notify.sendOnlineNotification(device_token,data)
        # pathContactList = indexing+'/contact_list'   
    # db.reference(accounts).update({
    #     pathContactList: {
    #         'contact_active': 'yes',
    #         'contact_number': '917786931286',

    #     },
    # })
def getUserProfileInfo():
    ref = db.reference('accounts').get()
    indexing = len(ref) - 1
    indexing = str(indexing)
    actData = db.reference('accounts/'+indexing).get()
    device_token = ''
    if actData:
        device_token =  actData['device_token']
        return device_token
    else:
        return device_token

# def main():
#     print(">>>>>>>>>>>>>>>>>> Get and Update Data in root Node")
#     getUserProfileInfo()
#     # data = []
#     # data.append({'contact_name': 'dfgsdfgsfdgfdgd Deepanshu','contact_photo' : 'https://pps.whatsapp.net/v/t61.24694-24/338836643_247119214390577_859335063681509195_n.jpg?stp=dst-jpg_s96x96&ccb=11-4&oh=01_AdSxyVTklNu__d_npN6T1dDg0eQkvvOgTfsEIbr24CNvoA&oe=6442176A','phone_no' : '+916666766678' })
#     # contacListInsert(data)
#     # print(">>>>>>>>>>>>>>>>>> Insert New Node in DB")

#         # listSnap = list(snapshot.items())
#     # print(listSnap[0][1]['build_id'])
#     # for key, val in snapshot:
#     #     print('{1}'.format(key, val))
#     # for key in snapshot:
#         #deleteNodeFromDB(ref)

# if __name__ == '__main__':
#     main()

