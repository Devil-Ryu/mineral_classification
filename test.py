import torch
from torch.autograd import Variable
import cv2
import os
import numpy as np
import torch.nn.functional as f


model = "models/net_2.pkl"
val_path = "/home/zhou/mineral_data/test"

if(not os.path.isdir('failed_cases')):
    os.mkdir('failed_cases')

net = torch.load(model)
net.eval()
net = net.cuda()

minerals = os.listdir(val_path)

classes = {0:'biotite', 1:'hornblende', 2:'olivine', 3:'quartz', 4:'garnet'}

for mineral in minerals:
    total = 0
    correct = 0
    path = os.path.join(val_path,mineral)
    for image in os.listdir(path):
        image_path = os.path.join(path,image)
        cv_image = cv2.imread(image_path)
        cv_image = cv2.resize(cv_image,(224,224))
        input = torch.from_numpy(cv_image.astype(np.float32)).permute(2,0,1)
        input = (input-127.5)/127.5
        input = input.unsqueeze(0)
        input = Variable(input).cuda()
        pred = net(input)
        pred = f.softmax(pred,dim=1)
        pred_kind = int(torch.argmax(pred).cpu().data)
        pred = float(pred[0][pred_kind].cpu().data)
        pred_class =  classes[pred_kind]
        if (pred_class == mineral):
            correct += 1
        else:
            cv2.imwrite("failed_cases/"+pred_class+"_"+mineral+"_"+str(pred)+'.jpg',cv_image)
        total += 1

    print(mineral, " accuracy ",correct/float(total))