# T-EVOLVERS
### Los commits recientes son agregados por la rama master
### Para hacer el despliegue se necesita que la maquina anfitrión tenga instalado y configurado docker y docker-compose
## Clonar repositorio
- git clone https://github.com/softkra/t-evolvers.git
#### *No deberia presentar problemas al momento de clonarlo ya que el repositorio es publico*
## Iniciar despliegue del proyecto mediante docker
- Una vez clonado el repositorio, se ingresa al directorio 't-evolvers'
- Con `docker-compose up --build -d` se iniciará la construccion de los contenedores docker que estan configurados para trabajar con la última version de Python 3 y la ultima de Django soportada por la version de python
- Una vez se creen los contenedores se puede hacer seguimiento a los logs con el comando `docker-compose logs -f`
## Seguimiento
- El admin de django se puede ver en el endpoint `localhost:8000/admin`, (usuario: `superuser` contraseña: `superpass`)
- De igual manera se habilita un endpoint mas amigable con algunas estadisticas que se pueden ver en el archivo de excel que se genera `localhost:80`


(https://drive.google.com/file/d/160yFZ1_aDAt5EaTrUkUJheXFLvnnk_7A/view?usp=sharing)
(https://drive.google.com/file/d/1WLNKHbQpRsE7vwfey7rDI1x2l2ONy1d8/view?usp=sharing)

La demás documentación se puede ver en el siguiente link: https://drive.google.com/drive/folders/1_16d0bOf1KddoiTz-31jRf-GBNpcghcr?usp=sharing


##### _El código almacenado en este GitHub fue desarrollado por Christian David Porres_
