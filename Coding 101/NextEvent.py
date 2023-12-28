from datetime import datetime

now = datetime.now()

event = input("Enter the date of your event (DD-MM-YYYY): ")
event_lst = event.split("-")


dt_event = datetime(int(event_lst[2]), int(event_lst[1]), int(event_lst[0]))

day_to_event = dt_event - now

print("The event is currently " + str(day_to_event.days) + " days away" )
