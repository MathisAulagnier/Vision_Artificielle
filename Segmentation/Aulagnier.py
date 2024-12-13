import cv2
import numpy as np
import pandas as pd
from skimage import color
from skimage.segmentation import watershed
from skimage.feature import peak_local_max
from scipy import ndimage as ndi
import matplotlib.pyplot as plt

def preprocess_image(image):
    """Prétraitement de l'image."""
    # Conversion en niveaux de HSV
    HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Extraire la composante de luminance
    h, s, v = cv2.split(HSV)
    value = v
    # Amélioration du contraste
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    value_clahe = clahe.apply(value)
    # Réduction du bruit
    preprocessed_image = cv2.GaussianBlur(value_clahe, (9, 9), 0)
    return preprocessed_image

def watershed_segmentation(preprocessed_image, gray_image):
    """Segmentation des grains par Watershed."""
    # Seuillage
    _, thresh_g = cv2.threshold(preprocessed_image, 40, 255, cv2.THRESH_BINARY)
    
    # Créer une carte de distance
    distance = ndi.distance_transform_edt(thresh_g)
    coordinates = peak_local_max(distance, footprint=np.ones((65, 65)), labels=thresh_g)
    
    # Marquer les grains
    markers = np.zeros_like(thresh_g, dtype=bool)
    markers[tuple(coordinates.T)] = True
    markers = ndi.label(markers)[0]

    # Application du watershed
    labels = watershed(-distance, markers, mask=thresh_g)
    image_colorier = color.label2rgb(labels, image=gray_image, bg_label=0)

    return labels, image_colorier

def extract_grain_features(image, gray_image, labels):
    # Calcul des moyennes BGR pour chaque segment de grain
    data = {"Moyenne de B": [], "Moyenne de G": [], "Moyenne de R": []}

    # Boucle sur chaque grain détecté
    for label in np.unique(labels):
        if label == 0:  # Ignorer le fond
            continue
        mask = np.zeros_like(gray_image, dtype="uint8")
        mask[labels == label] = 255
        
        # Calcul des moyennes de chaque canal BGR dans la zone du masque
        mean_val = cv2.mean(image, mask=mask)
        data["Moyenne de B"].append(mean_val[0])
        data["Moyenne de G"].append(mean_val[1])
        data["Moyenne de R"].append(mean_val[2])

    # Création du DataFrame
    df = pd.DataFrame(data)
    df.index = [f"Grain{i+1}" for i in range(len(df))]
    return df

def main(img_path, show_images=False):
    # Charger l'image
    image_path = img_path  # Remplace par ton chemin d'image
    image = cv2.imread(image_path)
    
    if image is None:
        raise ValueError("Impossible de charger l'image. Vérifiez le chemin.")

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    preprocessed_image = preprocess_image(image)
    
    # Segmentation Watershed
    labels, image_colorier = watershed_segmentation(preprocessed_image, gray_image)

    # Extraction des caractéristiques
    features_df = extract_grain_features(image, gray_image, labels)

    print(features_df)

    # Affichage des résultats
    if show_images:
        plt.subplot(1, 3, 1)
        plt.imshow(image)
        plt.title("Image originale")
        plt.subplot(1, 3, 2)
        plt.imshow(preprocessed_image, cmap="gray")
        plt.title("Image prétraitée")
        plt.subplot(1, 3, 3)
        plt.imshow(image_colorier)
        plt.title("Grains segmentés")
        plt.show()

dir_path = "Images/"
images_names = [
    "Echantillion1Mod2_301.png",
    "Echantillion1Mod2_302.png",
    "Echantillion1Mod2_303.png",
    "Echantillion1Mod2_304.png",
    "Echantillion1Mod2_305.png",
    "Echantillion1Mod2_306.png",
    "Echantillion1Mod2_316.png",
    "Echantillion1Mod2_422.png",
    "Echantillion1Mod2_471.png"
]

if __name__ == "__main__":
    # for img_name in images_names:
    #     main(dir_path + img_name, show_images=True)
    main("Images/Echantillion1Mod2_316.png", show_images=True)