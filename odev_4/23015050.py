import cv2
from collections import deque #yüzün koordinatlarını tutmak için gerekli
import time #sayaç için gerekli

cap = cv2.VideoCapture(0)  
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
) #opencv'nin daha önce eğitilmiş hazır bir yüz tanıma modeli
  

pts = deque(maxlen=60)  # son 60 framein koordinatlarını tutuyor
face_detection = False #yüz tespiti yapıldı mı/yapılmadı mı
time_start = 0 #sayacın başlangıç değeri

while True:
    ret, frame = cap.read()  
    if not ret:
        break
    else:
        print(frame.shape)

    width = int(cap.get(3))
    height = int(cap.get(4))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    faces = face_cascade.detectMultiScale(gray, 
                                        scaleFactor=1.1, #görüntü yüzde on küçültülerek taranır
                                        minNeighbors=5, #yüz sayılabilmesi için en az sayıdaki komşu dikdörtgen sayısı
                                        minSize=(50, 50)) #yüz boyutu

    if len(faces) > 0:
        if not face_detection: #false tanımladığımız için şu an true'ya döndü
            face_detection = True
            time_start = time.time()

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            center = (x + w//2, y + h//2) #yüzün merkez koordinatlarını yazdırıyor, hareketini çizdirirken gerekli
            cv2.putText(frame, f"{center}", (x, y-20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            pts.append(center)

        final_time = int(time.time() - time_start)
        cv2.putText(frame, f"{final_time} s", (frame.shape[1]-100, 30), #frame.shape[1] -> genişliği gösterir
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    else:
        face_detection = False 
        time_start = 0
        pts.clear() #görüntüde yüz yoksa her şey sıfırlanır

    for i in range(1, len(pts)):
        cv2.line(frame, pts[i-1], pts[i], (0, 255, 0), 2)

    cv2.imshow('Yuz Tanima', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

