from abc import ABC, abstractmethod
import logging

# Configuración de logs
logging.basicConfig(filename="logs.txt", level=logging.ERROR,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Excepciones personalizadas
class ClienteInvalidoError(Exception):
    pass

class ServicioNoDisponibleError(Exception):
    pass

class ReservaError(Exception):
    pass

# Clase abstracta base
class EntidadSistema(ABC):
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

    @abstractmethod
    def validar(self):
        pass

# Clase Cliente
class Cliente(EntidadSistema):
    def __init__(self, id, nombre, documento, correo, telefono):
        super().__init__(id, nombre)
        self.__documento = documento
        self.__correo = correo
        self.__telefono = telefono

    def validar(self):
        if not self.__correo or "@" not in self.__correo:
            raise ClienteInvalidoError("Correo inválido")
        if not self.__documento.isdigit():
            raise ClienteInvalidoError("Documento inválido")

    def __str__(self):
        return f"Cliente: {self.nombre}, Documento: {self.__documento}"

# Clase abstracta Servicio
class Servicio(EntidadSistema, ABC):
    def __init__(self, id, nombre, costo_base, disponible=True):
        super().__init__(id, nombre)
        self.costo_base = costo_base
        self.disponible = disponible

    @abstractmethod
    def calcular_costo(self, **kwargs):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    def validar(self):
        if self.costo_base <= 0:
            raise ValueError("Costo base inválido")

# Servicios especializados
class ReservaSala(Servicio):
    def calcular_costo(self, horas=1, impuestos=0.19):
        return self.costo_base * horas * (1 + impuestos)

    def describir_servicio(self):
        return f"Reserva de sala: {self.nombre}"

class AlquilerEquipo(Servicio):
    def calcular_costo(self, dias=1, descuento=0):
        return (self.costo_base * dias) - descuento

    def describir_servicio(self):
        return f"Alquiler de equipo: {self.nombre}"

class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, horas=1, tarifa_extra=50):
        return self.costo_base * horas + tarifa_extra

    def describir_servicio(self):
        return f"Asesoría especializada: {self.nombre}"

# Clase Reserva
class Reserva:
    def __init__(self, cliente, servicio, duracion):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar_reserva(self):
        try:
            self.servicio.validar()
            self.cliente.validar()
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError("Servicio no disponible")
            self.estado = "Confirmada"
        except Exception as e:
            logging.error(f"Error al confirmar reserva: {e}")
            raise ReservaError("No se pudo confirmar la reserva") from e

    def cancelar_reserva(self):
        self.estado = "Cancelada"

    def procesar_reserva(self):
        try:
            costo = self.servicio.calcular_costo(horas=self.duracion)
            print(f"Reserva procesada. Costo: {costo}")
        except Exception as e:
            logging.error(f"Error al procesar reserva: {e}")
            raise ReservaError("Error en el procesamiento") from e

# Simulación de 10 operaciones
if __name__ == "__main__":
    # 1. Cliente válido
    try:
        cliente1 = Cliente("C1", "Juan", "12345", "juan@mail.com", "3001234567")
        cliente1.validar()
        print("Cliente válido registrado:", cliente1)
    except Exception as e:
        print("Error:", e)

    # 2. Cliente inválido (correo incorrecto)
    try:
        cliente2 = Cliente("C2", "Ana", "67890", "ana_mail.com", "3009876543")
        cliente2.validar()
    except Exception as e:
        print("Error esperado:", e)

    # 3. Servicio válido
    servicio1 = ReservaSala("S1", "Sala de reuniones", 100)
    print(servicio1.describir_servicio())

    # 4. Servicio inválido (costo negativo)
    try:
        servicio2 = AlquilerEquipo("S2", "Proyector", -50)
        servicio2.validar()
    except Exception as e:
        print("Error esperado:", e)

    # 5. Reserva válida
    reserva1 = Reserva(cliente1, servicio1, 2)
    try:
        reserva1.confirmar_reserva()
        reserva1.procesar_reserva()
    except Exception as e:
        print("Error inesperado:", e)

    # 6. Reserva inválida (servicio no disponible)
    servicio3 = AsesoriaEspecializada("S3", "Consultoría TI", 200, disponible=False)
    reserva2 = Reserva(cliente1, servicio3, 3)
    try:
        reserva2.confirmar_reserva()
    except Exception as e:
        print("Error esperado:", e)

    # 7. Cancelación de reserva
    reserva1.cancelar_reserva()
    print("Reserva cancelada. Estado:", reserva1.estado)

    # 8. Procesamiento con parámetros inválidos
    try:
        reserva3 = Reserva(cliente1, servicio1, "dos")  # duración inválida
        reserva3.procesar_reserva()
    except Exception as e:
        print("Error esperado:", e)

    # 9. Cliente inválido (documento no numérico)
    try:
        cliente3 = Cliente("C3", "Pedro", "ABC123", "pedro@mail.com", "3011111111")
        cliente3.validar()
    except Exception as e:
        print("Error esperado:", e)

    # 10. Reserva exitosa con descuento
    servicio4 = AlquilerEquipo("S4", "Laptop", 80)
    reserva4 = Reserva(cliente1, servicio4, 5)
    try:
        reserva4.confirmar_reserva()
        costo = servicio4.calcular_costo(dias=5, descuento=50)
        print("Reserva exitosa. Costo con descuento:", costo)
    except Exception as e:
        print("Error inesperado:", e)

