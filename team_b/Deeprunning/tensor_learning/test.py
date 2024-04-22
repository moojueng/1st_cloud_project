from tensorflow.keras.models import load_model
import cv2
xception_model = load_model("/home/gugu/Project/back/tensor_learning/Model/best.h5")

Choi = cv2.imread('/home/gugu/Project/back/tensor_learning/01039978450_Choi/01039978450_face0.jpg')
An = cv2.imread('/home/gugu/Project/back/tensor_learning/01080082021_An/01080082021_face0.jpg')
Jo = cv2.imread('/home/gugu/Project/back/tensor_learning/01085988951_Jo/01085988951_face0.jpg')
Sim = cv2.imread('/home/gugu/Project/back/tensor_learning/01097805386_Sim/01097805386_face0.jpg')

Choi = cv2.resize(Choi, (224, 224), interpolation=cv2.INTER_NEAREST)
An = cv2.resize(An, (224, 224), interpolation=cv2.INTER_NEAREST)
Jo = cv2.resize(Jo, (224, 224), interpolation=cv2.INTER_NEAREST)
Sim = cv2.resize(Sim, (224, 224), interpolation=cv2.INTER_NEAREST)

Choi = Choi.reshape(-1, 224, 224, 3)/255
An = An.reshape(-1, 224, 224, 3)/255
Jo = Jo.reshape(-1, 224, 224, 3)/255
Sim = Sim.reshape(-1, 224, 224, 3)/255

r1 = xception_model.predict(Choi, batch_size=1, verbose=1)
r2 = xception_model.predict(An, batch_size=1, verbose=1)
r3 = xception_model.predict(Jo, batch_size=1, verbose=1)
r4 = xception_model.predict(Sim, batch_size=1, verbose=1)

print('Choi: ', r1[0])
print('An: ', r2[0])
print('Jo: ', r3[0])
print('Sim: ', r4[0])
