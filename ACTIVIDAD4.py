from abc import ABC, abstractmethod
import logging

# Configuración de logs
logging.basicConfig(filename="logs.txt", level=logging.ERROR)

# Clase abstracta general
class Entidad(ABC):
    @abstractmethod
    def validar(self):
        pass

# Clase Cliente con encapsulación y validaciones
class Cliente(Entidad):
    def __init__(self, nombre, correo, telefono):
        self.__nombre = nombre
        self.__correo = correo
        self.__telefono = telefono
        self.validar()

    def validar(self):
        if not self.__nombre or not isinstance(self.__nombre, str):
            raise ValueError("Nombre inválido")
        if "@" not in self.__correo:
            raise ValueError("Correo inválido")
        if not self.__telefono.isdigit():
            raise ValueError("Teléfono inválido")

    def get_nombre(self):
        return self.__nombre

# Clase abstracta Servicio
class Servicio(Entidad, ABC):
    @abstractmethod
    def calcular_costo(self, duracion):
        pass

# Servicios especializados
class ReservaSala(Servicio):
    def calcular_costo(self, duracion, impuesto=0.19):
        return (50 * duracion) * (1 + impuesto)

    def validar(self):
        if duracion <= 0:
            raise ValueError("Duración inválida")

class AlquilerEquipo(Servicio):
    def calcular_costo(self, duracion, descuento=0):
        return (30 * duracion) - descuento

    def validar(self):
        if duracion <= 0:
            raise ValueError("Duración inválida")

class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, duracion, tarifa=100):
        return duracion * tarifa

    def validar(self):
        if duracion <= 0:
            raise ValueError("Duración inválida")

# Excepción personalizada
class ServicioNoDisponibleError(Exception):
    def __init__(self, mensaje="El servicio no está disponible"):
        super().__init__(mensaje)

# Clase Reserva
class Reserva:
    def __init__(self, cliente, servicio, duracion):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self):
        try:
            costo = self.servicio.calcular_costo(self.duracion)
            self.estado = "Confirmada"
            print(f"Reserva confirmada. Costo: {costo}")
        except Exception as e:
            logging.error(f"Error al confirmar reserva: {e}")
            self.estado = "Fallida"

    def cancelar(self):
        self.estado = "Cancelada"
        print("Reserva cancelada correctamente")

# Simulación de operaciones
def simulacion():
    print("=== INICIO DE SIMULACIÓN ===")

    try:
        cliente1 = Cliente("Juan Pérez", "juan@mail.com", "123456")
        print("Cliente válido creado:", cliente1.get_nombre())
    except Exception as e:
        logging.error(f"Error creando cliente válido: {e}")

    try:
        cliente2 = Cliente("", "correo@mail.com", "987654")
    except Exception as e:
        logging.error(f"Error creando cliente inválido: {e}")

    sala = ReservaSala()
    equipo = AlquilerEquipo()
    asesoria = AsesoriaEspecializada()

    reserva1 = Reserva(cliente1, sala, 2)
    reserva1.confirmar()

    reserva2 = Reserva(cliente1, equipo, 3)
    reserva2.confirmar()

    reserva3 = Reserva(cliente1, asesoria, 1)
    reserva3.confirmar()
    reserva3.cancelar()

    print("=== FIN DE SIMULACIÓN ===")

if __name__ == "__main__":
    simulacion()
