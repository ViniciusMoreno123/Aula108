# código fornecido para capturar as imagens da camera
import cv2
#* 1.importar o mediapipe utilizando o alias(as)
import mediapipe as mp

cap = cv2.VideoCapture(0)

#* 2. utilizar os dois módulos hands(detectar os pontos das mãos) e drawing(desenhar as linhas de um ponto a outro)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

#*3. criando o método hands e definindo os valores de detecção de confianção e cofiança de rastreamento
hands = mp_hands.Hands(min_detection_confidence=0.8,min_tracking_confidence=0.5)


#* 6.Defina função para desenhar as conexões
def drawHandLanmarks(image, hand_landmarks):
  #desenho das conexões entres os pontos de referencia
  if hand_landmarks:
    for landmarks in hand_landmarks:
      mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)


#TODO: 7.CRIAR FUNÇÃO PARA CONTAR OS DEDOS
#8. criar lista onde cada número representará um dedo 4 = polegar 8 indicador, etc...
tipIds = [4, 8, 12, 16, 20]


#9. função para contar dedos
def countFingers(image, hand_landmarks, handNo=0):
  #criar condição para verificar se recebemos o valor de hand_landmarks ou no
  if hand_landmarks:
    landmarks = hand_landmarks[handNo].landmark
    #print(landmarks)
    #10. após finalizar chamar função no loop

    #TODO: 11. loop para contagem dos dos dedos e leitura da posição de cada dedo levantado
    fingers = []

    for lm_index in tipIds:
      #obter valores y da ponta dos dedos até a parte inferior
      finger_tip_y = landmarks[lm_index].y
      finger_bottom_y = landmarks[lm_index - 2].y
      #criar codição para verificar se o dedo está aberto ou fechado
      if lm_index != 4:
        if finger_tip_y < finger_bottom_y:
          fingers.append(1)
          print("DEDO COM ID ", lm_index, " está levantado")
        if finger_tip_y > finger_bottom_y:
          fingers.append(0)
          print("DEDO com id ", lm_index, " está Fechado")

    # print(fingers)
    totalFingers = fingers.count(1)
    # Exiba o texto
    text = f'Dedos: {totalFingers}'
    cv2.putText(image, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (255, 0, 0), 2)


while True:
  success, image = cap.read()
  #5. inverter a imagem para não ficar espelhada: 0 = verticalmente ; 1 = horizontalmente
  image = cv2.flip(image, 1)

  #* 4.chamar o método e salvar dentro de uma variável results
  results = hands.process(
    image
  )  # executar o código: python count_fingers.py (ainda não será possível ver os pontos)

  #* 6.1 obter posição do ponto de ref
  hand_landmarks = results.multi_hand_landmarks

  #* 6.2 chamar a função
  drawHandLanmarks(image, hand_landmarks)

  #10.função para contar os dedos
  countFingers(image, hand_landmarks)

  cv2.imshow("Controlador de Midia", image)

  key = cv2.waitKey(1)
  if key == 32:
    break

cv2.destroyAllWindows()
