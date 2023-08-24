class Auto():
    """Se crea una clase llamada Auto"""
    def __init__(self, numero_puertas, numero_ruedas, color):
        """Este es el constructor de la clase Auto"""
        # atributos
        self.numero_puertas = numero_puertas
        self.numero_ruedas = numero_ruedas
        self.color = color
        # el constructor define y establece que todos los objetos creados a partir de esta clase tendrán
        # n puertas, n ruedas y color
        
# instancias de la clase Auto
auto1= Auto(4, 4, 'rojo')
auto2= Auto(2, 4, 'azul')
auto3= Auto(7, 4, 'verde')