import pickle
import cv2

mean = pickle.load(open('clean_mean_preprocess.pickle', 'rb'))
model_svm = pickle.load(open('clean_model_svm.pickle', 'rb'))
model_pca = pickle.load(open('pca_250.pickle', 'rb'))

politician_pre = ['Robert Biedroń', 'Krzysztof Bosak', 'Andrzej Duda', 'Anna Grodzka', 'Szymon Hołownia',
                  'Jarosław Kaczynski', 'Ryszard Kalisz', 'Bronisław Komorowski', 'Janusz Korwin-Mikke',
                  'Leszek Miller', 'Beata Szydło', 'Rafał Trzaskowski', 'Donald Tusk']
font = cv2.FONT_HERSHEY_SIMPLEX


def pipeline_model(img):
    color = 'bgr'
    # to gray
    if color == 'bgr':
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    gray = gray / 255.0

    # resize image
    if gray.shape[1] > 100:
        gray_resize = cv2.resize(gray, (120, 120), cv2.INTER_AREA)
    else:
        gray_resize = cv2.resize(gray, (120, 120), cv2.INTER_CUBIC)
    # flattening
    gray_reshape = gray_resize.reshape(1, 14400)
    # subtract with mean

    gray_mean = gray_reshape - mean
    # get eigne image
    eigen_image = model_pca.transform(gray_mean)
    # pass to ML model (SVM)
    results = model_svm.predict_proba(eigen_image)[0]

    predict = results.argmax()
    result = politician_pre[predict]
    score = results[predict]
    return result, score
