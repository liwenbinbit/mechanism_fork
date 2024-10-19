from mechanism import *
import numpy as np
import matplotlib.pyplot as plt
import csv

# Declare the joints that make up the system.
O, A, B, C, D,E,F,G,I,H = get_joints('O A B C D E F G I H')

# Declare the vectors and keep in mind that angles are in radians and start from the positive x-axis.
a = Vector((O, A), theta=np.pi/2, style='ground')                   #内部驱动连杆布置
b = Vector((A, B), r=9,theta=0,color = 'red')
c = Vector((B, C), r=25, color = 'green')
d = Vector((C, D), r=14,color = 'blue')
e = Vector((O, D), theta = np.deg2rad(90-43.17),r=35.08, show = False)

f = Vector((D,E), r = 68,color = 'black')                            #传动平行四连杆布置
g = Vector((E,F), r=20.52,color = 'black')
h = Vector((F,G), r=68,color = 'black')
i = Vector((D,G), theta = np.deg2rad(133),r=20.52,show = False)
j = Vector((E,C), r=70.61,show = False)

k = Vector((F,I), r=13, theta = np.pi, color= 'green', lw = 5)       #指尖连杆布置
l = Vector((I,H), r=30, theta = np.pi/2, color= 'green', lw = 5)
m = Vector((H,F), r=np.sqrt(13**2+30**2), show = False)

# Define the known input to the system.
# For a 500 RMP crank, the time it takes to rotate one rev is 0.12s
# time = np.linspace(0, 0.12, 300)
# angular_velocity = 50*np.pi/3  # This is 500 RPM in rad/s

# Setting up input
h_dis = 20
v_leaf = 1
# t = h_dis/v_leaf
time = np.linspace(0, 15, 201)
v1_pos = v_leaf*time
v1_vel = v_leaf*np.ones(time.size)
v1_acc = np.zeros(time.size)
print(f't: {time}')

# theta = angular_velocity*time  # Integrate to find the theta
# omega = np.full((time.size,), angular_velocity)  # Just an array of the same angular velocity
# alpha = np.zeros(time.size)


# Define the loop equation(s)
def loops(x, inp):
    temp = np.zeros((4, 2))
    temp[0] = a(inp) + b() + c(x[0]) + d(x[1]) -e()
    temp[1] = f(x[2])+ g(x[3]) + h(x[4]) - i()
    temp[2] = d(x[1]) + f(x[2]) + j(x[5])
    temp[3] = k() + l() + m(x[6])
    return temp.flatten()

# def loops(x, inp):
    # temp = np.zeros((4, 2))
    # temp[0] = v1(inp) + v2() + v3() + v4(x[0]) - v5() - v6(x[1])
    # temp[1] = v7(x[2]) + v8(x[3]) + v9() - v10() - v4(x[0]) - v3() - v2()
    # temp[2] = v11() + v12(x[4], x[5]) - v3()
    # temp[3] = v13() - v14(x[6], x[7]) + v10()
    # return temp.flatten()

# Guess the unknowns
pos_guess = np.deg2rad([50, -50,50,120,210,-150,150,-60])
# pos_guess = np.deg2rad([0, 0,0,0,0,0,0,0])
vel_guess = np.array([100, 100,100,100,100,100,100,100])
acc_guess = np.array([100, 100,100,100,100,100,100,100])

# Create the mechanism object
mechanism = Mechanism(vectors=(a, b, c, d,e,f,g,h,i,j,k,l), origin=O, loops=loops, pos=v1_pos, vel=v1_vel, acc=v1_acc,
                      guess=(pos_guess, vel_guess, acc_guess))

# Call mechanism.iterate() then get and show the animation
mechanism.iterate()
ani, fig_, ax_ = mechanism.get_animation()

# Plot the angles, angular velocity, and angular acceleration of vector d
fig, ax = plt.subplots(nrows=2, ncols=1)
# ax[0].plot(time, np.rad2deg(d.pos.thetas), color='maroon')
L1, = ax[0].plot(time, A.y_positions, color='maroon')
L2, = ax[0].plot(time, H.x_positions, color='green')
ax[0].legend((L1,L2),('Screw_dis','Fingertip_dis'))
ax[1].plot(time, np.rad2deg(np.pi/2-f.pos.thetas), color='maroon')
# ax[1].plot(time, H.x_positions, color='maroon')

ax[0].set_ylabel('Dis')
ax[1].set_ylabel('Angle of spread')
# ax[1].set_ylabel('y-fingertip_dis')

ax[1].set_xlabel(r'Time (s)')
# ax[0].set_title(r'Analysis of $\vec{d}$')

for a in (ax[0],ax[1]):
    a.minorticks_on()
    a.grid(which='both')
# ax.minorticks_on()
# ax.grid(which='both')

fig.set_size_inches(7, 7)
# # fig.savefig('../images/analysis_d.png')
print(A.y_positions)
print(H.x_positions)
print(np.rad2deg(np.pi/2-f.pos.thetas))
# print(np.rad2deg(np.pi-g.pos.thetas))

result_header = ['Screw_dis','Fingertip_dis','Angle of spread']
testfilename= "EG01_mechanism1111" + ".csv" 
re =[]
re = list(zip(A.y_positions,H.x_positions, np.rad2deg(np.pi/2-f.pos.thetas)))
# re= list(map(lambda x:[x],A.y_positions))
with open(testfilename,'w')as f:     
    writer = csv.writer(f)
    writer.writerow(result_header)
    writer.writerows(re)
plt.show()
