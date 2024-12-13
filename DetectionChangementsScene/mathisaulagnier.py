import cv2
import numpy as np

def preporcess_image(image):
    '''
    Cette fonction prend une image en entrée et retourne une image prétraitée.
    '''
    # Convertir l'image en LAB
    lab_img = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    # Séparer les canaux
    l, a, b = cv2.split(lab_img)
    
    #hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #h, s, v = cv2.split(hsv_img)


    # Appliquer l'égalisation d'histogramme sur le canal L avec Clahe jugé plus efficace que l'égalisation d'histogramme classique
    clahe = cv2.createCLAHE(clipLimit=7, tileGridSize=(6, 6))
    equalized_image = clahe.apply(l)

    # Appliquer un flou gaussien pour réduire le bruit
    blurred_image = cv2.GaussianBlur(equalized_image, (5, 5), 0)

    # Normaliser la composante L pour limiter l'influence de la luminosité
    norm_image = cv2.normalize(blurred_image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    return norm_image

def encadrer(diff, img_shape):
    '''
    Cette fonction prend une image de différence et la forme de l'image originale en entrée.
    Elle retourne une liste de rectangles encadrant les objets détectés.
    '''
    # Appliquer un seuillage pour obtenir une image binaire
    _, thresh = cv2.threshold(diff, 55, 255, cv2.THRESH_BINARY)
    
    # Appliquer une fermeture et une ouverture morphologique pour éliminer le bruit
    kernel = np.ones((5,5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    # Trouver les contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filtrer les contours en fonction de leur aire
    min_area = 4000
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
    
    # Trier les contours par aire décroissante
    sorted_contours = sorted(filtered_contours, key=cv2.contourArea, reverse=True)
    
    # Garder les 15 plus grands contours
    top_contours = sorted_contours[:15]
    
    # Convertir les contours en rectangles
    rectangles = [cv2.boundingRect(cnt) for cnt in top_contours]
    
    # Fusionner les rectangles qui se chevauchent
    merged_rectangles = merge_rectangles(rectangles)
    
    # Filtrer les rectangles basés sur leur position
    filtered_rectangles = filter_rectangles(merged_rectangles, img_shape)
    
    return filtered_rectangles

def merge_rectangles(rectangles):
    '''
    Cette fonction prend une liste de rectangles en entrée et retourne une liste de rectangles fusionnés.
    '''
    if not rectangles:
        return []

    merged = []
    for rect in rectangles:
        # Si la liste des rectangles fusionnés est vide, ajouter le rectangle actuel
        if not merged:
            merged.append(rect)
        # Sinon, fusionner le rectangle actuel avec un rectangle existant s'ils se che
        else:
            merged_rect = rect
            for i, existing_rect in enumerate(merged):
                # Si les rectangles se chevauchent, les fusionner
                if rectangles_overlap(merged_rect, existing_rect):
                    merged_rect = merge_two_rectangles(merged_rect, existing_rect)
                    merged[i] = merged_rect
                    break
            else:
                merged.append(merged_rect)
    return merged

def rectangles_overlap(rect1, rect2):
    '''
    Cette fonction prend deux rectangles en entrée et retourne True s'ils se chevauchent, False sinon.
    '''
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    return not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)

def merge_two_rectangles(rect1, rect2):
    '''
    Cette fonction prend deux rectangles en entrée et retourne un rectangle fusionné.   
    '''
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    x = min(x1, x2)
    y = min(y1, y2)
    w = max(x1 + w1, x2 + w2) - x
    h = max(y1 + h1, y2 + h2) - y
    return (x, y, w, h)

def filter_rectangles(rectangles, img_shape):
    '''
    Cette fonction prend une liste de rectangles et la forme de l'image en entrée.
    Elle retourne une liste de rectangles filtrés en fonction de leur position.
    '''
    height, width = img_shape[:2]
    left_threshold = width * 0.2
    right_threshold = width * 0.9
    top_threshold = height * 0.2

    filtered = []
    for rect in rectangles:
        x, y, w, h = rect
        if x > left_threshold and x + w < right_threshold and y + h > top_threshold:
            filtered.append(rect)
    return filtered

def main(reference_path, current_path):
    '''
    Cette fonction prend les chemins des images de référence et actuelle en entr
    Elle affiche les différences entre les deux images et encadre les objets détectés.
    '''
    # Lire les images
    reference = cv2.imread(reference_path)
    current = cv2.imread(current_path)
    
    # Prétraiter les images
    reference_eq = preporcess_image(reference)
    current_eq = preporcess_image(current)

    # Calculer la différence entre les images
    diff = cv2.absdiff(reference_eq, current_eq)

    # Encadrer les objets détectés
    changes = encadrer(diff, current.shape)

    # Afficher les objets détectés
    result = current.copy()  # Use the original image for visualization

    # Dessiner les rectangles autour des objets détectés
    for rect in changes:
        x, y, w, h = rect
        cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
    # Afficher l'image résultante
    cv2.imshow('Detected Changes', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

main('Images/Salon/Reference.JPG', 'Images/Salon/IMG_6553.JPG')