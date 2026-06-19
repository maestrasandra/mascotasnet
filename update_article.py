import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mascotasnet.settings")
django.setup()

from core.models import ArticuloInformativo

a = ArticuloInformativo.objects.filter(titulo__icontains="Guía Completa").first()
if a:
    a.contenido = """Tener un perro es una de las experiencias más gratificantes de la vida, pero también conlleva una gran responsabilidad. Para asegurar que tu compañero peludo tenga una vida larga, sana y feliz, es fundamental cubrir todas sus necesidades físicas y emocionales. A continuación, te presentamos nuestra guía completa de cuidado.

1. Alimentación Balanceada
Una buena nutrición es la base de la salud. Es vital elegir un alimento de alta calidad adecuado para la edad, tamaño y nivel de actividad de tu perro. Los cachorros necesitan dietas ricas en calorías para su desarrollo, mientras que los perros mayores se benefician de alimentos formulados para cuidar sus articulaciones. Recuerda siempre mantener un recipiente con agua fresca y limpia a su disposición.

2. Ejercicio Diario
Los perros necesitan actividad física diaria no solo para mantenerse en forma, sino también para su bienestar mental. Dependiendo de la raza, un perro puede necesitar desde un par de paseos cortos al día hasta largas carreras y juegos intensos. El ejercicio ayuda a prevenir el aburrimiento, que a menudo se traduce en comportamientos destructivos en el hogar.

3. Higiene y Aseo
El cuidado del pelaje de tu perro dependerá de su raza, pero el cepillado regular es recomendado para todos; ayuda a eliminar el pelo muerto y distribuye los aceites naturales de su piel. Además, no olvides el cuidado dental (cepillar sus dientes un par de veces a la semana previene enfermedades periodontales) y el corte regular de sus uñas. Bañarlo una vez al mes suele ser suficiente para la mayoría de las razas.

4. Visitas al Veterinario
La prevención es tu mejor aliada. Lleva a tu perro al veterinario al menos una vez al año para un chequeo general. Mantén al día su calendario de vacunación y asegúrate de proporcionarle tratamientos contra parásitos internos y externos (como pulgas y garrapatas). Si notas cualquier cambio repentino en su apetito, energía o comportamiento, no dudes en consultar a un profesional.

5. Entrenamiento y Socialización
Un perro bien educado es un perro feliz. Dedica tiempo a enseñarle comandos básicos y normas de convivencia usando refuerzo positivo (premios, caricias). La socialización temprana con otros perros, personas y entornos es crucial para que desarrolle confianza y no sea temeroso o agresivo en el futuro.

6. Cariño y Atención
Por último, pero no menos importante, los perros son animales extremadamente sociales que forman lazos profundos con sus familias. Dedícale tiempo de calidad todos los días: juega con él, háblale y hazle saber que es amado. Un entorno lleno de cariño es fundamental para su estabilidad emocional.

Con amor, paciencia y siguiendo estos consejos, garantizarás que tu mejor amigo disfrute de la mejor calidad de vida a tu lado."""
    a.save()
    print("Articulo actualizado.")
else:
    print("Articulo no encontrado.")
