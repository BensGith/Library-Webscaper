import requests
from bs4 import BeautifulSoup
from datetime import timedelta, date

# value in rooms dictionary represents rid
small_rooms = {"013": "1", "014": "4",
               "015": "5", "016": "6"}
medium_rooms = {"018": "7", "019": "8"}
big_rooms = {"101": "2", "107": "3"}
# creating a list of all times available for an order
times = ["08:00:00", "09:00:00"] + [str(i)+":00:00" for i in range(10, 23)]
date = "2020-01-12"  # change dynamically to desired date (every tuesday for example)
sd = date + " " + times[0]
ed = date + " " + times[1]
username = "benmali"
password = "Bentel26"

# login logs into the system and returns the session object

def login(username,password):
        url = "https://schedule.tau.ac.il/scilib/Web/index.php?redirect="
        session = requests.session()
        # header from post command
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {'email': username, 'password': password, "resume": "", "login": "submit", "language": "en_gb"}
        session.post(url, cookies=session.cookies, headers=header, data=payload)
        return session

# parse parameters from html page to get a specific wanted open slot
# build query string for get request
# --------------------------------------------------------
# capturing all table data for specific day of the week table including reservation ids inside tags
# capturing every reservation id in schedule page


#session = login(username,password)
def create():
        soup1 = BeautifulSoup(session.get('https://schedule.tau.ac.il/scilib/Web/schedule.php').text)
        table_body=soup1.find('tbody')
        rows = table_body.find_all('tr')
        table_row = [row.find_all('td') for row in rows]
        col = str(table_row).split(" ")
        res_ids = [string[7:29] for string in col if string[0:5] =="resid"]
        # there is also a field called colspan in COLS variable - calculation of reservation duration is possible
        # res_ids holds all the reservations in the page
        # --------------------------------------------------------
        desired_room_rid = big_rooms["107"]
        parameters_for_query = {"rid": desired_room_rid,  # change parameters
                                "sid": "1",
                                "rd": date,
                                "sd": sd,
                                "ed": ed}
        rs_page_par = ""

        for key in parameters_for_query.keys():
            rs_page_par = rs_page_par + str(key) + "=" + str(parameters_for_query[key]) + "&"
        res_page_url = "https://schedule.tau.ac.il/scilib/Web/reservation.php?" + rs_page_par
        res_page = session.get(res_page_url)
        soup = BeautifulSoup(res_page.text)

        user_id = str(soup.find("input", {"name": 'userId'})["value"])  # captures the user ID
        token = str(soup.find('input', {'name': 'CSRF_TOKEN'})["value"])  # changes every session,captures csrf token value
        begin_date = str(soup.find("input", {"id": "formattedBeginDate"})["value"])

        head = {
                "Referer": res_page_url  # changes accordingly to date and room desired
        }

        body = {"userId": user_id,
                "beginDate": begin_date,
                "beginPeriod": "08:00:00",
                "endDate": begin_date,
                "endPeriod": "09:00:00",
                "scheduleId": "1",
                "resourceId": "3",
                "reservationTitle":"",
                "reservationDescription":"",
                "reservationId":"",
                "referenceNumber":"",
                "reservationAction": "create",
                "DELETE_REASON":"",
                "seriesUpdateScope": "full",
                "CSRF_TOKEN": token}

        create_res_url = "https://schedule.tau.ac.il/scilib/Web/ajax/reservation_save.php"
        create = session.post(create_res_url,cookies=session.cookies, headers=head, data=body, verify=True)


def delete_reservation(user_id,rn):
        soup2 = BeautifulSoup(somepage.text)  # change some page
        csrf_token = str(soup2.find('input', {'name': 'CSRF_TOKEN'})["value"])
        delete_page = "https://schedule.tau.ac.il/scilib/Web/ajax/reservation_delete.php"
        # connect to reservation page
        # extract desired parameters, parse to parameters dictionary

        header = {"Referer": "{}?rn={}".format(delete_page, rn)}
        body = {
                "userId": user_id,  # replace depending on need,default is users id
                "beginDate": "2020 - 01 - 14",  # replace
                "beginPeriod": "08:00:00",  # replace
                "endDate": "2020 - 01 - 14",  # replace
                "endPeriod": "09:00:00",  # replace
                "scheduleId": "1",  # replace
                "resourceId": "2",  # replace
                "reservationTitle": "",
                "reservationDescription": "",
                "reservationId": "17743",  # replace
                "referenceNumber": rn,
                "reservationAction": "update",
                "DELETE_REASON": "",
                "seriesUpdateScope": "full",
                "CSRF_TOKEN": csrf_token}

if __name__ == "__main__":
        login("user","password")
        create()



