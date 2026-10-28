# ============================================
# PROYECTO UNIDAD I - PROGRAMACIÓN III
# Estudiante: Bryan Fernandez
# Cédula: 32240469
# Enunciado: #6 - Sistema de Gestion de Empleados
# Fecha: 27 de octubre de 2026
# ============================================

# ======PERSONALIZACION======

ULTIMOS_2_DIGITOS_CEDULA = 69      
LETRAS_DE_MI_NOMBRE = 5     

# Calculo automatico del porcentaje de bono
PORCENTAJE_BONO = ULTIMOS_2_DIGITOS_CEDULA % 15
# Ejemplo: 34 % 15 = 4  -> el bono sera el 4% del salario (solo si gana < 500)


# ====== DEFINICION DE LA CLASE ======
class Empleado:
    def __init__(self, nombre, cedula, salario, departamento):
        """Constructor: se ejecuta automaticamente al crear un empleado."""
        self.nombre = nombre                 # tipo str
        self.cedula = cedula                 # tipo str (ej: "V-12345678")
        self.salario = float(salario)        # tipo float
        self.departamento = departamento     # tipo str
        self.activo = True                   # tipo bool 

    def calcular_bono(self):
        """Calcula el bono del empleado.
        Regla: si gana MENOS de 500, recibe X% de bono.
        Si gana 500 o mas, bono = 0."""
        if self.salario < 500:
            bono = self.salario * (PORCENTAJE_BONO / 100)
        else:
            bono = 0.0
        return bono

    def salario_total(self):
        """Devuelve salario base + bono."""
        return self.salario + self.calcular_bono()

    def mostrar_ficha(self):
        """Imprime en pantalla los datos completos del empleado."""
        print(f"  Cedula:        {self.cedula}")
        print(f"  Nombre:        {self.nombre}")
        print(f"  Departamento:  {self.departamento}")
        print(f"  Salario base:  {self.salario:.2f}")
        print(f"  Bono:          {self.calcular_bono():.2f} ({PORCENTAJE_BONO}% si <500)")
        print(f"  Salario TOTAL: {self.salario_total():.2f}")
        print("  " + "-" * 35)


# ====== FUNCIONES DE VALIDACION DE ENTRADA ======
def pedir_texto_no_vacio(mensaje):
    """Pide un texto y NO acepta que quede vacio."""
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        else:
            print("[ERROR] Este campo no puede estar vacio. Intenta de nuevo.")


def pedir_cedula_valida(lista_empleados):
    """Pide una cedula y valida:
       1) Formato correcto: V-XXXXXXX o E-XXXXXXX (solo numeros despues del guion)
       2) Que NO exista ya registrada (no se repite).
       Devuelve la cedula en MAYUSCULAS para normalizar."""
    while True:
        cedula = input("Cedula (ej V-12345678): ").strip().upper()

        # Validacion de formato: debe tener al menos V- + 1 digito
        formato_ok = False
        if len(cedula) >= 3 and cedula[1] == "-":
            if cedula[0] in ("V", "E") and cedula[2:].isdigit():
                formato_ok = True

        if not formato_ok:
            print("[ERROR] Formato invalido. Usa V-12345678 o E-12345678 (solo numeros).")
            continue  # vuelve a pedir

        # Validacion de cedula repetida
        repetida = False
        for emp in lista_empleados:
            if emp.cedula == cedula:
                repetida = True
                break

        if repetida:
            print("[ERROR] Ya existe un empleado con esa cedula. Intenta con otra.")
        else:
            return cedula


def pedir_salario_valido():
    """Pide el salario y SOLO acepta numeros positivos.
       Si el usuario escribe letras, no se crashea el programa."""
    while True:
        try:
            salario = float(input("Salario base: "))
            if salario > 0:
                return salario
            else:
                print("[ERROR] El salario debe ser mayor a 0.")
        except ValueError:
            print("[ERROR] Debes ingresar un numero (ej: 450.50).")


# ====== FUNCIONES DE LOGICA (fuera de la clase) ======
def contar_nombres_largos(lista_empleados, letras_minimas):
    """Cuenta cuantos empleados tienen un nombre con MAS letras
    que el nombre del estudiante (personalizacion obligatoria)."""
    contador = 0
    for emp in lista_empleados:                      # ciclo for
        letras = len(emp.nombre.replace(" ", ""))    # sin contar espacios
        if letras > letras_minimas:                  # operador de comparacion
            contador += 1                            # operador aritmetico
    return contador


def calcular_nomina_con_while(lista_empleados):
    """Calcula la nomina total (suma de todos los salarios totales)
    usando OBLIGATORIAMENTE un ciclo while (lo pide el enunciado)."""
    total = 0.0
    i = 0
    while i < len(lista_empleados):
        total += lista_empleados[i].salario_total()
        i += 1
    return total


