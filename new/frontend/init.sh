#!/bin/bash
export $(grep -v '^#' .env | xargs)
echo "Valeur de LOCALHOST : $LOCALHOST"
echo "Contenu du fichier .env :"
cat .env
TARGET_DIR="./src"
find "$TARGET_DIR" -type f -exec sed -i "s/localhost/$LOCALHOST/g" {} +

echo "Remplacement terminé dans le répertoire $TARGET_DIR."
