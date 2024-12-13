# **Projets de Vision Artificielle (8INF804)**  
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)  
![Langages](https://img.shields.io/badge/Languages-Python-blue)  
![Licence](https://img.shields.io/badge/License-MIT-lightgrey)  

Ce dépôt contient quatre projets réalisés dans le cadre du cours **Vision Artificielle (8INF804)** à l'UQAC. Chaque projet explore des concepts clés de la vision par ordinateur et met en œuvre des approches innovantes pour résoudre des problématiques spécifiques.

---

## **Contenu du dépôt**  

### 1. **Auto-Encodeur Débruiteur**  
![Denoising Autoencoder](https://via.placeholder.com/600x200.png?text=Image+Denoising+Autoencoder)  
- **Description** : Développement d’un auto-encodeur basé sur des CNN pour débruiter des images du dataset MNIST et améliorer la performance d’un modèle de classification.  
- **Points clés** :  
  - Extraction de caractéristiques à partir de l’espace latent.  
  - Comparaison de fonctions de perte (MSE, L1, SmoothL1).  
  - Résilience testée face à différents types de bruit (Poisson, Speckle, périodique).  
- **Compétences** : PyTorch, auto-encodeurs, traitement de bruit.  
- [Dossier du projet](./Autoencodeur_Debruiteur)  

---

### 2. **Détection de Pneumonie par CNN et Transfert Learning**  
![Pneumonia Detection](https://via.placeholder.com/600x200.png?text=Image+Pneumonia+Detection)  
- **Description** : Ce projet compare les performances d’un modèle CNN entraîné de zéro et d’un modèle pré-entraîné (ResNet50) pour la détection de pneumonie à partir de radiographies thoraciques.  
- **Points clés** :  
  - Fine-tuning de ResNet50 pour une tâche de classification binaire.  
  - Analyse approfondie des performances (F1-score, matrice de confusion).  
  - Gestion des données déséquilibrées.  
- **Compétences** : PyTorch, transfert learning, vision médicale.  
- [Dossier du projet](./Detection_Pneumonie_CNN)  

---

### 3. **Analyse et Segmentation d’Images Microscopiques**  
![Microscopic Image Analysis](https://via.placeholder.com/600x200.png?text=Image+Microscopic+Analysis)  
- **Description** : Segmentation et analyse de grains dans des images microscopiques pour extraire des caractéristiques et faciliter leur classification automatique.  
- **Points clés** :  
  - Utilisation de l’algorithme Watershed pour la segmentation.  
  - Prétraitement par CLAHE et analyse des composantes HSV.  
  - Génération de cartes de distance pour identifier les grains.  
- **Compétences** : OpenCV, segmentation d’images, algorithme Watershed.  
- [Dossier du projet](./Segmentation_Images_Microscopiques)  

---

### 4. **Détection des Changements dans une Scène Intérieure**  
![Scene Change Detection](https://via.placeholder.com/600x200.png?text=Image+Scene+Change+Detection)  
- **Description** : Ce projet détecte les objets déplacés ou mal rangés dans des pièces d’un appartement en conditions d’éclairage variées. Les changements pertinents sont mis en valeur à l’aide de bounding boxes.  
- **Points clés** :  
  - Utilisation des espaces de couleur LAB et de l’algorithme CLAHE pour normaliser les images.  
  - Identification des changements par calcul de différence absolue entre les images.  
  - Filtrage des détections pour exclure les faux positifs.  
- **Compétences** : OpenCV, traitement d’images, analyse de scènes.  
- [Dossier du projet](./Detection_Changements_Scene)  

---
Mathis Aulagnier