# ====== PROGRAMA PRINCIPAL ======
if __name__ == "__main__":
    empleados = []       # Lista principal (usa .append() y .remove())
    departamentos = []   # Lista secundaria (usa .append() y .count())

    seguir = True        # tipo bool: controla el ciclo del menu

    print("=" * 45)
    print("   SISTEMA DE GESTION DE EMPLEADOS")
    print(f"   (Bono del {PORCENTAJE_BONO}% para salarios < 500)")
    print("=" * 45)

    while seguir:
        print("\n===== MENU PRINCIPAL =====")
        print("1. Agregar empleado")
        print("2. Mostrar empleados por departamento")
        print("3. Calcular nomina total")
        print("4. Mostrar empleado con mayor salario")
        print("5. Eliminar empleado (por cedula)")
        print("6. Contar nombres mas largos que el mio")
        print("7. Listar todos los empleados")
        print("0. Salir")

        opcion = input("Elige una opcion: ")

        # ---------- OPCION 1: AGREGAR (con validaciones) ----------
        if opcion == "1":
            nombre = pedir_texto_no_vacio("Nombre completo: ")
            cedula = pedir_cedula_valida(empleados)      # valida formato + no repetida
            salario = pedir_salario_valido()             # solo numeros positivos
            departamento = pedir_texto_no_vacio("Departamento: ")

            nuevo = Empleado(nombre, cedula, salario, departamento)
            empleados.append(nuevo)                      # metodo .append()

            # Guardar departamento si no existia (lista secundaria)
            if departamentos.count(departamento) == 0:
                departamentos.append(departamento)

            print(f"[OK] Empleado '{nombre}' agregado correctamente.")

        # ---------- OPCION 2: MOSTRAR POR DEPARTAMENTO ----------
        elif opcion == "2":
            if len(empleados) == 0:
                print("No hay empleados registrados.")
            else:
                depto = input("Que departamento quieres ver?: ").strip()
                print(f"\n--- Empleados de {depto} ---")
                encontrados = 0
                for emp in empleados:                    # ciclo for
                    if emp.departamento.lower() == depto.lower():
                        emp.mostrar_ficha()
                        encontrados += 1
                if encontrados == 0:
                    print("No se encontraron empleados en ese departamento.")

        # ---------- OPCION 3: NOMINA TOTAL (ciclo while) ----------
        elif opcion == "3":
            if len(empleados) == 0:
                print("No hay empleados registrados.")
            else:
                total = calcular_nomina_con_while(empleados)
                print(f"[+] Nomina TOTAL a pagar: {total:.2f}")

        # ---------- OPCION 4: MAYOR SALARIO ----------
        elif opcion == "4":
            if len(empleados) == 0:
                print("No hay empleados registrados.")
            else:
                mayor = empleados[0]
                for emp in empleados:                    # ciclo for
                    if emp.salario > mayor.salario:      # comparacion
                        mayor = emp
                print("[*] Empleado con MAYOR salario:")
                mayor.mostrar_ficha()

        # ---------- OPCION 5: ELIMINAR (usa .remove()) ----------
        elif opcion == "5":
            if len(empleados) == 0:
                print("No hay empleados registrados.")
            else:
                # Normalizamos a mayusculas para que funcione aunque escriban en minuscula
                cedula_buscar = input("Cedula del empleado a eliminar: ").strip().upper()
                eliminado = False
                for emp in empleados:
                    if emp.cedula == cedula_buscar:
                        empleados.remove(emp)            # metodo .remove()
                        print(f"[-] Empleado '{emp.nombre}' eliminado.")
                        eliminado = True
                        break
                if not eliminado:
                    print("No se encontro ningun empleado con esa cedula.")

        # ---------- OPCION 6: CONTAR NOMBRES LARGOS ----------
        elif opcion == "6":
            cantidad = contar_nombres_largos(empleados, LETRAS_DE_MI_NOMBRE)
            print(f"[i] Empleados con nombre mas largo que el mio "
                  f"(+{LETRAS_DE_MI_NOMBRE} letras): {cantidad}")

        # ---------- OPCION 7: LISTAR TODOS ----------
        elif opcion == "7":
            if len(empleados) == 0:
                print("No hay empleados registrados.")
            else:
                print(f"\n--- {len(empleados)} empleados registrados ---")
                for emp in empleados:
                    emp.mostrar_ficha()

        # ---------- OPCION 0: SALIR ----------
        elif opcion == "0":
            seguir = False
            print("Saliendo del sistema...")

        # ---------- OPCION INVALIDA ----------
        else:
            print("[ERROR] Opcion no valida, intenta de nuevo.")
