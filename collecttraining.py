import numpy as np
from grabscreen import grab_screen
import cv2
import time
from getkeys import key_check
import os

w = [1,0,0,0,0,0,0,0,0]
s = [0,1,0,0,0,0,0,0,0]
a = [0,0,1,0,0,0,0,0,0]
d = [0,0,0,1,0,0,0,0,0]
wa = [0,0,0,0,1,0,0,0,0]
wd = [0,0,0,0,0,1,0,0,0]
sa = [0,0,0,0,0,0,1,0,0]
sd = [0,0,0,0,0,0,0,1,0]
nk = [0,0,0,0,0,0,0,0,1]

def keys_to_output(keys):
    '''
    Convert keys to a ...multi-hot... array
     0  1  2  3  4   5   6   7    8
    [W, S, A, D, WA, WD, SA, SD, NOKEY] boolean values.
    '''
    output = [0,0,0,0,0,0,0,0,0]
    
    if 'W' in keys and 'A' in keys:
        output = wa
    elif 'W' in keys and 'D' in keys:
        output = wd
    elif 'S' in keys and 'A' in keys:
        output = sa
    elif 'S' in keys and 'D' in keys:
        output = sd
    elif 'W' in keys:
        output = w
    elif 'S' in keys:
        output = s
    elif 'A' in keys:
        output = a
    elif 'D' in keys:
        output = d
    else:
        output = nk
    return output

'''file_name = 'training_data-1.npy'

if os.path.isfile(file_name):
	print('File exists, loading previous data!')
	training_data = list(np.load(file_name))
else:
	print('File does not exist, starting fresh!')
	training_data = []'''


def main():

	for i in list(range(4))[::-1]:
		print(i+1)
		time.sleep(1)
	paused = False
	for j in range(110,200):
		flag = True
		training_data = []
		count = 0
		while(flag):
			if not paused:
				screen = grab_screen(region = (0,23, 800, 623))
				last_time = time.time()
				#screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
				#screen = cv2.resize(screen,(80,60))
				keys = key_check()
				output = keys_to_output(keys)
				if(output==wd or output ==d):
					training_data.append(list(output))
					#date_string = time.strftime("%Y-%m-%d-%H:%M-%s")

					cv2.imwrite('data/training/track1/images/image-{0}-{1}'.format(j,count) +'.jpg', screen)
					#print(time.time() - last_time)
					count = count +1
				if len(training_data) % 1000 == 0 and count>0:
					flag = False
					print(len(training_data)*(j+1))
					file_name = 'data/training/track1/outputs/training_data-{0}.npy'.format(j)
					save_dir = os.path.join(os.getcwd(), file_name)
					np.save(file_name,training_data)

			keys = key_check()
			if 'T' in keys:
				if paused:
					paused = False
					print('unpaused')
					time.sleep(1)
				else:
					print('Pausing!')
					paused = True
					time.sleep(1)
main()