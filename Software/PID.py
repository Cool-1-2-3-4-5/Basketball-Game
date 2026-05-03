Frame_width = int(input("Enter Frame Width: "))
Frame_height = int(input("Enter Frame Height: "))
Hoop_width = 40.0
Hoop_height = 40.0

x_axis_rate = Frame_width/Hoop_width
y_axis_rate = Frame_height/Hoop_height

# Input from Kalmin Filter
predicted_location = (400,200)

current_location_cm = (0,0)

move_to_cm = (predicted_location[0]/x_axis_rate,predicted_location[1]/y_axis_rate)

def conversion_to_steps(move_to_cm, current_location_cm):
    x_movement = move_to_cm[0] - current_location_cm[0]
    y_movement = move_to_cm[1] - current_location_cm[1]
    x_steeper_degrees = (x_movement / 4) * 360
    y_steeper_degrees = (y_movement / 4) * 360
    return x_steeper_degrees,y_steeper_degrees

def P_control(x_steeper_degrees_left,y_steeper_degrees_left,steps_complete,confidence,kp=0.1):
    error_x = (x_steeper_degrees_left-steps_complete)*kp*confidence
    error_y = (y_steeper_degrees_left-steps_complete)*kp*confidence
    cum_error_x += error_x
    cum_error_y += error_y
    



# cirfucence ofpulley wheel is 4 cm. Do for 10 spins of wheel, the carridge moves to the end
