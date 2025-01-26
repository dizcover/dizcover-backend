from rest_framework import viewsets, status
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Establecimiento
from discotequero.models import Discotequero
from establecimiento.models import Establecimiento, ImagenEstablecimiento, Horario, HorarioEstablecimiento, Coordenada
from rest_framework.views import APIView
from .serializer import EstablecimientoSerializer, ImagenEstablecimientoSerializer, HorarioEstablecimientoSerializer, CoordenadaSerializer




class EstablecimientoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar la creación y visualización de Establecimientos.
    """
    queryset = Establecimiento.objects.all()
    serializer_class = EstablecimientoSerializer

    @transaction.atomic #Con este decorador hacemos garantiazar que si falla algo en el proceso, no se vera en la base de datos información incompleta dado a esto.
    def create(self, request, *args, **kwargs):
        """
        Crea un nuevo establecimiento solo si no existe uno previamente duplicado.
        - La condicion para que un establecimiento sea duplicado es que tenga el mismo nombre y direccion en la misma ciudad. (Se debe mejorar la validacion)
        """

        # Obtenemos los datos para validar si ya existe un establecimiento con los mismos datos (Con estos atributos que son esecniales para la creación de un establecimiento)
        id_discotequero = request.data.get("id_discotequero")
        nombre = request.data.get("nombre")
        direccion = request.data.get("direccion")
        departamento = request.data.get("departamento")
        municipio = request.data.get("municipio")
    

        datosIncompletos = not id_discotequero or not nombre or not direccion or not departamento or not municipio
        if datosIncompletos:
            return Response(
                {'detail': 'Debe proporcionar los datos completos.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Verificar si el discotequero existe
            get_object_or_404(Discotequero, id=id_discotequero)
        except:
            return Response(
                {'detail': 'Discotequero no encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # (Se debe mejorar la validacion)
        # Se maneja desde esta vista el tema de no duplicar un establecimiento
        existeEstablecimiento = Establecimiento.objects.filter(nombre=nombre, direccion=direccion, departamento=departamento, municipio=municipio).exists()
        if existeEstablecimiento:
            return Response(
                {'detail': 'Este establecimiento ya se encuentra registrado.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # (Se debe mejorar la validacion)
        duplicadoPorDiscotequero = Establecimiento.objects.filter(nombre=nombre, id_discotequero=id_discotequero).exists()
        if duplicadoPorDiscotequero:
            return Response(
                {'detail': 'El discotequero ya tiene un establecimiento con este nombre.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Si hay ningun error, crear la entidad
        return super().create(request, *args, **kwargs)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """
        Actualiza un establecimiento existente solo si cumple con las validaciones.
        """
        id_establecimiento = kwargs.get('pk')
        id_discotequero = request.data.get("id_discotequero")
        nombre = request.data.get("nombre")
        direccion = request.data.get("direccion")
        departamento = request.data.get("departamento")
        municipio = request.data.get("municipio")

        datosIncompletos = not id_establecimiento or not id_discotequero or not nombre or not direccion or not departamento or not municipio
        if datosIncompletos:
            return Response(
                {'detail': 'Debe proporcionar los datos completos.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Verificar si el establecimiento existe
            establecimiento = get_object_or_404(Establecimiento, id=id_establecimiento)
        except:
            return Response(
                {'detail': 'Establecimiento no encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            # Verificar si el discotequero existe
            get_object_or_404(Discotequero, id=id_discotequero)
        except:
            return Response(
                {'detail': 'Discotequero no encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # (Se debe mejorar la validacion)

        # Verificar si el discotequero ya tiene un establecimiento con este nombre
        duplicadoPorDiscotequero = Establecimiento.objects.filter(nombre=nombre, id_discotequero=id_discotequero).exclude(id=id_establecimiento).exists()
        
        if duplicadoPorDiscotequero:
            return Response(
                {'detail': 'El discotequero ya tiene un establecimiento con este nombre.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Si no pasa nada, actualizamos la entidad
        return super().update(request, *args, **kwargs)
    
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """
        Elimina un establecimiento existente.
        """
        id_establecimiento = kwargs.get('pk')

        try:
            # Verificar si el establecimiento existe
            establecimiento = get_object_or_404(Establecimiento, id=id_establecimiento)
        except:
            return Response(
                {'detail': 'Establecimiento no encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Eliminar el establecimiento
        establecimiento.delete()

        return Response(
            {'detail': 'Establecimiento eliminado exitosamente.'},
            status=status.HTTP_200_OK
        )

# API de imagenes de establecimientos
class ImagenesEstablecimientoView(APIView):
    # Recibe el id del establecimiento al que se le asociará la imagen
    def post(self, request, pk):
        """
        Crea una nueva imagen asociada a un establecimiento.

        La estructura de debe ser un Form Data en la cual se pueden mandar varias imagenes a la vez. Ejemplo:
            imagen1: imagen1.jpg
            imagen2: imagen2.jpg
            ...
            imagen5: imagen5.jpg
        """
        try:
            establecimiento = get_object_or_404(Establecimiento, id=pk)
            imagenes_existentes = ImagenEstablecimiento.objects.filter(establecimiento=establecimiento).count()
            imagenes = [request.data.get(f'imagen{i}') for i in range(1, len(request.data)+1)]
            suma_imgenes_guardas_subidas = imagenes_existentes + len([imagen for imagen in imagenes if imagen])

            # Validar el tipo de archivo de las imágenes
            #webp 0 jpg 200 o jpg xr 
            formatos_permitidos = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']
            for imagen in imagenes:
                if imagen and imagen.content_type not in formatos_permitidos:
                    return Response(
                        {'detail': 'Formato de imagen no permitido. Solo se permiten imágenes JPEG, PNG, JPG o WebP.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            if imagenes_existentes >= 10 or suma_imgenes_guardas_subidas > 10:
                return Response(
                    {'detail': 'El establecimiento no puede tener más de 10 imágenes.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not any(imagenes):
                return Response(
                    {'detail': 'Debe proporcionar al menos una imagen.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            for imagen in imagenes:
                if imagen:
                    total_size_mb = imagen.size / (1024 * 1024)
                    if total_size_mb > 5:  # Limite de tamaño total de imágenes en MB
                        return Response(
                        {'detail': 'El tamaño total de las imágenes no puede exceder los 5 MB.'},
                        status=status.HTTP_400_BAD_REQUEST
                        )
                    else:
                        ImagenEstablecimiento.objects.create(establecimiento=establecimiento, imagen=imagen)
                
            return Response(
                {'detail': 'Imagen/es creada exitosamente.'},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'Error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
    def get(self, request, pk):
        """
        Obtiene las imágenes asociadas a un establecimiento.
        """
        try:
            establecimiento = get_object_or_404(Establecimiento, id=pk)
            imagenes = ImagenEstablecimiento.objects.filter(establecimiento=establecimiento)
            serializer = ImagenEstablecimientoSerializer(imagenes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'Error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk_imagen):
        """
        Elimina una imagen asociada a un establecimiento.
        """
        try:
            imagen = get_object_or_404(ImagenEstablecimiento, id=pk_imagen)
            imagen.delete()
            return Response(
                {'detail': 'Imagen eliminada exitosamente.'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'Error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
# API Horario


class HorarioEstablecimientoView(APIView):
    def post(self, request, pk):
        """
        Crea nuevos horarios asociados a un establecimiento, asegurando que no haya días duplicados.

        El Json enviado debe tener la siguiente estructura:
        {
            "Lunes": {
                "hora_apertura": "10:00",
                "hora_cierre": "23:30"
            },
            "Domingo": {
                "hora_apertura": "10:00",
                "hora_cierre": "23:30"
            },
            "Miércoles": {
                "hora_apertura": "10:00",
                "hora_cierre": "23:30"
            }
        }

        """
        # Obtener el establecimiento
        establecimiento = get_object_or_404(Establecimiento, pk=pk)

        # Obtener los datos del request (esperamos varios días con su hora de apertura y cierre)
        horarios = request.data

        # Lista para almacenar los días duplicados
        dias_duplicados = []

        # Iterar sobre los días en el JSON enviado
        for dia, horario_data in horarios.items():
            # Verificar que el día no esté duplicado para el establecimiento
            if HorarioEstablecimiento.objects.filter(establecimiento=establecimiento, horario__dia=dia).exists():
                dias_duplicados.append(dia)
                continue  # Si el día ya está asignado, saltamos a la siguiente iteración

            # Crear el horario
            hora_apertura = horario_data.get('hora_apertura')
            hora_cierre = horario_data.get('hora_cierre')

            if not hora_apertura or not hora_cierre:
                return Response(
                    {'detail': f"Los horarios de apertura y cierre son obligatorios para {dia}."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            horario = Horario.objects.create(dia=dia, hora_apertura=hora_apertura, hora_cierre=hora_cierre)
            
            # Asociar el horario al establecimiento
            HorarioEstablecimiento.objects.create(establecimiento=establecimiento, horario=horario)

        if dias_duplicados:
            return Response(
                {'detail': f"Ya existe un horario para los días: {', '.join(dias_duplicados)}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'detail': "Horario/s creados exitosamente."},
            status=status.HTTP_201_CREATED
        )

    def get(self, request, pk):
        """
        Obtiene los horarios asociados a un establecimiento, incluyendo el ID del horario y el día.
        """
        # Obtener el establecimiento
        establecimiento = get_object_or_404(Establecimiento, pk=pk)
        
        # Obtener todos los horarios asociados al establecimiento
        horarios = HorarioEstablecimiento.objects.filter(establecimiento=establecimiento)
        
        
        # Serializar los horarios
        serializer = HorarioEstablecimientoSerializer(horarios, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """
        Elimina un horario asociado a un establecimiento.
        """
        
        # Obtener el día del horario a eliminar
        
        # Buscar el horario para ese día
        dia = Horario.objects.filter(
            id=pk
        ).first()
        
        if not dia:
            return Response(
                {'detail': f"No se encontró un horario para el día {dia.dia}."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Eliminar el horario
        dia.delete()
        
        return Response(
            {'detail': f"Horario para el día {dia.dia} eliminado exitosamente."},
            status=status.HTTP_200_OK
        )
    
    def put(self, request, pk):
        """
        Actualiza un horario asociado a un establecimiento.
        """
        try:
            # Obtener el día del horario a actualizar
            dia = Horario.objects.filter(id=pk).first()
            
            # Actualizar el horario
            dia.hora_apertura = request.data.get('hora_apertura', dia.hora_apertura)
            dia.hora_cierre = request.data.get('hora_cierre', dia.hora_cierre)
            dia.save()
            
            return Response(
            {'detail': f"Horario para el día {dia.dia} actualizado exitosamente."},
            status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
            {'Error': "El horario no pudo ser actualizado. Verifique los datos enviados."},
            status=status.HTTP_400_BAD_REQUEST
        )

def validar_coordenadas(latitud, longitud, hemisferio_lat, hemisferio_lon):
        """
        Valida las coordenadas proporcionadas.
        """
        if latitud is not None:
            latitud = float(latitud)
            if latitud < -90.0 or latitud > 90.0:
                return {'detail': 'Latitud debe estar entre -90.0 y 90.0.'}

        if longitud is not None:
            longitud = float(longitud)
            if longitud < -180.0 or longitud > 180.0:
                return {'detail': 'Longitud debe estar entre -180.0 y 180.0.'}

        if hemisferio_lat not in ['N', 'S']:
            return {'detail': 'Hemisferio de latitud debe ser "N" o "S".'}

        if hemisferio_lon not in ['E', 'O']:
            return {'detail': 'Hemisferio de longitud debe ser "E" o "O".'}

        if latitud is None or longitud is None:
            return {'detail': 'Latitud y longitud son requeridos.'}

        return None

#API Coordenadas
class CoordenadaEstablecimientoView(APIView):
    #TODO: Incluir coordenadas planas (cuantos metros al n o s, ect)

    def post(self, request, pk):
        """
        Crea una nueva coordenada asociada a un establecimiento.
        """
        try:
            # Obtener el establecimiento por el pk
            establecimiento = get_object_or_404(Establecimiento, pk=pk)

            # Extraer los datos del request
            latitud = request.data.get('latitud')
            longitud = request.data.get('longitud')
            hemisferio_lat = request.data.get('hemisferio_lat')
            hemisferio_lon = request.data.get('hemisferio_lon')

            # Validar las coordenadas
            error = validar_coordenadas(latitud, longitud, hemisferio_lat, hemisferio_lon)
            if error:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            # Crear la coordenada
            coordenada = Coordenada.objects.create(
                establecimiento=establecimiento,
                latitud=latitud,
                longitud=longitud,
                hemisferio_lat=hemisferio_lat,
                hemisferio_lon=hemisferio_lon
            )

            # Serializar la respuesta
            serializer = CoordenadaSerializer(coordenada)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'Error': "No se pudo crear la coordenada. Verifique los datos enviados y que el establecimiento no tenga coordenadas ya creadas."},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, pk):
        """
        Obtiene todas las coordenadas asociadas a un establecimiento.
        """
        try:
            establecimiento = get_object_or_404(Establecimiento, pk=pk)

            # Obtener todas las coordenadas del establecimiento
            coordenadas = Coordenada.objects.filter(establecimiento=establecimiento)

            # Serializar las coordenadas
            serializer = CoordenadaSerializer(coordenadas, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'Error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk, coord_pk):
        """
        Actualiza una coordenada asociada a un establecimiento.
        """
        try:
            # Obtener el establecimiento y la coordenada a actualizar
            establecimiento = get_object_or_404(Establecimiento, pk=pk)
            coordenada = get_object_or_404(Coordenada, pk=coord_pk, establecimiento=establecimiento)

            # Actualizar los campos de la coordenada
            latitud = request.data.get('latitud')
            longitud = request.data.get('longitud')
            hemisferio_lat = request.data.get('hemisferio_lat')
            hemisferio_lon = request.data.get('hemisferio_lon')

            # Validar las coordenadas
            error = validar_coordenadas(latitud, longitud, hemisferio_lat, hemisferio_lon)
            if error:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            if latitud is not None:
                coordenada.latitud = latitud
            if longitud is not None:
                coordenada.longitud = longitud
            if hemisferio_lat is not None:
                coordenada.hemisferio_lat = hemisferio_lat
            if hemisferio_lon is not None:
                coordenada.hemisferio_lon = hemisferio_lon

            coordenada.save()

            # Serializar y devolver la coordenada actualizada
            serializer = CoordenadaSerializer(coordenada)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'Error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk, coord_pk):
        """
        Elimina una coordenada asociada a un establecimiento.
        """
        try:
            # Obtener el establecimiento y la coordenada a eliminar
            establecimiento = get_object_or_404(Establecimiento, pk=pk)
            coordenada = get_object_or_404(Coordenada, pk=coord_pk, establecimiento=establecimiento)

            coordenada.delete()

            return Response(
                {'detail': 'Coordenada eliminada exitosamente.'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {'Error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )