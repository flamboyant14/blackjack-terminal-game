# Importes y archivos
import random
registroTransacciones = open("txts/registroTransacciones.txt", "w")
registroTransacciones.write("Bienvenido al registro de transacciones de mi casino.\n")

# Sistema de juego
def reiniciar():
    global manoJugador, manoCasa, baraja
    # Vaciar manos y reiniciar baraja
    manoJugador =[[],[]]
    manoCasa = [[],[]]
    baraja = [
        ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'],
        ['♥', '♥', '♥', '♥', '♥', '♥','♥', '♥','♥', '♥','♥', '♥','♥', '♣', '♣', '♣', '♣', '♣', '♣', '♣', '♣', '♣', '♣', '♣', '♣', '♣', '♠',  '♠', '♠', '♠', '♠', '♠', '♠', '♠', '♠', '♠', '♠', '♠', '♠', '♦', '♦', '♦', '♦', '♦', '♦', '♦', '♦', '♦', '♦', '♦', '♦', '♦',]
    ]

def cartaRandom():
    # Determinar index al azar
    indexRandom = random.randint(0, len(baraja[0]) -1)

    # Determinar carta con index
    valor = baraja[0][indexRandom]
    palo = baraja[1][indexRandom]
    
    # Sacar carta de la baraja
    del baraja[0][indexRandom]
    del baraja[1][indexRandom]

    # Regresar carta
    return valor, palo

def añadir(aqui):
    # Agregar carta random a baraja o mano entrada
    nuevaCarta = cartaRandom()
    aqui[0].append(nuevaCarta[0])
    aqui[1].append(nuevaCarta[1])

def mostrarMano(manoAMostrar):
    # Imprimir las cartas en la mano entregada
    for carta in range(len(manoAMostrar[0])):
        print('[',manoAMostrar[0][carta], manoAMostrar[1][carta],']')
    totalM = total(manoAMostrar)
    print("Valor total: ", totalM)

def verReglas():
    print("El objetivo es llegar lo más cerca posible a 21 sin pasarse.\nLas cartas del 2 al 10 valen su número.\nJ, Q y K valen 10. \nEl As vale 1 o 11, según convenga.\nEl jugador y el dealer reciben 2 cartas.\nEl jugador puede pedir más cartas (“Hit”) o quedarse con lo que tiene (“Stand”).\nSi el jugador pasa de 21, pierde automáticamente.\nCuando el jugador termina, el dealer juega: debe pedir cartas hasta tener al menos 17.\nGana quien esté más cerca de 21 sin pasarse.")

def repartirManosIniciales():
    # Repartir a jugador
    añadir(manoJugador)
    añadir(manoJugador)
    print("Tu mano:")
    mostrarMano(manoJugador)
    
    # Repartir a Casa
    añadir(manoCasa)
    print("Mano de la casa:")
    mostrarMano(manoCasa)

def total(aSumar):
    # Reiniciar total
    total = 0
    aces = 0

    # Dar valor a la carta
    for carta in aSumar[0]:
        if carta == 'J' or carta == 'Q' or carta == 'K':
            total += 10
        elif carta == 'A':
            total += 11
            aces += 1
        else:
            total += int(carta)
    
    # Convertir As a 1 si se pasa de 21
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    
    return total 

def hitCasa(apuestaInicial):
    # Mostrar mano entera de la casa
    añadir(manoCasa)
    total(manoCasa)
    print("La mano de la casa es:")
    mostrarMano(manoCasa)

    # Hit casa
    while total(manoCasa) < 17:
            print("La casa pidio carta")
            añadir(manoCasa)
            total(manoCasa)
            mostrarMano(manoCasa) 
            # Checar si se pasa
            if total(manoCasa) > 21:
                # GANA FICHAS
                cantidadFichas['rojas'] += apuestaInicial[0]
                cantidadFichas['azules'] += apuestaInicial[1]
                cantidadFichas['negras'] += apuestaInicial[2]
                print("La casa se paso de 21, ganaste!\n")
                mostrarFichas()
                registroTransacciones.write(f"\nEl usuario gano la apuesta, su balance ahora es de {balance}$ en fichas.")
                break # Regresa a main
                       
def comparacion(apuestaInicial):
    # Solo si la casa no ha perdido
    if total(manoCasa) < 21:
        # Determinar ganador
        if total(manoJugador) > total(manoCasa):
            # GANA FICHAS
            cantidadFichas['rojas'] += apuestaInicial[0]
            cantidadFichas['azules'] += apuestaInicial[1]
            cantidadFichas['negras'] += apuestaInicial[2]
            print("Le ganaste a la casa (", total(manoJugador), ">", total(manoCasa),")!\n")
            mostrarFichas()
            registroTransacciones.write(f"\nEl usuario gano la apuesta, su balance ahora es de {balance}$ en fichas.")
        elif total(manoJugador) == total(manoCasa):
            # NO PIERDE FICHAS
            print("Empataste con la casa (", total(manoJugador), "=", total(manoCasa),")!\n")
            mostrarFichas()
            registroTransacciones.write(f"\nEl usuario empato con la casa, su balance se mantiene igual ({balance}$) en fichas.")
        else:
            # PIERDE FICHAS
            cantidadFichas['rojas'] -= apuestaInicial[0]
            cantidadFichas['azules'] -= apuestaInicial[1]
            cantidadFichas['negras'] -= apuestaInicial[2]
            print("Te gano la casa! (", total(manoJugador), "<", total(manoCasa),")!\n")
            mostrarFichas()
            registroTransacciones.write(f"\nEl usuario perdio la apuesta, su balance ahora es de {balance}$ en fichas.")

def menuJugadas(apuestaInicial):
    # Menu Jugadas
    while True: 
        # Checar si el jugador se paso de 21 despues de cada jugada
        if total(manoJugador) > 21:
                # PIERDE FICHAS
                cantidadFichas['rojas'] -= apuestaInicial[0]
                cantidadFichas['azules'] -= apuestaInicial[1]
                cantidadFichas['negras'] -= apuestaInicial[2]
                print("Te pasaste de 21, perdiste.\n")
                mostrarFichas()
                registroTransacciones.write(f"\nEl usuario perdio la apuesta, su balance ahora es de {balance}$ en fichas.")
                break # Regresar a main
        
        # Jugadas
        try:
            jugada = int(input("Escoge Jugada:\n1. Hit\n2. Stand\n"))
            if jugada == 1:
                # Hit
                print("Tu mano:")
                añadir(manoJugador)
                mostrarMano(manoJugador)
            elif jugada == 2:
                # Stand
                hitCasa(apuestaInicial)
                comparacion(apuestaInicial)
                break # Regresar a main
            else:
                print("Por favor seleccione una jugada valida.") 
                break # Regresar a main
        except ValueError:
            print("Por favor seleccionar una opcion valida (1, 2)")
            continue

def mostrarFichas():
    global balance
    balance = (cantidadFichas['rojas'] * 5) + (cantidadFichas['azules'] * 10) + (cantidadFichas['negras'] * 25)
    print(f"\nTu balance: {balance}$\nDesglose: \nfichas rojas (5$): {cantidadFichas['rojas']}\nfichas azules (10$): {cantidadFichas['azules']}\nfichas negras (25$): {cantidadFichas['negras']}\n")

def apostar(balanceFichas):
    while True:
        try:
            # Recibir input de cuanto quiere apostar
            rojasApostadas = int(input("Cuantas fichas rojas (5$) quieres apostar esta ronda?\n"))
            azulesApostadas = int(input("Cuantas fichas azules (10$) quieres apostar esta ronda?\n"))
            negrasApostadas = int(input("Cuantas fichas negras (25$) quieres apostar esta ronda?\n"))

            # Asegurar que el input no sea negativo ni mas alto que el balance
            if negrasApostadas >= 0 and negrasApostadas <= balanceFichas['negras'] and azulesApostadas >= 0 and azulesApostadas <= balanceFichas['azules'] and rojasApostadas >= 0 and rojasApostadas <= balanceFichas['rojas']:
                # Retornar cantidad de fichas apostadas
                return rojasApostadas, azulesApostadas, negrasApostadas
            else:
                print("No puedes apostar mas fichas de las que tienes ni fichas negativas.")
        except ValueError:
            print("Por favor ingresa solo números enteros.")

def jugar():
    global apuestaInicial 
    # Apuesta 
    apuestaInicial = []
    mostrarFichas()
    # guardar ints en lista
    apuestaInicial = list(apostar(cantidadFichas)) 

    # Repartir Cartas Iniciales
    repartirManosIniciales()
    
    # Menu jugadas
    menuJugadas(apuestaInicial)

# Sistema de fichas
fichas = {"roja": 5, "azul": 10, "negra": 25}
cantidadFichas = {"rojas": 0, "azules": 0, "negras": 0}
balance = 0

def menuCajas():
    global balance
    while True:
        try:  
            menuCaja = int(input("\n♣ Bienvenido, ¿que operacion deseas realizar? ♥\n1. Comprar Fichas\n2. Vender Fichas\n3. Ver Balance\n4. Regresar\n"))
            if menuCaja == 1:
                # Comprar fichas
                paqueteAComprar = int(input("Que paquete de fichas quieres comprar? (Se te daran fichas que sumen a esa cantidad) (100$, 250$, 500$)\n"))
                try:
                    if paqueteAComprar == 100:
                        cantidadFichas['rojas'] += 5
                        cantidadFichas['azules'] += 5
                        cantidadFichas['negras'] += 1
                        registroTransacciones.write("\nEl usuario compro el paquete de 100$")
                    elif paqueteAComprar == 250:
                        cantidadFichas['rojas'] += 10
                        cantidadFichas['azules'] += 10
                        cantidadFichas['negras'] += 4
                        registroTransacciones.write("\nEl usuario compro el paquete de 250$")
                    elif paqueteAComprar == 500:
                        cantidadFichas['rojas'] += 20
                        cantidadFichas['azules'] += 20
                        cantidadFichas['negras'] += 8
                        registroTransacciones.write("\nEl usuario compro el paquete de 500$")
                except ValueError:
                    print("Por favor seleccionar el paquete que desea comprar solamente con el valor numerico del paquete (100, 250, 500)")
                    continue
            elif menuCaja == 2:
                # Vender fichas
                mostrarFichas()
                try:
                    confirmacion = int(input("Deseas vender tus fichas? (Presiona 1 para confirmar o 2 para cancelar)\n"))
                    if confirmacion == 1:
                        print(f"Canjeaste tus {cantidadFichas['rojas'] + cantidadFichas['azules'] + cantidadFichas['negras']} fichas por {balance}$")
                        registroTransacciones.write(f"\nSe le compraron las fichas al usuario por {balance}$")
                        cantidadFichas['rojas'] = 0
                        cantidadFichas['azules'] = 0 
                        cantidadFichas['negras'] = 0
                        balance = 0
                except:
                    print("Por favor seleccionar una opcion valida (1, 2).")
                    continue
            elif menuCaja == 3:
                # Ver el balance
                mostrarFichas()
            elif menuCaja == 4:
                # Regresar a main
                break
        except ValueError:
            print("Ingresa un numero del 1 al 4 para seleccionar una opcion valida.")

# main
while True:
    try: 
        opcMenu = int(input("\n♣ Blackjack ♥\n1. Jugar\n2. Ver Reglas\n3. Caja\n4. Salir\n"))
        if opcMenu == 1:
            reiniciar()
            jugar()
        elif opcMenu == 2:
            verReglas()
        elif opcMenu == 3:
            menuCajas()
        elif opcMenu == 4:
            # Salir del programa y cerrar archivo
            registroTransacciones.close()
            break
    except ValueError:
        print("Ingresa un numero del 1 al 4 para seleccionar una opcion valida.")
